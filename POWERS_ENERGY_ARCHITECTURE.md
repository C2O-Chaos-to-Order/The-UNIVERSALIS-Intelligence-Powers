# UNIVERSALIS Powers: Open Energy Measurement, Optimization, and Synergy

**Owner:** UNIVERSALIS / MotherThread  
**Boundary:** Public, inspectable, local-first, and independently operable. Do not include C2O-private budgets, carbon ceilings, permit records, policies, identities, credentials, or operational receipts.  
**Status:** Shared schemas, synthetic fixtures, semantic checker, and CI authored in this branch. External candidate integrations are proposed, not adopted.

## 1. Powers definition

Powers are measurable, enforceable, and auditable capacities possessed by an agent or system—not merely permissions or evaluations. Energy efficiency is treated as a first-class observable and schedulable resource because it affects operating cost, sustainability, workload placement, and federated synergy.

UNIVERSALIS treats measurement as an independently inspectable evidence stream. Scheduling and optimization decisions must expose the basis for deferral, routing, compression, batching, frequency changes, migration, or abstention. The measurement and knowledge path must work locally and deterministically without requiring an LLM.

## 2. Open candidate tool map (owner-supplied; not adopted)

| Power function | Candidate tools | Intended role |
|---|---|---|
| Measurement and attribution | CodeCarbon; Zeus; Joular Core; Perfetto Wattson | CPU/GPU/DRAM measurement, hardware counter use where available, per-thread/task attribution, monitoring export |
| Carbon-aware scheduling | ebb-ai; Green SARC; GreenAccounter; Arboric | Grid/provider-aware deferral, forecast-before-action gates, geo-distributed workload shifting |
| Inference energy reduction | Joule; ModeSwitch-LLM; SDSIE; llm-zipper; sleeping_gpu_inference | Per-request energy/cost metadata, model/mode routing, serving efficiency, compression, local inference |
| Workflow and multi-agent efficiency | Murakkab; KAIROS; EcoxPU; SAGE | Profile-guided workflow optimization, context-aware scheduling, heterogeneous accelerator placement, independent sustainability instrumentation |

The supplied proposal includes performance figures for several candidates (for example, relative energy, GPU, latency, token, or cost reductions). These are owner-supplied research claims, not independently verified benchmarks and not acceptance criteria. Verify canonical source, license, maintainer, release activity, security, hardware support, baseline definition, workload, measurement method, reproducibility, and SLO impact before adoption.

## 3. Open implementation posture

- Keep core measurement, receipt parsing, contract validation, and synergy calculation available locally.
- Do not require a cloud account, proprietary provider, or LLM for the evidence path.
- Permit optional adapters for hardware counters, provider APIs, grid-carbon feeds, schedulers, model routers, and accelerator telemetry.
- Preserve raw observations, source references, calibration, sampling gaps, uncertainty, estimator identity, and derived-value lineage.
- Publish machine-readable receipts and schemas so a third party can recompute the reported values.
- Do not describe estimated CPU/TDP values as measured hardware-counter energy.

## 4. Shared measurement plane

The common measurement vocabulary covers:
- PDU for site/rack/host power;
- Intel RAPL CPU-package and memory-controller energy where supported;
- Kepler pod/container attribution via cgroup and hardware counters;
- GPU NVML sampling;
- CodeCarbon, Zeus, Joular Core, Perfetto/Wattson, Joule, and compatible adapters for request/task/thread-level attribution.

Each ecosystem retains its own storage and access controls. InfluxDB or another time-series store is an implementation choice, not a shared data store requirement.

**No-double-count rule:** PDU, RAPL, Kepler, and GPU telemetry are overlapping measurement/attribution views. A PDU may include CPU and GPU draw; Kepler may allocate the same host counters to containers. Do not sum the readings as independent consumption. Reconcile the scope tree and meter hierarchy, declare a single accounting boundary, and use explicit allocation for child scopes. Preserve meter uncertainty, actual sample frequency, and calibration status. One-second / 1 Hz sampling is a target only where hardware and collectors actually support it.

## 5. Forecast-before-action and task receipts

The common task receipt separates forecast from actual:
- forecast timestamp and method, expected values, and upper bounds for joules, CO2e, and cost;
- provider, model, region, timestamped carbon-intensity source, and workload cohort;
- actual joules, CO2e, cost, tokens, and measurement references;
- task result, SLO adherence, verified useful-work units, and verification reference;
- gate decision and optional permit/budget-grant references;
- signer, payload hash, signature algorithm, and signature data.

A UNIVERSALIS scheduler may defer non-urgent work to cleaner/cheaper windows, choose a more efficient model, apply caching/compression, reduce speculative work, or run a local model. The caller's deadline, privacy, quality, and SLO constraints remain explicit. Forecast ceilings are user/operator policy inputs; the shared schema does not prescribe private C2O carbon or energy thresholds.

## 6. Synergy factor

Version S-v1 preserves the owner-proposed measure:

`S = (W_federated / E_federated) / ((W_C2O,isolated + W_UNIVERSALIS,isolated) / (E_C2O,isolated + E_UNIVERSALIS,isolated))`

- `W` is normalized useful-work units from successful, independently verified, SLO-adherent outcomes; not raw prompts, tokens, attempts, or unverified text.
- `E` is reconciled joules inside a stated system boundary and time window.
- `S > 1` means higher useful-work-per-joule than the stated isolated baseline; `S < 1` means an orchestration tax for that workload cohort and accounting policy.

Valid comparisons use the same workload cohort, work-unit catalog, SLO profile, quality threshold, and comparable time window. If those differ, the metric may still be exploratory, but must not be presented as a clean federation gain/loss.

The energy inventory must apply the same categories to all scenarios (compute, memory, storage, network, orchestration, retries, and idle allocation where relevant). PDU/RAPL/Kepler/GPU overlap must be reconciled before computing S. Report measurement coverage and uncertainty next to the point estimate; do not interpret false precision as a verified improvement.

The calculation is local and reproducible from receipts. No central truth authority or shared central energy database is required.

## 7. Shared contract implementation

The v1 schema is `schemas/powers/powers-energy-contracts.v1.schema.json`, defining:
- `measurement`
- `task_receipt`
- `energy_budget_grant`
- `synergy_evaluation`

Synthetic non-production fixtures are in `examples/powers/powers-energy-fixtures.v1.json`; the dependency-free validator is `.github/scripts/powers_energy_contract.py`.

The validator checks timezone-aware measurement windows, estimated-meter provenance, overlap reconciliation declarations, forecast-before-execution ordering, receipt/outcome consistency, holder-bound budget attenuation, non-widening delegation, the no-double-count flag, and the S-v1 calculation. It does not cryptographically verify Ed25519 signatures or implement live hardware metering, carbon forecasting, a scheduler, or an optimizer.

The shared energy-budget grant schema defines holder binding and attenuation. It does not carry a real C2O grant. Actual grants, limits, authority state, and approval records remain local to the issuing ecosystem.

## 8. Implementation sequence

1. Inventory available PDU/RAPL/NVML sensors and report support/coverage by device.
2. Add one local, inspectable measurement adapter and an independent reconciliation test.
3. Implement task-level receipts with forecast, actual, provider/grid source, SLO, and verification references.
4. Add one carbon-aware deferral experiment and one inference efficiency experiment with fixed workloads and SLOs.
5. Compare against a reproducible baseline with repeated runs and uncertainty intervals.
6. Compute synergy locally from the shared receipts and publish the benchmark protocol and non-sensitive results.
7. Add optional MCP and cross-ecosystem PACT Passport adapters only after identity, attenuation, replay, revocation, and conformance tests.

## 9. Evidence status

| Item | Status |
|---|---|
| Owner-supplied UNIVERSALIS tool candidates recorded | Documented |
| Shared measurement / receipt / grant / synergy schemas | Implemented in this branch |
| Synthetic fixtures and dependency-free semantic validator | Implemented in this branch |
| GitHub Actions execution | Pending |
| Hardware measurement coverage and calibration | Pending |
| Carbon scheduling / inference / workflow integrations | Not implemented |
| Candidate source/license/security verification | Pending |
| Independent synergy benchmark | Not performed |
