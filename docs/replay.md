# Replay

Most systems tell you what happened. Replay answers a different question: **what was knowable at the time**.

Only the second one defends a decision.

## What it returns

```json
{
  "replay_class": "FORENSIC_RECONSTRUCTION",
  "decided_at": "2026-09-14T09:22:41Z",
  "knowable_at_decision_time": {
    "evidence_ref": "doc:contract-4471#p12",
    "scopes": ["action.propose", "evidence.view"],
    "principal_id": "agent_intake_03"
  },
  "changed_since": [
    "doc:contract-4471 was superseded 2026-09-19"
  ]
}
```

## The boundary, stated in the payload

`replay_class` is `FORENSIC_RECONSTRUCTION` and it is in the response body rather than only in documentation.

Replay reconstructs the **stored envelope** around a decision. It does not re-execute a model and cannot tell you
what a model would produce today. If a vendor offers to replay a language model's cognition exactly as it ran,
ask them to demonstrate it on last quarter's data before believing it.

## Empty is an answer

When `changed_since` is empty, nothing later has been admitted against that evidence. That is a finding worth
recording, not an absence of one.

## Why the envelope must be kept at decision time

Reconstructing it afterwards means joining logs never designed to be joined, against source systems that have
moved on. Sometimes possible. Never cheap, never complete, and always done under the pressure of the event that
made it necessary.

Decision time is the only moment the envelope is free.
