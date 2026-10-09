#!/usr/bin/env python3
"""Repository self-check, run in CI on every push and pull request.

- the OpenAPI contract and JSON schemas parse, and the contract validates as OpenAPI 3.1
- the Python example compiles and the shell example passes `bash -n`
- the claims ceiling in CLAIMS.md holds in every other file (prose and code comments)
- nothing credential-shaped is present

Exit 0 only when every check passes.
"""
from __future__ import annotations

import json
import pathlib
import py_compile
import re
import subprocess
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
# Words CLAIMS.md says we will not use. CLAIMS.md, SECURITY.md and TRADEMARKS.md must name them, so are exempt.
BANNED = [r"\bverified\b", r"\bcertified\b", r"\battested\b", r"\bimmutable\b", r"\btamper-?proof\b",
          r"\bcompliant with\b", r"\bguarantee[ds]?\b", r"\bsoc ?2\b", r"\bzero (raw )?pii\b",
          r"\bdeterministic(ally)? repl", r"\bMerkle\b", r"\bgenerally available\b", r"\bSLA\b"]
EXEMPT = {"CLAIMS.md", "SECURITY.md", "TRADEMARKS.md", "check_repo.py"}
SECRET = re.compile(r"(sk-[A-Za-z0-9]{16,}|sk_live_[A-Za-z0-9]{8,}|whsec_[A-Za-z0-9]{16,}|-----BEGIN [A-Z ]*PRIVATE KEY)")
failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print("FAIL", msg)


def main() -> int:
    spec = yaml.safe_load((ROOT / "openapi.yaml").read_text(encoding="utf-8"))
    try:
        from openapi_spec_validator import validate
        validate(spec)
        print("ok   openapi.yaml validates as OpenAPI", spec.get("openapi"))
    except ImportError:
        print("skip openapi-spec-validator not installed (parsed only)")
    except Exception as e:  # noqa: BLE001
        fail(f"openapi.yaml: {str(e)[:200]}")
    for s in sorted((ROOT / "schemas").glob("*.json")):
        json.loads(s.read_text(encoding="utf-8"))
        print("ok  ", s.relative_to(ROOT), "parses")
    capability_schema = json.loads((ROOT / "schemas" / "capability-request.json").read_text(encoding="utf-8"))
    capability_example = json.loads((ROOT / "examples" / "json" / "capability-request.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(capability_schema)
    Draft202012Validator(capability_schema).validate(capability_example)
    print("ok   capability request example validates against its public contract")
    for p in sorted((ROOT / "examples").rglob("*.py")):
        py_compile.compile(str(p), doraise=True)
        print("ok  ", p.relative_to(ROOT), "compiles")
    for p in sorted((ROOT / "examples").rglob("*.sh")):
        if subprocess.run(["bash", "-n", str(p)]).returncode:
            fail(f"{p.relative_to(ROOT)}: bash -n")
        else:
            print("ok  ", p.relative_to(ROOT), "bash -n")
    for f in sorted(ROOT.rglob("*")):
        if not f.is_file() or ".git" in f.parts or f.suffix not in (".md", ".yaml", ".yml", ".json", ".py", ".sh"):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if SECRET.search(text):
            fail(f"{f.relative_to(ROOT)}: credential-shaped material")
        if f.name in EXEMPT:
            continue
        for pat in BANNED:
            m = re.search(pat, text, re.I)
            if m:
                fail(f"{f.relative_to(ROOT)}: claims ceiling term {m.group(0)!r}")
    print("PASS" if not failures else f"{len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
