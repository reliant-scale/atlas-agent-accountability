# Replay

Most systems tell you what happened. Replay answers a different question: **what was knowable at the time**.

Only the second one defends a decision.

## What it returns

```json
{
  "idempotency_key": "intake-4471-approve",
  "decision": "ALLOW",
  "decided_at": "2026-09-14 09:22:41+00",
  "knowable_at_the_time": {
    "credential_scopes_at_decision": ["action.propose", "drill.read"],
    "credential_state_at_decision": "ACTIVE",
    "role_capabilities_at_decision": [],
    "organization_at_decision": "org_…",
    "entitlement_capabilities_at_decision": ["action.propose", "drill.read"],
    "evidence_ref_supplied": "doc:contract-4471#p12",
    "proposer_id": ""
  },
  "changed_since": [
    { "what": "workspace entitlement", "then": ["action.propose", "drill.read"], "now": ["drill.read"] }
  ],
  "replay_class": "FORENSIC_RECONSTRUCTION",
  "replay_class_note": "The decision-time envelope is reconstructed from the stored record. …",
  "statement": "State has changed since this decision was made. The decision is reported as it was, against what was knowable then, not re-decided against today.",
  "charged_for_this_read": false
}
```

## What `changed_since` compares

Today, replay compares three things against the stored envelope, and names each one that differs:

- the **credential's scopes**
- the **workspace entitlement** capabilities
- the **organization's status**

It does not track changes to the evidence itself: `evidence_ref_supplied` is reported exactly as it was given at
decision time.

## The boundary, stated in the payload

`replay_class` is `FORENSIC_RECONSTRUCTION` and it is in the response body rather than only in documentation.

Replay reconstructs the **stored envelope** around a decision. It does not re-execute a model and cannot tell you
what a model would produce today. If a vendor offers to replay a language model's cognition exactly as it ran,
ask them to demonstrate it on last quarter's data before believing it.

## Empty is an answer

When `changed_since` is empty, none of the compared state has changed since the decision. That is a finding
worth recording, not an absence of one.

## Why the envelope must be kept at decision time

Reconstructing it afterwards means joining logs never designed to be joined, against source systems that have
moved on. Sometimes possible. Never cheap, never complete, and always done under the pressure of the event that
made it necessary.

Decision time is the only moment the envelope is free.
