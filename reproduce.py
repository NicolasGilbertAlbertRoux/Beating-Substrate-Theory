#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"

def ordered_scripts(include_supplementary: bool = True) -> list[Path]:
    canonical = sorted(SCRIPTS.glob("stage*.py"))
    controls = sorted(SCRIPTS.glob("control_*.py"))
    supplementary = sorted(SCRIPTS.glob("supplementary_*.py")) if include_supplementary else []
    return canonical + controls + supplementary

def main() -> int:
    parser = argparse.ArgumentParser(description="Reproduce BST numerical stages and controls.")
    parser.add_argument("--quiet", action="store_true", help="Only print one line per script.")
    parser.add_argument("--timeout", type=float, default=60.0, help="Timeout per script in seconds.")
    parser.add_argument("--canonical-only", action="store_true", help="Run only canonical stage scripts.")
    args = parser.parse_args()

    scripts = sorted(SCRIPTS.glob("stage*.py")) if args.canonical_only else ordered_scripts(True)
    print(f"Beating Substrate Theory — reproducing {len(scripts)} script(s)")
    print("=" * 72)

    failures: list[tuple[str, str]] = []
    for script in scripts:
        t0 = time.time()
        try:
            proc = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(SCRIPTS),
                text=True,
                capture_output=True,
                timeout=args.timeout,
            )
            dt = time.time() - t0
            ok = proc.returncode == 0
            status = "PASS" if ok else f"FAIL({proc.returncode})"
            if args.quiet:
                print(f"[{status}] {script.name}  ({dt:.2f}s)")
            else:
                tail = ""
                output = (proc.stdout + "\n" + proc.stderr).strip().splitlines()
                if output:
                    tail = " | " + output[-1][:180]
                print(f"[{status}] {script.name}  ({dt:.2f}s){tail}")
            if not ok:
                failures.append((script.name, proc.stderr[-500:]))
        except subprocess.TimeoutExpired:
            print(f"[TIMEOUT] {script.name}  (>{args.timeout:.1f}s)")
            failures.append((script.name, "timeout"))

    print("=" * 72)
    if failures:
        print(f"{len(failures)}/{len(scripts)} script(s) failed.")
        return 1
    print(f"{len(scripts)}/{len(scripts)} script(s) ran cleanly.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
