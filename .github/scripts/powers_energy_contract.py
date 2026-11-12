#!/usr/bin/env python3
"""Dependency-free semantic checks for Powers energy, receipt, budget, and synergy contracts."""
from __future__ import annotations

import argparse
import copy
import json
import math
import sys
from datetime import datetime
from pathlib import Path

FIXTURE = Path("examples/powers/powers-energy-fixtures.v1.json")
REQUIRED_FIXTURES = {"measurement", "task_receipt", "energy_budget_grant", "synergy_evaluation"}

def parse_time(value: str, label: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include an explicit timezone")
    return parsed

def check_window(window: dict, label: str) -> tuple[datetime, datetime]:
    start = parse_time(window.get("start"), label + ".start")
    end = parse_time(window.get("end"), label + ".end")
    if end <= start:
        raise ValueError(f"{label} end must be later than start")
    return start, end

def validate_measurement(item: dict) -> None:
    if item.get("schema_version") != "1.0.0":
        raise ValueError("unsupported measurement schema version")
    if not item.get("measurement_id") or not item.get("source_ref"):
        raise ValueError("measurement ID and source reference are mandatory")
    if item.get("measurement_method") not in {"direct_counter", "instrumented", "estimated", "derived"}:
        raise ValueError("unsupported measurement method")
    if item.get("meter_kind") not in {"pdu", "rapl_cpu_package", "rapl_memory", "kepler_container", "gpu_nvml", "codecarbon", "zeus", "joular_core", "perfetto_wattson", "joule_api", "other"}:
        raise ValueError("unsupported meter kind")
    start, end = check_window(item["interval"], "measurement.interval")
    seconds = (end - start).total_seconds()
    energy = item.get("energy_joules")
    frequency = item.get("sample_frequency_hz")
    uncertainty = item.get("uncertainty_fraction")
    if not isinstance(energy, (int, float)) or energy < 0:
        raise ValueError("energy_joules must be non-negative")
    if not isinstance(frequency, (int, float)) or frequency <= 0:
        raise ValueError("sample_frequency_hz must be positive")
    if not isinstance(uncertainty, (int, float)) or not 0 <= uncertainty <= 1:
        raise ValueError("uncertainty_fraction must be between 0 and 1")
    if item["measurement_method"] == "estimated" and not item.get("estimator_id"):
        raise ValueError("estimated measurements require estimator_id")
    if item.get("average_power_watts") is not None:
        expected = energy / seconds
        if not math.isclose(item["average_power_watts"], expected, rel_tol=0.02, abs_tol=0.01):
            raise ValueError("average_power_watts does not reconcile with energy and interval")
    overlaps = item.get("overlaps_measurement_ids", [])
    if item["measurement_id"] in overlaps:
        raise ValueError("a measurement cannot overlap itself")
    if overlaps and item.get("allocation_basis", "none") == "none":
        raise ValueError("overlapping measurements require an explicit allocation/reconciliation basis")
    parse_time(item["captured_at"], "measurement.captured_at")

def validate_budget(grant: dict) -> None:
    if grant.get("schema_version") != "1.0.0":
        raise ValueError("unsupported energy budget grant version")
    if grant.get("holder_bound") is not True:
        raise ValueError("energy budget grant must be holder-bound")
    if not grant.get("holder_id") or not grant.get("holder_key_fingerprint"):
        raise ValueError("energy budget grant requires holder identity and key fingerprint")
    start = parse_time(grant["not_before"], "grant.not_before")
    end = parse_time(grant["expires_at"], "grant.expires_at")
    if end <= start:
        raise ValueError("grant expiry must be later than not_before")
    parent = grant.get("parent_constraints")
    if not isinstance(parent, dict):
        raise ValueError("delegated grants require parent constraints")
    parent_start = parse_time(parent["not_before"], "parent_constraints.not_before")
    parent_end = parse_time(parent["expires_at"], "parent_constraints.expires_at")
    if start < parent_start:
        raise ValueError("child grant starts before parent validity")
    if end > parent_end:
        raise ValueError("child grant expiry widens parent validity")
    if grant["max_energy_joules"] > parent["max_energy_joules"]:
        raise ValueError("child energy budget widens parent authority")
    if not set(grant["scope"]).issubset(set(parent["scope"])):
        raise ValueError("child scope widens parent authority")
    if not set(grant["operations"]).issubset(set(parent["operations"])):
        raise ValueError("child operations widen parent authority")
    if not grant.get("issuer_receipt_ref") or not grant.get("holder_receipt_ref"):
        raise ValueError("delegated budget grant requires receipts for issuer and holder")
    signature = grant.get("signature", {})
    if signature.get("algorithm") != "Ed25519" or not signature.get("value"):
        raise ValueError("energy budget grant requires an Ed25519 signature field")
    # Signature bytes are not cryptographically verified by this stdlib-only validator.

def validate_receipt(receipt: dict, measurement: dict, grant: dict, profile: str) -> None:
    if receipt.get("schema_version") != "1.0.0":
        raise ValueError("unsupported receipt schema version")
    start, end = check_window(receipt["execution_window"], "receipt.execution_window")
    forecast = receipt["forecast"]
    forecasted_at = parse_time(forecast["forecasted_at"], "receipt.forecast.forecasted_at")
    if forecasted_at >= start:
        raise ValueError("forecast must be recorded before task execution begins")
    if forecast.get("upper_bound_method") not in {"conformal", "quantile", "deterministic", "other"}:
        raise ValueError("forecast upper bound requires a declared method")
    if not 0 < forecast.get("confidence_level", 0) < 1:
        raise ValueError("forecast confidence_level must be between 0 and 1")
    for expected, upper in (
        ("energy_expected_joules", "energy_upper_joules"),
        ("co2e_expected_grams", "co2e_upper_grams"),
        ("cost_expected_usd", "cost_upper_usd"),
    ):
        if forecast[expected] > forecast[upper]:
            raise ValueError(f"forecast {upper} must be at least {expected}")
    if set(receipt["actual"]["measurement_refs"]) != set(receipt["measurement_refs"]):
        raise ValueError("actual and top-level measurement references must agree")
    if measurement["measurement_id"] not in receipt["measurement_refs"]:
        raise ValueError("receipt must reference the supplied measurement fixture")
    measure_start, measure_end = check_window(measurement["interval"], "measurement.interval")
    if measure_start < start or measure_end > end:
        raise ValueError("referenced measurement interval must be within the task execution window")
    actual = receipt["actual"]
    if receipt["outcome"]["useful_work_units"] > 0:
        if receipt["outcome"]["status"] != "succeeded" or not receipt["outcome"]["verified_outcome"] or not receipt["outcome"]["slo_adherent"]:
            raise ValueError("useful work counts only for successful, verified, SLO-adherent outcomes")
    if receipt["outcome"]["status"] != "succeeded" and receipt["outcome"]["useful_work_units"] > 0:
        raise ValueError("failed or incomplete tasks cannot contribute useful work units")
    gate = receipt["gate"]
    if gate["decision"] in {"denied", "deferred"} and receipt["outcome"]["status"] == "succeeded":
        raise ValueError("a denied or deferred action cannot be recorded as executed successfully")
    if gate["gate_type"] in {"human_permit", "combined"} and not gate.get("permit_ref"):
        raise ValueError("human-permit gate requires permit_ref")
    if gate["gate_type"] in {"energy_budget", "combined"}:
        if not gate.get("budget_grant_ref"):
            raise ValueError("energy-budget gate requires budget_grant_ref")
        if gate["budget_grant_ref"] != grant["grant_id"]:
            raise ValueError("receipt budget grant reference does not match the grant fixture")
        if actual["energy_joules"] > grant["max_energy_joules"]:
            raise ValueError("actual task energy exceeds its granted energy budget")
    if profile == "c2o" and receipt["outcome"]["status"] == "succeeded":
        if gate["gate_type"] not in {"energy_budget", "human_permit", "combined"} or gate["decision"] != "allowed":
            raise ValueError("C2O executed work requires an explicit allowed governance gate")
    if actual["energy_joules"] < 0 or actual["co2e_grams"] < 0 or actual["cost_usd"] < 0 or actual["carbon_intensity_g_per_kwh"] < 0:
        raise ValueError("actual energy, emissions, cost, and carbon intensity cannot be negative")
    if not actual.get("carbon_intensity_source"):
        raise ValueError("actual carbon intensity requires a source reference")
    expected_co2e = actual["energy_joules"] / 3600000.0 * actual["carbon_intensity_g_per_kwh"]
    if abs(actual["co2e_grams"] - expected_co2e) > max(1e-5, expected_co2e * 0.02):
        raise ValueError("actual CO2e does not reconcile with joules and carbon intensity")
    parse_time(receipt["attestation"].get("signed_at") or receipt["execution_window"]["end"], "receipt.attestation.signed_at")

def calculate_synergy(item: dict) -> float:
    fed = item["federated"]
    c2o = item["isolated_c2o"]
    uni = item["isolated_universalis"]
    if not all(part["slo_adherent"] for part in (fed, c2o, uni)):
        raise ValueError("synergy comparison requires SLO-adherent scenarios")
    if min(fed["useful_work_units"], c2o["useful_work_units"], uni["useful_work_units"]) <= 0:
        raise ValueError("all scenarios require positive useful work")
    if min(fed["energy_joules"], c2o["energy_joules"], uni["energy_joules"]) <= 0:
        raise ValueError("all scenarios require positive energy measurements")
    if item["accounting_policy"]["overlap_reconciliation"] != "no_double_count":
        raise ValueError("overlapping PDU/RAPL/Kepler/GPU measurements must be reconciled, never simply summed")
    federated_efficiency = fed["useful_work_units"] / fed["energy_joules"]
    isolated_efficiency = (c2o["useful_work_units"] + uni["useful_work_units"]) / (c2o["energy_joules"] + uni["energy_joules"])
    if isolated_efficiency <= 0:
        raise ValueError("isolated baseline efficiency must be positive")
    return federated_efficiency / isolated_efficiency

def validate_synergy(item: dict) -> None:
    if item.get("schema_version") != "1.0.0" or item.get("formula_version") != "S-v1":
        raise ValueError("unsupported synergy evaluation version")
    check_window(item["window"], "synergy.window")
    expected = calculate_synergy(item)
    if not math.isclose(item["computed_synergy_factor"], expected, rel_tol=1e-8, abs_tol=1e-10):
        raise ValueError(f"synergy factor mismatch: supplied={item['computed_synergy_factor']}, calculated={expected}")
    parse_time(item["evaluated_at"], "synergy.evaluated_at")

def load_fixtures(root: Path) -> dict:
    path = root / FIXTURE
    raw = json.loads(path.read_text(encoding="utf-8"))
    fixtures = raw.get("fixtures", {})
    missing = REQUIRED_FIXTURES - set(fixtures)
    if missing:
        raise ValueError("missing fixture sections: " + ", ".join(sorted(missing)))
    return fixtures

def self_test(root: Path) -> None:
    fixture = load_fixtures(root)
    measurement = fixture["measurement"]
    receipt = fixture["task_receipt"]
    grant = fixture["energy_budget_grant"]
    synergy = fixture["synergy_evaluation"]
    validate_measurement(measurement)
    validate_budget(grant)
    validate_receipt(receipt, measurement, grant, "universalis")
    validate_receipt(receipt, measurement, grant, "c2o")
    validate_synergy(synergy)
    failures = []

    bad = copy.deepcopy(grant)
    bad["max_energy_joules"] = bad["parent_constraints"]["max_energy_joules"] + 1
    failures.append((lambda: validate_budget(bad), "parent-budget widening"))

    bad = copy.deepcopy(grant)
    bad["not_before"] = "2026-11-10T00:00:00Z"
    failures.append((lambda: validate_budget(bad), "grant starts before parent"))

    bad = copy.deepcopy(grant)
    bad["scope"].append("private-extra-scope")
    failures.append((lambda: validate_budget(bad), "scope widening"))

    bad = copy.deepcopy(receipt)
    bad["forecast"]["forecasted_at"] = bad["execution_window"]["start"]
    failures.append((lambda: validate_receipt(bad, measurement, grant, "universalis"), "forecast after execution start"))

    bad = copy.deepcopy(receipt)
    bad["gate"]["decision"] = "denied"
    failures.append((lambda: validate_receipt(bad, measurement, grant, "c2o"), "denied execution"))

    bad = copy.deepcopy(measurement)
    bad["measurement_method"] = "estimated"
    bad["estimator_id"] = None
    failures.append((lambda: validate_measurement(bad), "estimated meter without estimator"))

    bad = copy.deepcopy(synergy)
    bad["accounting_policy"]["overlap_reconciliation"] = "sum_all"
    failures.append((lambda: validate_synergy(bad), "double-counted measurement layers"))

    bad = copy.deepcopy(receipt)
    bad["actual"]["co2e_grams"] = 99
    failures.append((lambda: validate_receipt(bad, measurement, grant, "universalis"), "actual CO2e inconsistent with energy and carbon intensity"))

    bad = copy.deepcopy(synergy)
    bad["computed_synergy_factor"] = 99
    failures.append((lambda: validate_synergy(bad), "forged synergy factor"))

    for operation, label in failures:
        try:
            operation()
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError("negative test unexpectedly passed: " + label)
    print("Powers energy contract self-test: PASS (4 positive profiles/records, 9 negative cases)")

def check(root: Path, profile: str) -> int:
    try:
        fixture = load_fixtures(root)
        validate_measurement(fixture["measurement"])
        validate_budget(fixture["energy_budget_grant"])
        validate_receipt(fixture["task_receipt"], fixture["measurement"], fixture["energy_budget_grant"], profile)
        validate_synergy(fixture["synergy_evaluation"])
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError, TypeError) as exc:
        print("Powers energy contract validation: FAIL")
        print(" - " + str(exc))
        return 1
    factor = calculate_synergy(fixture["synergy_evaluation"])
    print("Powers energy contract validation: PASS (measurement, task receipt, attenuable grant, synergy evaluation)")
    print(f"Synergy factor fixture: {factor:.6f}")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("c2o", "universalis"), default="universalis")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    if args.self_test:
        self_test(args.root.resolve())
    if args.check:
        return check(args.root.resolve(), args.profile)
    if not args.self_test:
        parser.error("choose --self-test and/or --check")
    return 0

if __name__ == "__main__":
    sys.exit(main())
