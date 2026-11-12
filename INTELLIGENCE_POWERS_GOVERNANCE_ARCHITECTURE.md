# Intelligence Powers Governance Toolchain — UNIVERSALIS

**Owner:** The UNIVERSALIS Intelligence Powers repository  
**Boundary:** Public, open, inspectable, independently operated  
**Status:** Portable contract foundation; external runtime integrations remain candidates  
**Taxonomy:** Existing `Intelligence_Powers.md` I-P-01–I-P-12 remains canonical and unchanged

## Architectural position

Enforcement is an external deterministic boundary around an agent. Models and agents may propose intent or risk assessments; a separately operated policy decision point (PDP) and policy enforcement point (PEP) decide and enforce the result. A capability is not authority, a policy decision is not proof of execution, and a reputation score is not permission.

## Open candidate inventory

### Runtime governance and reference monitors
OpenShell; ActShield; Sponsio; AgentSentrix; agentpolicy; Aethelgard. OpenShell is an external runtime/reference monitor. Cedar is a formally analyzable policy-language choice; OPA/Rego remains a peer backend. Unknown tools, malformed policies, PDP timeouts, missing context and verifier failures must fail closed.

### Audit, provenance and trust
AgentOps Replay; auditant; omega-audit; halo-record; IETF Agent Audit Trail draft; SwarmScore; ClankerScore. Hash-chained records should preserve causal stages (INTENDED, REQUESTED, EVALUATED, ALLOWED, ATTEMPTED, EXECUTED, BLOCKED, REVOKED). SwarmScore is an individual Internet-Draft, not an IETF-approved standard. Reputation is a routing signal, never an authority grant.

### Sandbox isolation
Google Agent Substrate / Agent Sandbox; Akamai Agent Sandbox; Edera; gVisor. Treat isolation type as a declared property backed by evidence, not by a vendor label. WASM, microVMs, gVisor, containers, kernel reference monitors and hardware watchdogs are distinct mechanisms.

### Governance measurement and interoperability
Agentic Governance Benchmark (AGB) proposal; OpenID AuthZEN Authorization API 1.0. AGB dimensions: policy determinism, enforcement latency, receipt provenance, scope containment, jurisdictional enforcement and override integrity. The score record accepts 0–100 per dimension but does not invent maturity-tier bands absent a published rubric. AuthZEN provides a vendor-neutral PDP/PEP API surface; it does not prescribe a policy language or policy store.

All other project names, advertised features, tool counts and performance figures remain owner-supplied candidates or claims pending canonical source, licensing, maintenance, security, compatibility and independent reproduction.

## Portable shared contracts

The shared schema family defines policy-language metadata, AuthZEN-compatible authorization request/response shapes, signed enforcement-receipt metadata, hash-chained audit records, runtime sandbox attestations, six-dimension governance benchmark results, reputation evidence signals, and attenuable/expiring capability-grant metadata.

The contracts are registry-neutral and do not create a central enforcement authority. They contain no private C2O policy, signing key, authority token, private decision, or private enforcement trace.

## Policy and enforcement semantics

- Deny by default. Unknown principal/action/resource, expired policy, parser error, PDP timeout, missing evidence or verifier error is not an allow.
- Interception must occur before the protected tool/action is dispatched.
- Delegated authority is monotonic: child grants are subsets of parent grants; delegation never amplifies.
- Untrusted context is labelled and cannot flow to sensitive sinks without an explicit sanitizer decision and evidence receipt.
- Advisory model output can recommend review but cannot override deterministic policy.
- Human-in-the-loop outcomes suspend execution; they do not imply approval.
- Quarantine, block, revoke, rate-limit and redact remain distinct outcomes.
- Log explicit causal events; never expose private reasoning or raw secret values.
- Hash-chain verification detects modification; independent custody and anchoring provide stronger tamper evidence.

## Governance benchmark discipline

Each dimension is scored against a versioned rubric, protocol, evidence set and observation window. Overall score must be derived from all six scores under the referenced rubric. Tier names and bands remain rubric-defined. Scores do not certify compliance or establish legal conclusions.

## Current implementation and limits

The companion shared schemas, fixtures and semantic validator provide basic contract coverage on this branch. They do not deploy OpenShell, a Cedar engine, PDP/PEP, ActShield, Sponsio, AgentSentrix, auditant, AgentOps Replay, sandbox runtime, reputation network or AGB assessor. Fixture signatures are synthetic and not cryptographically verified. No external candidate is marked integrated.

## Current source verification

- OpenShell joined CNCF Sandbox on 2026-11-10: https://www.cncf.io/blog/2026/11/10/welcoming-openshell-to-the-cncf-open-governance-to-secure-agentic-ai/
- Cedar CNCF Sandbox profile and formal-methods notes: https://www.cncf.io/projects/cedar/
- AuthZEN Authorization API 1.0 final specification: https://openid.net/authorization-api-1-0-final-specification-approved/
- SwarmScore individual Internet-Draft: https://datatracker.ietf.org/doc/draft-stone-swarmscore-v1/
- Google Agent Substrate / gVisor CNCF announcement: https://cloud.google.com/blog/products/containers-kubernetes/open-infrastructure-for-autonomous-agents-comes-to-cncf/
- Akamai Agent Sandbox: https://www.akamai.com/products/akamai-agent-sandbox
- Edera Agent Sandbox microVM pattern: https://docs.edera.dev/guides/deployment/agent-sandbox/
