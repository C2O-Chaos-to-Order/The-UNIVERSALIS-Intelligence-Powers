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
| GitHub Actions execution | Passed — see POWERS_ENERGY_VALIDATION.md |
| Hardware measurement coverage and calibration | Pending |
| Carbon scheduling / inference / workflow integrations | Not implemented |
| Candidate source/license/security verification | Pending |
| Independent synergy benchmark | Not performed |


## 10. Power topology and optimizer competence evidence

Represent the energy system as a queryable graph: meter → host/device → runtime → model/request/task → agent/workflow → policy/budget → receipt → verified outcome. Map dependencies and blast radius before changing model routes, accelerator placement, batch windows, fan-out, or frequency controls. Kula, reponova, AnaxiGraph, GRASP, FlowForge, and wikifier are candidate mapping/impact tools; the MokuGraph JSON contract is a candidate shared rendering format. They are not installed or verified by this change.

Optimizer competence is a separate capability claim, not an energy measurement. Kredo, ToolGym, and SkillSeal are candidate skill-attestation and qualification patterns; they must not be treated as energy sensors or as authorization gates. PACT Passport is a candidate shared holder-bound delegation substrate, not a central trust authority.

## 11. Owner-supplied benchmark figures requiring independent reproduction

The following figures are carried forward as claims from the supplied proposal only. They are not verified performance evidence, adoption criteria, or guarantees:

| Candidate | Reported figure in supplied proposal | Required reproduction controls |
|---|---|---|
| Green SARC | 47% fewer tokens, 68% lower USD cost, 67% lower carbon, zero gate rejections | Workload and baseline definition, model/provider, gate behavior, energy/carbon instrumentation, latency and quality |
| ModeSwitch-LLM | 0.48× mean energy ratio; 51.7% lower energy per generated token | Same model, hardware, batch/concurrency, output quality, and sampling boundary |
| Murakkab | Up to 2.8× lower GPU usage, 3.7× lower energy, 4.3× lower cost | Workflow mix, SLOs, accelerator inventory, orchestration overhead, repeated trials |
| KAIROS | 27% average and up to 39.8% power reduction | Workload context, utilization, latency, hardware, and control stability |
| EcoxPU | 31.9–45% energy reduction (42% average) with at most 6% latency overhead | Supported accelerator stack, task placement, measured power boundary, latency/quality trade-offs |
| ebb-ai proposal context | 30–60% intra-day grid-intensity variation and a 50% batch-API discount | ISO/region, date/time series, provider terms, eligibility, and time-of-use baseline |

Do not promote these figures into default savings assumptions. Store the source, benchmark version, workload, device/provider, method, uncertainty, and independent reproduction receipt for each claim.

The executed checks and their exact run IDs, including the intermediate failed attempt and correction where applicable, are recorded in `POWERS_ENERGY_VALIDATION.md`.

## 12. Receipt precision and derived efficiency measures

The v1 task receipt records forecast upper-bound method, confidence level, and calibration reference, as well as the actual carbon-intensity value and its source. Actual CO2e must reconcile with actual joules and the stated carbon intensity within the validator's declared tolerance. The attenuable grant records both issuer-side and holder-side receipt references; the CI checks structural presence and non-widening constraints, not signature validity.

Useful derived measures include:
- energy per verified useful-work unit (J / useful-work unit);
- carbon per verified outcome (gCO2e / verified outcome);
- SLO-adherent useful-work units per joule;
- token throughput per watt, only when the time basis, token definition, and measured power window are explicitly stated.

A token-per-watt number without a time basis is ambiguous. Token count, token throughput, wattage, energy, and cost are separate measures and should not be substituted for one another.


## 13. Adapter compatibility and local scheduling thresholds

A Joule-compatible adapter may map `x-joule-energy-j`, `x-joule-co2-g`, and `x-joule-cost-usd` into the standard actual receipt fields (`energy_joules`, `co2e_grams`, and `cost_usd`). The header values remain claims from the serving path until their measurement provenance, scope, and uncertainty are inspectable and independently checked.

UNIVERSALIS operators may set local minimum synergy or maximum energy/carbon thresholds and use them to defer, reroute, or refuse work. These are local policy inputs, not a central truth authority or shared C2O policy. A measured S above 1 does not by itself authorize a workload or prove safety.
