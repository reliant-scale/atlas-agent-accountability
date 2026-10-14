# Sanitized event capture — `RST-BYA-DEMO-CEREMONY-20261014T191401Z`

This is an editorial event capture derived from the sealed machine receipt. It contains no raw credential and is not a screen recording.

| Beat | Observed event |
| --- | --- |
| Authority | One-run synthetic ceremony authority; publication and external admission held. |
| Identity | `agent/agt_003272aa388e` in synthetic workspace `ws_003272aa388e`; scopes `action.propose`, `drill.read`. |
| Permitted use | `action.propose` returned `ALLOW`; receipt `rcp_18693ca347f5443c`; billed once. |
| Idempotency | The exact same request returned the same receipt and was not billed again. |
| Prohibited use | `evidence.export_source` returned `DENY` / 403 because it was outside credential scope; receipt `rcp_3f390e4ecdb25668`. |
| Receipt read | Both reads were free and returned their original decisions. |
| Replay | `FORENSIC_RECONSTRUCTION`; decision-time scopes were visible; `changed_since` was initially empty. |
| Later change | Workspace entitlement narrowed from `action.propose, drill.read` to `drill.read`; Replay named that admitted change without changing the historical `ALLOW`. |
| Revocation | The next `whoami` returned 401: credential not recognised. |
| Teardown | Organization terminated; agent revoked; zero live credentials/entitlements; two receipts and two usage events retained. |

## Editorial inference

> Agents can consume capabilities. They cannot buy authority.

This inference is supported by the observed bounded ALLOW and same-identity out-of-scope DENY. It is not a universal theorem and does not imply customer use, external business mutation, H.I.F. recomputation, or general availability.
