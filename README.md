# Reliant Scale Atlas — Agent Accountability

**Know what your agents did, what they relied on, what they were allowed to do, and what happened afterward.**

Atlas records consequential agent activity and makes it accountable after the fact. Four operations, a scoped
bearer credential, durable receipts, and forensic reconstruction of the decision-time envelope.

The machine-readable contract is [`openapi.yaml`](./openapi.yaml), also served live at
[reliantscale.com/atlas-openapi.yaml](https://reliantscale.com/atlas-openapi.yaml).

---

## Bring your agent

Atlas gives an application or an AI agent a governed place to record consequential work — and gives you a
reconstructable account of it afterwards. Your agent stays the actor; it never becomes the authority over your
business state.

```
your agent ──► POST /v1/atlas/actions ──► receipt (who · on what evidence · under what authority · outcome)
                                              │
                         later, anyone ◄──────┘  GET …/replay  →  the decision-time envelope, and what changed since
```

| Step | What happens |
|---|---|
| 1. Read the contract | [`openapi.yaml`](./openapi.yaml), [`docs/`](./docs), and the [curl](./examples/curl/four-operations.sh) and [Python](./examples/python/atlas_client.py) examples. No credential needed to evaluate. |
| 2. Get a credential | Today, credentials are opened with Reliant Scale — see [Getting access](#getting-access). Self-serve developer access is being built and is **not available yet**. |
| 3. Send one action | One `POST` with an `Idempotency-Key`. You get a receipt, even when the action is refused. |
| 4. Read it back | `GET` the receipt and its replay. Reads are never charged. |

**Status, plainly:** the four REST operations below are live in production as a **qualified controlled-pilot
API**. Thin MCP and A2A adapters over the same four operations are in qualification; neither is available yet,
and this README will link them when they are.

---

## The problem this exists for

A single agent is traceable. A fleet of agents calling each other — reusing service identities, spanning systems,
running for hours — produces a causal chain with no single operator who watched it happen.

Application logs record what executed. They rarely record **which principal held which authority, on what
evidence, at that moment**, because nobody needed that until the actor stopped being a person.

So when someone asks about one decision six months later, the answer is archaeology.

Pick a decision an agent made last week that affected a customer, and try to answer four questions about it:

| | |
|---|---|
| **Which actor decided?** | Not which service — which principal, holding which credential, under what scope. |
| **What did it rely on?** | The evidence available *at decision time*, not what that source says today. |
| **Was it allowed to?** | The authority evaluation, recorded as part of the action. |
| **What happened next?** | The observed outcome, and what has changed since. |

Most organisations can answer the first and the last.

---

## The four operations

```
POST /v1/atlas/actions              submit an accountable action
GET  /v1/atlas/actions/{key}        read the receipt
GET  /v1/atlas/actions/{key}/replay replay the decision-time envelope
GET  /v1/atlas/whoami               ask what a credential may do
```

That is the whole contract. The surface is small deliberately: a service holding other organisations'
accountability records should not have a large attack surface.

---

## Behaviour worth checking

These matter mainly when something has already gone wrong, which is exactly when you find out whether they were
implemented.

**Revocation takes effect on the very next request.** There is no session and no cache. Every request re-reads the
credential's state, so a revoked key stops working immediately rather than at the end of a token lifetime.

**A denial is accountable work.** An action refused for being outside its scope returns `403` **with a full
receipt**, not an error — and it is metered. A prevented unauthorised action is the service doing its job.

**The record outlives the credential.** Receipts survive revocation and termination. Revoking access never erases
the account of what was done.

**Retrying is safe and is not billed twice.** `Idempotency-Key` is required, not optional — without it a retry
could be billed twice, so the service refuses rather than guessing. The same key returns the same receipt.

**Reads are never charged.** Inspecting your own record must not create a reason to inspect less of it.

**Reads do not confirm existence across a tenant boundary.** Reading a receipt or replay that belongs to another
organisation returns `404`, not `403`. An unknown credential and a revoked credential are refused identically, so
neither teaches an attacker which keys once existed.

**Idempotency keys are global today — use a UUID.** An `Idempotency-Key` already used by another organisation is
refused with `409`. Generate keys that are unique across everyone (for example a random UUID), not sequential
business identifiers such as `order-1001`. Per-organisation key scoping is being worked on.

---

## Replay is forensic reconstruction, not re-execution

Replay reconstructs the stored envelope around a decision: the evidence reference, the authority evaluation, the
outcome, the principal that acted, and what has changed since.

It does **not** re-execute a model, and it cannot tell you what a model would output today.

The response carries `replay_class: FORENSIC_RECONSTRUCTION`. The classification is in the payload rather than in
the documentation, so an integrator cannot mistake what is being offered — and neither can we.

Where nothing has changed, replay says so. "No later change has been admitted" is a finding, not an absence of
one.

---

## What this is not

Honest boundaries, because a technical reviewer rewards what you can show rather than what you can describe:

- **One contract.** The native Atlas contract is the four REST operations above. Adapters in qualification
  (MCP, A2A) are thin projections onto those same operations: they will not mint credentials, create customer
  state, alter receipts, or widen authority beyond the presented Atlas credential. Neither is served today.
- **Not gRPC, not GraphQL, not OAuth2, not JWT.** REST over HTTPS with a scoped revocable bearer credential,
  stored as a hash and re-read on every request.
- **The receipt contract is exactly what is documented here.** It carries the fields in
  [`schemas/receipt.json`](./schemas/receipt.json) and nothing further — no cryptographic inclusion proof, no
  external anchor, no attestation token. If a field is not in that schema, the service does not return it.
- **No zero-PII claim.** A consequential-action payload may carry whatever the customer sends.
- **Not a compliance certification.** Atlas is accountability infrastructure that can *support* oversight, audit,
  examination and incident work. It does not place any organisation in conformance with any regulation, and no
  output here is assurance.
- **Controlled access only.** Atlas runs today as a hardened Linux service under systemd. There is no public
  signup and no self-service credential; access is opened with the customer.

---

## Getting access

Credentials are issued by Reliant Scale with the customer. This repository exists so your engineers can evaluate
the interface **before** anyone talks to sales.

- Integration surface: <https://reliantscale.com/atlas/integrate>
- Agent accountability: <https://reliantscale.com/atlas/agent-accountability>
- Replay: <https://reliantscale.com/atlas/replay>
- Self-guided Agent Accountability Quickstart ($36): <https://reliantscale.com/products/agent-accountability-quickstart>
- partnerships@reliantscale.com

---

## Licence and trademarks

The code, examples and schemas in this repository are released under the [MIT licence](./LICENSE). The Atlas
service itself is proprietary and is not part of this repository. Reliant Scale, Atlas and 1V names and marks are
not licensed — see [TRADEMARKS.md](./TRADEMARKS.md).

---

## Repository contents

```
openapi.yaml          the contract, written from the deployed service
docs/                 receipts, replay, credentials, errors
examples/curl/        the four operations as shell
examples/python/      a minimal client
schemas/              receipt and replay JSON Schema
CLAIMS.md             what we will and will not say, and why
SECURITY.md           how to report a vulnerability
LICENSE · TRADEMARKS.md
```

Issues and questions are welcome. If you find a claim here that the service does not honour, that is a defect and
we want it reported.

© Reliant Scale Technologies. Atlas is a managed accountability service. *Powered by 1V.*
