# Engineering Toolchain and Initial Build Plan

**Repository:** `C2O-Chaos-to-Order/The-UNIVERSALIS-Intelligence-Powers`  
**Responsibility:** Intelligence Powers  
**Status:** Initial executable foundation in this branch; specialized candidates remain proposed pending verification.  
**Boundary:** Open UNIVERSALIS / independently operable. No C2O-private credentials, policies, authority state, or restricted operational data.

## Universal engineering foundation

- Least-privilege GitHub Actions CI, automated tests, and JSON contract/config validation.
- CodeQL/static analysis, secret scanning, dependency review, Dependabot, actionlint, and SBOM generation after settings, ownership, and outputs are confirmed.
- CycloneDX/SPDX, OSV-Scanner, Trivy/Grype, Gitleaks, SLSA provenance, in-toto attestations, cosign signing, and immutable releases as staged assurance capabilities.
- Pin toolchain versions and action references; preserve specifications, fixtures, execution logs, provenance, limitations, and version history.

**Foundation candidates:** Secure SDLC Evidence Collector; repo-assurance; Chainguard Actions; cnspec SBOM Cataloger; CodeQL; actionlint; OSV-Scanner; Trivy/Grype; Gitleaks; SLSA/in-toto; cosign. These are candidates, not verified integrations.

## Domain-specific candidate tools

@absolutejs/agent-conformance for adversarial credential/delegation/spend-mandate conformance; Agent Conformance Testing and agentic-dataset-conformance for behavioral evaluation; @openwop/openwop-conformance for workflow/MCP redaction invariants. Model powers as bounded, explicit, testable permissions; conformance never grants authority.

Verify each candidate's canonical source, license, maintainer, release activity, security, compatibility, data flow, and claims before adoption. Advertised capabilities are not evidence of repository implementation.

## Initial executable implementation

- `.github/workflows/repository-quality.yml` runs on pushes and pull requests with read-only repository permissions.
- `.github/scripts/repository_quality_baseline.py` provides a dependency-free self-test and validates JSON in schema/manifest/contract/capability/skill directories plus `package.json` and `tsconfig.json`.
- This narrow baseline does not replace formal ontology validation, skill sandboxing, CodeQL, secret scanning, SBOMs, or domain-specific conformance.

## Next increments

1. Audit current source, schemas, graph fixtures, workflow permissions, and dependencies.
2. Add positive/negative domain fixtures and deterministic contract tests.
3. Integrate the domain harness after source/license/security review.
4. Preserve validation outputs, dependency/SBOM evidence, provenance, and unresolved findings.

## Evidence status

| Item | Status |
|---|---|
| Tool candidates recorded | Documented |
| Baseline validator and CI authored | Implemented in this branch |
| GitHub Actions execution | Pending |
| Domain candidate verification | Pending |
| Specialized integration | Not yet implemented |

## Cross-repository architecture register — 2026-11-12

The following are the canonical working records for the latest owner-supplied toolchain proposals. This repository records the references and boundary rules; implementation belongs in the domain-owning repositories.

### Human Knowledge
- [C2O Human Knowledge architecture](https://github.com/C2O-Chaos-to-Order/The-C2O-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/HUMAN_KNOWLEDGE_ARCHITECTURE.md), [shared MCP interface contracts](https://github.com/C2O-Chaos-to-Order/The-C2O-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/MCP_INTERFACE_CONTRACTS.md), and [validation evidence](https://github.com/C2O-Chaos-to-Order/The-C2O-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/HUMAN_KNOWLEDGE_VALIDATION.md).
- [UNIVERSALIS Human Knowledge architecture](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/HUMAN_KNOWLEDGE_ARCHITECTURE.md), [shared MCP interface contracts](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/MCP_INTERFACE_CONTRACTS.md), and [validation evidence](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Human-Knowledge/blob/implementation/repository-foundation-2026-11-12/HUMAN_KNOWLEDGE_VALIDATION.md).

### OS provisioning and virtualization
- [C2O private provisioning architecture](https://github.com/C2O-Chaos-to-Order/The-C2O-Ecosystem/blob/implementation/repository-foundation-2026-11-12/OS_PROVISIONING_ARCHITECTURE.md).
- [UNIVERSALIS open provisioning architecture](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Ecosystem/blob/implementation/repository-foundation-2026-11-12/OS_PROVISIONING_ARCHITECTURE.md).

### UNIVERSALIN Grid, Guardian, and Golden Compass
- [C2O boundary and verifier architecture](https://github.com/C2O-Chaos-to-Order/The-C2O-Ecosystem/blob/implementation/repository-foundation-2026-11-12/UNIVERSALIN_GUARDIAN_GOLDEN_COMPASS.md).
- [UNIVERSALIS Grid / Guardian / Compass architecture](https://github.com/C2O-Chaos-to-Order/The-UNIVERSALIS-Ecosystem/blob/implementation/repository-foundation-2026-11-12/UNIVERSALIN_GUARDIAN_GOLDEN_COMPASS.md).

### Boundary and evidence status
C2O-private credentials, policies, identity state, authority tokens, private source text, and operational evidence remain inside authorized C2O environments. UNIVERSALIS remains public, local-first, inspectable, and independently operable. Only versioned, explicitly approved interface schemas and evidence packages may cross the boundary; an interface does not grant authority.

All named external tools remain owner-supplied candidates or reference patterns pending canonical-source, license, maintainer, release, security, compatibility, and claim verification. No candidate is represented as installed or adopted merely because it appears in these records.

## Powers energy-efficiency implementation

See `POWERS_ENERGY_ARCHITECTURE.md` for the open measurement, carbon scheduling, inference efficiency, and synergy model. Shared contract and synthetic fixture are in `schemas/powers/powers-energy-contracts.v1.schema.json` and `examples/powers/powers-energy-fixtures.v1.json`; the deterministic checker is `.github/scripts/powers_energy_contract.py`. Candidate integrations remain proposed and unverified; none is installed by this change.

The energy architecture records reported optimizer benchmark figures as unverified claims and ties energy receipts to workload/SLO hashes and a reconciled measurement graph; see `POWERS_ENERGY_ARCHITECTURE.md`.

Powers energy contract CI is passing for the current v1 semantic checks. Exact runs, negative cases, and remaining cryptographic/schema/measurement limitations are recorded in `POWERS_ENERGY_VALIDATION.md`.
