# Receipts

A receipt is a durable, attributed record of one action and the inputs that were knowable when it was decided.

It is **not** a cryptographically signed attestation, and it carries no signature or inclusion proof. Describing it
in that language would be an overclaim.

## What a receipt carries

```json
{
  "idempotency_key": "your-key",
  "receipt_id": "rcpt_...",
  "decision": "ALLOW",
  "reasons": ["within scope action.propose", "evidence reference present"],
  "evidence_ref": "doc:contract-4471#p12",
  "observed_outcome": "quote issued",
  "billed": true,
  "replay": "/v1/atlas/actions/your-key/replay"
}
```

## A denial is a receipt, not an error

An action refused for being outside its scope returns **HTTP 403 with the same shape above**, `decision: "DENY"`,
and `reasons` explaining the refusal. It is metered like any other accountable action.

This is deliberate. A prevented unauthorised action is the system doing its job, and the fact that it was
prevented is exactly the thing you will want evidence of later.

## Retry semantics

`Idempotency-Key` is **required**. Without it, a retry after a network failure could be billed twice — so the
service refuses the request rather than guessing your intent.

A repeated key returns the existing receipt with `billed: false`. A key already used by another organisation
returns `409`: keys are global across all organisations today, so generate keys that are unique across everyone
(for example a random UUID) rather than sequential business identifiers.

## Reads are free

`GET` on a receipt or a replay is never charged. Inspecting your own accountability record should not create a
financial reason to inspect less of it.

## The record outlives the credential

Revoking a credential stops it working on the very next request. It does not remove the receipts of what that
credential did while it was valid. Terminating a customer does not either.
