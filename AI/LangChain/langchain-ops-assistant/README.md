# langchain-ops-assistant

> The on-call agent that doesn't need to be woken up.

A LangChain ReAct agent that autonomously investigates infrastructure incidents. Given
an incident description, it decides which tools to run (kubectl, Prometheus, runbook search),
interprets the results, and iterates until it reaches a diagnosis and remediation plan.

## Tools available to the agent

| Tool | What it does |
|---|---|
| `kubectl_get` | Read-only kubectl commands (get, describe, logs, top) |
| `prometheus_query` | Execute PromQL instant queries |
| `search_runbooks` | Keyword search over local Markdown runbooks |

## Usage

```bash
# Basic incident investigation
python assistant.py "Pods in namespace prod are crashlooping since 14:00"

# With runbooks directory
python assistant.py "High memory on node-3" --runbooks ./runbooks

# Point at a specific Prometheus instance
PROMETHEUS_URL=http://prometheus.monitoring:9090 python assistant.py "CPU spike on api pods"

# Dry-run
python assistant.py "Database pods not starting" --dry-run
```

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
export PROMETHEUS_URL=http://localhost:9090   # optional
```

## Example agent trace (verbose output)

```
Thought: I need to check the status of pods in namespace prod.
Action: kubectl_get
Action Input: pods -n prod
Observation: NAME              READY   STATUS             RESTARTS   AGE
             api-7d9f-xkp2n   0/1     CrashLoopBackOff   14         2h

Thought: There is a CrashLoopBackOff. Let me check the logs.
Action: kubectl_get
Action Input: logs -n prod api-7d9f-xkp2n --tail=50
...
Final Answer: The api pod is crashlooping due to a missing DATABASE_URL environment variable...
```
