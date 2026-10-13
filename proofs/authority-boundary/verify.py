#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


manifest = load("manifest.json")
for entry in manifest["files"]:
    payload = (ROOT / entry["path"]).read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    assert actual == entry["sha256"], f"hash mismatch: {entry['path']}"

request = load("request.json")
policy = load("authority-policy.json")
result = load("result.json")
audit = load("actuator-audit.json")
target = load("target-state.json")
escalation = load("escalation-receipt.json")

assert request["requested_amount_usd"] > policy["maximum_amount_usd"]
assert policy["over_limit_decision"] == "REFUSE"
assert policy["automatic_override_permitted"] is False
assert result["assessment"]["recommended_action"] == "REFUSE"
assert result["assessment"]["critical_gate_reasons"] == ["AUTHORIZATION_INVALID"]
assert result["actuator_invocations"] == 0
assert result["external_target_mutations"] == 0
assert result["target_unchanged"] is True
assert audit["actuator_invocations"] == 0
assert audit["before_sha256"] == audit["after_sha256"]
assert target["balance_delta_usd"] == 0
assert target["mutation_count"] == 0
assert escalation["reason"] == "REQUEST_EXCEEDS_ADMITTED_AUTHORITY"
assert escalation["pre_resolution_execution"] is False

print("AUTHORITY_BOUNDARY_PROOF: PASS")
print("- request exceeded admitted authority")
print("- decision was REFUSE")
print("- recorded actuator invocations and target mutations were zero")
print("- observed sandbox target hash was unchanged")
print("- escalation receipt is present")
