#!/usr/bin/env python3
"""Validate shared Intelligence Powers governance contracts."""
import copy,json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[2]
SCHEMA=json.loads((ROOT/"schemas/powers/governance-contracts.v1.schema.json").read_text())
FIX=json.loads((ROOT/"examples/powers/governance-contracts.v1.json").read_text())
KEYS={"policy_bundle":"policyBundle","authzen_request":"authzenRequest","authzen_response":"authzenResponse","enforcement_receipt":"enforcementReceipt","audit_record":"auditRecord","sandbox_attestation":"sandboxAttestation","governance_benchmark":"governanceBenchmark","reputation_signal":"reputationSignal","capability_grant":"capabilityGrant"}
def valid(k,obj):
 s={"$schema":SCHEMA["$schema"],"$ref":"#/$defs/"+KEYS[k],"$defs":SCHEMA["$defs"]}
 Draft202012Validator.check_schema(s); Draft202012Validator(s).validate(obj)
 if k=="enforcement_receipt" and obj.get("fixture_only") and obj.get("verification_status")=="verified":
  raise ValueError("fixture-only signature cannot be marked verified")
def main():
 for k in KEYS: valid(k,FIX[k])
 assert FIX["policy_bundle"]["default_effect"]=="deny"
 assert FIX["enforcement_receipt"]["verification_status"]=="not-verified"
 g=FIX["capability_grant"]; assert set(g["delegated_capabilities"])<=set(g["capabilities"]); assert set(g["capabilities"])<=set(g["parent_capabilities"])
 b=FIX["governance_benchmark"]; scores=[b["dimensions"][d]["score"] for d in b["dimensions"]]
 assert abs(b["overall_score"]-sum(scores)/len(scores))<1e-9
 neg=[]
 x=copy.deepcopy(FIX); x["policy_bundle"]["default_effect"]="allow"; neg.append(("policy default deny","policy_bundle",x))
 x=copy.deepcopy(FIX); x["enforcement_receipt"]["signature_algorithm"]="none"; neg.append(("receipt signature algorithm","enforcement_receipt",x))
 x=copy.deepcopy(FIX); x["enforcement_receipt"]["verification_status"]="verified"; neg.append(("fixture signature state","enforcement_receipt",x))
 x=copy.deepcopy(FIX); x["sandbox_attestation"]["network_default"]="allow"; neg.append(("sandbox egress default","sandbox_attestation",x))
 x=copy.deepcopy(FIX); x["governance_benchmark"]["dimensions"]["policy_determinism"]["score"]=101; neg.append(("benchmark score range","governance_benchmark",x))
 x=copy.deepcopy(FIX); x["authzen_response"]["decision"]="allow"; neg.append(("AuthZEN boolean decision","authzen_response",x))
 x=copy.deepcopy(FIX); x["reputation_signal"]["confidence"]=1.2; neg.append(("reputation confidence range","reputation_signal",x))
 x=copy.deepcopy(FIX); x["audit_record"]["record_sha256"]="bad"; neg.append(("audit digest format","audit_record",x))
 x=copy.deepcopy(FIX); x["capability_grant"]["capabilities"]=["shell.exec"]; neg.append(("child capability must not exceed parent","capability_grant",x))
 for label,k,obj in neg:
  try: valid(k,obj)
  except Exception: continue
  raise AssertionError("negative case passed: "+label)
 print(f"PASS: {len(KEYS)} positive contract fixtures and {len(neg)} negative cases")
 print("LIMIT: no live PDP/PEP, enforcement runtime, sandbox, cryptographic verification, ledger anchoring, or governance assessor")
if __name__=="__main__":
 try: main()
 except Exception as e: print("FAIL:",e,file=sys.stderr); raise SystemExit(1)
