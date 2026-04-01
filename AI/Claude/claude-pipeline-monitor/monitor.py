#!/usr/bin/env python3
"""
claude-pipeline-monitor — Diagnose CI/CD pipeline failures using Claude API.

Usage:
    python monitor.py --log pipeline.log
    python monitor.py --log pipeline.log --output report.json
    python monitor.py --log pipeline.log --dry-run
"""

import argparse
import json
import sys
import re
from datetime import datetime
from pathlib import Path

import anthropic

MODEL = "claude-sonnet-4-6"
MAX_LOG_CHARS = 12000

SYSTEM_PROMPT = """You are a CI/CD expert. Analyze pipeline failure logs and return a JSON object.
Always respond with valid JSON only — no markdown fences, no extra text."""

DIAGNOSE_PROMPT = """Analyze this pipeline failure log and return a JSON object with exactly these fields:
- "root_cause": string, one sentence describing the primary failure
- "failed_step": string, name of the step or job that failed
- "fix_suggestion": string, concrete actionable fix
- "severity": one of "LOW", "MEDIUM", "HIGH", "CRITICAL"
- "error_lines": array of strings, the most relevant error lines (max 5)
- "affected_files": array of strings, source files mentioned near the failure (max 5)

Pipeline log:
{log}"""


SEVERITY_COLORS = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "red", "CRITICAL": "red"}

DRY_RUN_REPORT = {
    "root_cause": "[dry-run] Fixture output — no real analysis performed.",
    "failed_step": "build",
    "fix_suggestion": "Set ANTHROPIC_API_KEY and run without --dry-run.",
    "severity": "LOW",
    "error_lines": [],
    "affected_files": [],
}


def truncate_log(log: str, max_chars: int) -> str:
    if len(log) <= max_chars:
        return log
    half = max_chars // 2
    return log[:half] + "\n\n[... truncated ...]\n\n" + log[-half:]


def parse_report(raw: str) -> dict:
    # Strip any accidental markdown fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw.strip(), flags=re.MULTILINE)
    return json.loads(raw)


def diagnose(log_text: str, dry_run: bool = False) -> dict:
    if dry_run:
        print("[dry-run] Skipping API call.", file=sys.stderr)
        return DRY_RUN_REPORT

    truncated = truncate_log(log_text, MAX_LOG_CHARS)
    client = anthropic.Anthropic()
    print(f"[*] Sending {len(truncated)} chars to Claude...", file=sys.stderr)

    message = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": DIAGNOSE_PROMPT.format(log=truncated)}],
    )
    raw = message.content[0].text
    try:
        return parse_report(raw)
    except json.JSONDecodeError as e:
        print(f"[!] Claude returned invalid JSON: {e}\nRaw: {raw[:200]}", file=sys.stderr)
        return {"root_cause": raw, "severity": "UNKNOWN", "error": str(e)}


def print_summary(report: dict) -> None:
    severity = report.get("severity", "?")
    print(f"\n{'='*50}")
    print(f"  SEVERITY   : {severity}")
    print(f"  FAILED STEP: {report.get('failed_step', '?')}")
    print(f"  ROOT CAUSE : {report.get('root_cause', '?')}")
    print(f"  FIX        : {report.get('fix_suggestion', '?')}")
    if report.get("error_lines"):
        print("  TOP ERRORS :")
        for line in report["error_lines"]:
            print(f"    » {line}")
    print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(description="Diagnose CI/CD pipeline failures with Claude")
    parser.add_argument("--log", required=True, metavar="FILE", help="Pipeline log file")
    parser.add_argument("--output", default="report.json", metavar="FILE", help="Output JSON report (default: report.json)")
    parser.add_argument("--dry-run", action="store_true", help="Skip API call, return fixture output")
    args = parser.parse_args()

    log_path = Path(args.log)
    if not log_path.exists():
        print(f"Error: file not found: {log_path}", file=sys.stderr)
        sys.exit(1)

    log_text = log_path.read_text(errors="replace")
    report = diagnose(log_text, dry_run=args.dry_run)

    report["_meta"] = {
        "analyzed_at": datetime.utcnow().isoformat() + "Z",
        "model": MODEL,
        "log_file": str(log_path),
        "dry_run": args.dry_run,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(report, indent=2))
    print(f"[+] Report written to {output_path}", file=sys.stderr)
    print_summary(report)

    # Exit 1 on HIGH/CRITICAL so CI can pick it up
    if report.get("severity") in ("HIGH", "CRITICAL"):
        sys.exit(1)


if __name__ == "__main__":
    main()
