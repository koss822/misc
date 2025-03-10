# NRPE Plugin: Kubernetes Pod Status Checker

This NRPE plugin checks the status of Kubernetes pods and reports if any pod is not in the "Running" state. It is designed to work with Nagios or any monitoring system compatible with NRPE.

---

## Features

- Verifies the status of all pods in a specified namespace or across all namespaces.
- Reports the number and names of pods not in the "Running" state.
- Supports filtering out completed pods (e.g., from Kubernetes jobs).
- Outputs results in Nagios-compatible format.

---

## Requirements

- **NRPE**: Ensure that NRPE is installed and configured on the target machine.
- **Kubernetes CLI (kubectl)**: The plugin requires `kubectl` to interact with the Kubernetes cluster.
- **Kubeconfig**: Ensure that the user running this plugin has access to the Kubernetes cluster via a valid kubeconfig file.

---

## Installation

1. Clone or download this repository to your NRPE plugins directory (e.g., `/usr/local/nagios/libexec`).
2. Make the script executable