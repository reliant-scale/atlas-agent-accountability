#!/usr/bin/env bash
# The four Atlas operations. Every status code below is one the live service returns.
#
# Credentials are issued by Reliant Scale with the customer; nothing here creates one.
set -euo pipefail

: "${ATLAS_TOKEN:?export ATLAS_TOKEN with your scoped credential}"
: "${ATLAS_WORKSPACE:?export ATLAS_WORKSPACE with your workspace id}"
BASE="${ATLAS_BASE:-https://api.reliantscale.com}"

# A stable key per logical action. Reuse it on retry — that is the point of it.
KEY="act-$(date -u +%Y%m%dT%H%M%S)-$RANDOM"

echo "== 1. submit an accountable action"
# 200 = allowed, 403 = denied WITH A FULL RECEIPT. A denial is accountable work, not an error.
curl -sS -X POST "$BASE/v1/atlas/actions" \
  -H "Authorization: Bearer $ATLAS_TOKEN" \
  -H "Idempotency-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"action.propose\",
       \"workspace_id\":\"$ATLAS_WORKSPACE\",
       \"evidence_ref\":\"doc:example#p1\",
       \"observed_outcome\":\"quote issued\"}" \
  -w '\n  status %{http_code}\n'

echo "== 2. retry the SAME key — same receipt, billed:false, never charged twice"
curl -sS -X POST "$BASE/v1/atlas/actions" \
  -H "Authorization: Bearer $ATLAS_TOKEN" \
  -H "Idempotency-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"action.propose\",\"workspace_id\":\"$ATLAS_WORKSPACE\"}" \
  -w '\n  status %{http_code}\n'

echo "== 3. read the receipt (reads are never charged)"
curl -sS "$BASE/v1/atlas/actions/$KEY" \
  -H "Authorization: Bearer $ATLAS_TOKEN" -w '\n  status %{http_code}\n'

echo "== 4. replay — what was knowable then, and what changed since"
curl -sS "$BASE/v1/atlas/actions/$KEY/replay" \
  -H "Authorization: Bearer $ATLAS_TOKEN" -w '\n  status %{http_code}\n'

echo "== 5. what may this credential do? (scopes are an upper bound, not a grant)"
curl -sS "$BASE/v1/atlas/whoami" \
  -H "Authorization: Bearer $ATLAS_TOKEN" -w '\n  status %{http_code}\n'
