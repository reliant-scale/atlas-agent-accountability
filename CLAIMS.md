# What we will and will not say

Atlas is accountability infrastructure. The value of that depends entirely on our own accounts being accurate, so
this file states the boundary publicly and holds us to it.

## Will not be claimed

| Claim | Why not |
|---|---|
| verified · certified · attested | Accountability receipts are durable attributed records, not cryptographically signed attestations. Those words would describe a different object. |
| immutable · tamper-proof | Not a property we have qualified for this path. |
| Merkle or inclusion proof in the receipt | The receipt returns no such field. |
| zero PII | A consequential-action payload may carry whatever the customer sends. |
| compliant with any regulation | A legal conclusion we have not qualified and cannot make. |
| SOC 2 · ISO 27001 · HIPAA · FedRAMP | We hold none of these. |
| any SLA or uptime figure | Never measured. Stating one would be inventing it. |
| deterministic replay of model cognition | Replay is forensic reconstruction. It does not re-execute a model. |
| Docker-native · Kubernetes-native | Production is a hardened Linux service under systemd. OCI packaging with Podman is under qualification. |
| generally available | Controlled enterprise engagements only. |

## Will be claimed, because it is demonstrable on request

- four operations live and failing closed without a credential
- scoped credentials, revocation effective on the very next request
- accountability records outliving the credential and termination
- receipts, retry-safe metering by idempotency key, free reads
- forensic replay that names what changed since, and says so when nothing has
- tenant isolation that does not confirm existence across a boundary
- a governed customer creation protocol that is payment-gated, atomic, idempotent and attributed
- proven recovery: encrypted off-host retention and a scheduled restore rehearsal

## Why publish this

A claims ceiling that lives only in internal documents is a discipline control, not a real one. We learned that
the hard way: our own public product page declared for five days that its ceiling was "asserted by" a verifier
that had never been written.

If you find a claim in this repository that the service does not honour, open an issue. That is a defect.
