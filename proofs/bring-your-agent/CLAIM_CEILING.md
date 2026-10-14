# Claim ceiling

## Observed in this synthetic demo

- Bounded synthetic identity, workspace, credential and scopes.
- `action.propose` returned `ALLOW`; a real receipt and one usage event were retained.
- The exact retry returned the same receipt without a second charge.
- `evidence.export_source` returned `DENY` / `403` because it was outside credential scope.
- Distinct ALLOW and DENY receipts were read without an additional charge.
- Replay returned `FORENSIC_RECONSTRUCTION`; a later entitlement change was named without rewriting the historical decision.
- Revocation refused the next call; teardown left zero live credentials and entitlements while retaining two receipts.

## Not claimed

- Customer or external-participant proof.
- External business-action execution.
- H.I.F. recomputation or Vantage runtime.
- Evidence Check → Accountability automatic integration.
- Compliance, certification, universal behavior or general availability.
- Replay as model/action re-execution.
