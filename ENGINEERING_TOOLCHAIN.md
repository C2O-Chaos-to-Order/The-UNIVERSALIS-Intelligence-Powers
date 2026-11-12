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
