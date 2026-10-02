#!/usr/bin/env python3
"""A minimal Atlas client. Standard library only — no dependency should stand between you and evaluating this.

    export ATLAS_TOKEN=...  ATLAS_WORKSPACE=...
    python3 atlas_client.py
"""
from __future__ import annotations

import json
import os
import uuid
import urllib.error
import urllib.request

BASE = os.environ.get("ATLAS_BASE", "https://api.reliantscale.com")


class Atlas:
    def __init__(self, token: str, workspace_id: str, base: str = BASE):
        self.token, self.workspace_id, self.base = token, workspace_id, base

    def _call(self, method: str, path: str, body: dict | None = None,
              idempotency_key: str | None = None) -> tuple[int, dict]:
        headers = {"Authorization": f"Bearer {self.token}"}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        data = None
        if body is not None:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(f"{self.base}{path}", data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            # 403 is NOT an error here — it is a denial carrying a full receipt, and the denial is the
            # accountable event. Treat it as data.
            return e.code, json.loads(e.read() or b"{}")

    def submit(self, action: str, idempotency_key: str, **fields) -> tuple[int, dict]:
        """Submit an accountable action. The idempotency key is required: without it a retry could be billed
        twice, so the service refuses rather than guessing."""
        body = {"action": action, "workspace_id": self.workspace_id, **fields}
        return self._call("POST", "/v1/atlas/actions", body, idempotency_key)

    def receipt(self, key: str) -> tuple[int, dict]:
        """Read the receipt. Never charged. 404 across a tenant boundary, so existence is not confirmed."""
        return self._call("GET", f"/v1/atlas/actions/{key}")

    def replay(self, key: str) -> tuple[int, dict]:
        """Forensic reconstruction of the decision-time envelope. Not model re-execution."""
        return self._call("GET", f"/v1/atlas/actions/{key}/replay")

    def whoami(self) -> tuple[int, dict]:
        """Scopes are an upper bound on what may be attempted, never a grant."""
        return self._call("GET", "/v1/atlas/whoami")


if __name__ == "__main__":
    token = os.environ.get("ATLAS_TOKEN")
    workspace = os.environ.get("ATLAS_WORKSPACE")
    if not token or not workspace:
        raise SystemExit("set ATLAS_TOKEN and ATLAS_WORKSPACE")

    atlas = Atlas(token, workspace)
    key = "act-" + uuid.uuid4().hex   # idempotency keys are global across organisations: make them unique

    status, receipt = atlas.submit("action.propose", key,
                                   evidence_ref="doc:example#p1", observed_outcome="quote issued")
    print(f"submit   {status}  decision={receipt.get('decision')}  billed={receipt.get('billed')}")

    status, again = atlas.submit("action.propose", key)
    print(f"retry    {status}  billed={again.get('billed')}  <- same receipt, not charged twice")

    status, r = atlas.replay(key)
    print(f"replay   {status}  class={r.get('replay_class')}  changed_since={r.get('changed_since')}")

    status, who = atlas.whoami()
    print(f"whoami   {status}  scopes={who.get('scopes')}")
