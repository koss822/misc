#!/usr/bin/env python3
"""
claude-k8s-assistant — Natural-language Kubernetes troubleshooting powered by Claude.

Usage:
    python assistant.py "Why are my pods crashlooping in namespace prod?"
    python assistant.py "Check overall cluster health"
    python assistant.py "What's wrong with deployment nginx?" --namespace prod
    python assistant.py "Check node status" --dry-run
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass

import anthropic

MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are an expert Kubernetes SRE. You receive kubectl command outputs
and answer the user's question with a clear diagnosis and concrete remediation steps.
Be concise. Use Markdown. If you need more information, say what command would help."""

# Diagnostic commands run automatically based on keywords in the question
DIAGNOSTIC_COMMANDS = [
    ("nodes",        ["kubectl", "get", "nodes", "-o", "wide"]),
    ("pods",         ["kubectl", "get", "pods", "--all-namespaces", "--field-selector=status.phase!=Running"]),
    ("events",       ["kubectl", "get", "events", "--all-namespaces", "--sort-by=.lastTimestamp", "--field-selector=type=Warning"]),
    ("top_nodes",    ["kubectl", "top", "nodes"]),
    ("top_pods",     ["kubectl", "top", "pods", "--all-namespaces"]),
]

KEYWORD_MAP = {
    "crash": ["pods", "events"],
    "loop":  ["pods", "events"],
    "oom":   ["pods", "events", "top_pods"],
    "node":  ["nodes", "top_nodes"],
    "memory": ["top_pods", "top_nodes"],
    "cpu":   ["top_pods", "top_nodes"],
    "pending": ["pods", "events", "nodes"],
    "health": ["nodes", "pods", "events"],
    "deploy": ["pods", "events"],
}


@dataclass
class CommandResult:
    name: str
    command: str
    output: str
    error: bool


def run_kubectl(name: str, cmd: list[str], namespace: str | None = None) -> CommandResult:
    full_cmd = cmd[:]
    if namespace and "--all-namespaces" not in cmd:
        full_cmd += ["-n", namespace]
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=15)
        output = result.stdout or result.stderr
        return CommandResult(name, " ".join(full_cmd), output.strip(), result.returncode != 0)
    except FileNotFoundError:
        return CommandResult(name, " ".join(full_cmd), "[kubectl not found in PATH]", True)
    except subprocess.TimeoutExpired:
        return CommandResult(name, " ".join(full_cmd), "[command timed out after 15s]", True)


def select_commands(question: str) -> list[tuple[str, list[str]]]:
    q = question.lower()
    selected_names = set()
    for keyword, names in KEYWORD_MAP.items():
        if keyword in q:
            selected_names.update(names)
    if not selected_names:
        selected_names = {"pods", "events", "nodes"}
    cmd_map = dict(DIAGNOSTIC_COMMANDS)
    return [(name, cmd_map[name]) for name in selected_names if name in cmd_map]


DRY_RUN_OUTPUTS = {
    "nodes":     "NAME       STATUS   ROLES           AGE   VERSION\nnode-1     Ready    control-plane   30d   v1.28.0\nnode-2     Ready    worker          30d   v1.28.0",
    "pods":      "NAMESPACE   NAME              READY   STATUS             RESTARTS   AGE\nprod        api-7d9f-xkp2n   0/1     CrashLoopBackOff   14         2h",
    "events":    "NAMESPACE   LAST SEEN   TYPE      REASON    MESSAGE\nprod        2m          Warning   BackOff   Back-off restarting failed container api",
    "top_nodes": "NAME       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%\nnode-1     850m         21%    3Gi             48%",
    "top_pods":  "NAMESPACE   NAME              CPU(cores)   MEMORY(bytes)\nprod        api-7d9f-xkp2n   0m           0Mi",
}


def build_context(results: list[CommandResult]) -> str:
    parts = []
    for r in results:
        status = "ERROR" if r.error else "OK"
        parts.append(f"### `{r.command}` [{status}]\n```\n{r.output}\n```")
    return "\n\n".join(parts)


def ask_claude(question: str, context: str) -> str:
    client = anthropic.Anthropic()
    prompt = f"User question: {question}\n\nKubectl outputs:\n\n{context}"
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def main():
    parser = argparse.ArgumentParser(description="Natural-language Kubernetes troubleshooting with Claude")
    parser.add_argument("question", help="Your question about the cluster")
    parser.add_argument("--namespace", "-n", help="Kubernetes namespace to focus on")
    parser.add_argument("--dry-run", action="store_true", help="Use fixture kubectl output, skip real commands and API call")
    args = parser.parse_args()

    commands = select_commands(args.question)
    print(f"[*] Running {len(commands)} diagnostic command(s)...", file=sys.stderr)

    results = []
    for name, cmd in commands:
        if args.dry_run:
            results.append(CommandResult(name, " ".join(cmd), DRY_RUN_OUTPUTS.get(name, "[dry-run fixture]"), False))
        else:
            r = run_kubectl(name, cmd, args.namespace)
            results.append(r)
            status = "ERROR" if r.error else "OK"
            print(f"  [{status}] {r.command}", file=sys.stderr)

    context = build_context(results)

    if args.dry_run:
        print("\n[dry-run] Fixture kubectl outputs collected. Skipping Claude API call.\n")
        print(context)
        return

    print("[*] Asking Claude...\n", file=sys.stderr)
    answer = ask_claude(args.question, context)
    print(answer)


if __name__ == "__main__":
    main()
