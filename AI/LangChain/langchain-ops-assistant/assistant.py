#!/usr/bin/env python3
"""
langchain-ops-assistant — ReAct agent for autonomous infrastructure incident investigation.

The agent has access to these tools:
  - kubectl_get     : run read-only kubectl commands
  - prometheus_query: execute PromQL queries
  - search_runbooks : keyword search over local Markdown runbooks

Usage:
    python assistant.py "Pods in namespace prod are crashlooping since 14:00"
    python assistant.py "High memory usage on node-3" --runbooks ./runbooks
    python assistant.py "Database pods not starting" --dry-run
"""

import argparse
import subprocess
import sys
import os
import re
from pathlib import Path

from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain import hub

MODEL = "claude-sonnet-4-6"
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
RUNBOOKS_DIR = None  # Set via --runbooks arg


# ── Tools ──────────────────────────────────────────────────────────────────────

@tool
def kubectl_get(resource_and_args: str) -> str:
    """Run a read-only kubectl command. Input: resource type and optional flags,
    e.g. 'pods -n prod', 'events --field-selector=type=Warning', 'nodes -o wide'.
    Only 'get', 'describe', 'logs' subcommands are allowed."""
    parts = resource_and_args.strip().split()
    # Safety: only allow read operations
    allowed = ("get", "describe", "logs", "top")
    if parts and parts[0] not in allowed:
        parts.insert(0, "get")
    cmd = ["kubectl"] + parts
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return (result.stdout or result.stderr).strip() or "(no output)"
    except FileNotFoundError:
        return "[kubectl not found — is it installed and in PATH?]"
    except subprocess.TimeoutExpired:
        return "[kubectl timed out after 15s]"


@tool
def prometheus_query(promql: str) -> str:
    """Execute a PromQL instant query against Prometheus.
    Input: a PromQL expression, e.g. 'container_memory_usage_bytes{namespace="prod"}'."""
    import urllib.request
    import urllib.parse
    import json
    url = f"{PROMETHEUS_URL}/api/v1/query?query={urllib.parse.quote(promql)}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
        results = data.get("data", {}).get("result", [])
        if not results:
            return "(no data)"
        lines = []
        for r in results[:10]:
            metric = r.get("metric", {})
            value = r.get("value", ["", ""])[1]
            lines.append(f"{metric} = {value}")
        return "\n".join(lines)
    except Exception as e:
        return f"[Prometheus error: {e}]"


@tool
def search_runbooks(keywords: str) -> str:
    """Search local Markdown runbooks for relevant sections.
    Input: space-separated keywords to search for."""
    if not RUNBOOKS_DIR or not Path(RUNBOOKS_DIR).is_dir():
        return "[No runbooks directory configured — pass --runbooks <dir>]"
    words = [w.lower() for w in keywords.split()]
    results = []
    for md_file in sorted(Path(RUNBOOKS_DIR).rglob("*.md")):
        text = md_file.read_text(errors="replace")
        if all(w in text.lower() for w in words):
            # Extract the most relevant paragraph
            for para in text.split("\n\n"):
                if all(w in para.lower() for w in words):
                    results.append(f"**{md_file.name}**:\n{para.strip()[:400]}")
                    break
    if not results:
        return f"(no runbooks matched: {keywords})"
    return "\n\n---\n\n".join(results[:3])


# ── Agent ──────────────────────────────────────────────────────────────────────

def build_agent():
    llm = ChatAnthropic(model=MODEL, max_tokens=2048, temperature=0)
    tools = [kubectl_get, prometheus_query, search_runbooks]
    # Use a standard ReAct prompt from LangChain hub, or fall back to a local one
    try:
        prompt = hub.pull("hwchase17/react")
    except Exception:
        from langchain.prompts import PromptTemplate
        prompt = PromptTemplate.from_template(
            "You are an SRE agent. Answer the question using the tools available.\n"
            "Tools: {tools}\nTool names: {tool_names}\n\n"
            "Question: {input}\nScratchpad: {agent_scratchpad}"
        )
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=8, handle_parsing_errors=True)


def dry_run(incident: str) -> None:
    print(f"\n[dry-run] Incident: {incident}\n")
    print("Agent would use these tools in sequence:")
    print("  1. kubectl_get('pods --all-namespaces --field-selector=status.phase!=Running')")
    print("  2. kubectl_get('events --field-selector=type=Warning --sort-by=.lastTimestamp')")
    print("  3. search_runbooks('crashloop pod restart')")
    print("  4. prometheus_query('kube_pod_container_status_restarts_total')")
    print("\n[dry-run] Skipping real API calls. Set ANTHROPIC_API_KEY and remove --dry-run to run.\n")


def main():
    global RUNBOOKS_DIR
    parser = argparse.ArgumentParser(description="Autonomous incident investigation agent")
    parser.add_argument("incident", help="Incident description or question")
    parser.add_argument("--runbooks", metavar="DIR", help="Path to Markdown runbooks directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what the agent would do, skip API calls")
    args = parser.parse_args()

    RUNBOOKS_DIR = args.runbooks

    if args.dry_run:
        dry_run(args.incident)
        return

    executor = build_agent()
    result = executor.invoke({"input": args.incident})
    print("\n" + "="*60)
    print("AGENT CONCLUSION:")
    print("="*60)
    print(result.get("output", "(no output)"))


if __name__ == "__main__":
    main()
