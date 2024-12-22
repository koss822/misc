# `pod_by_pid_4microk8s`

### A Script to Find the Kubernetes Pod Associated with a Process (PID) on MicroK8s

`pod_by_pid.sh` is a Bash script designed specifically for environments running MicroK8s. It helps you determine which Kubernetes pod a specific process (identified by its PID) belongs to. This script extracts the container ID from the Linux process cgroup file and maps it to the corresponding pod using the `kubectl` command.

---

## ✨ Features

- **Works exclusively with MicroK8s**:
  - The script is tailored for MicroK8s, a lightweight Kubernetes distribution.
- **Maps processes to pods**:
  - Given a Linux process ID (PID), this script efficiently locates the associated pod's name and namespace.
- **Handles Edge Cases**:
  - Includes robust handling for processes without container IDs or when certain fields are null or incomplete.
- **Error Handling**:
  - Clearly notifies users of invalid PIDs, missing container IDs, or unmatched pods.

---

## ⚙️ How It Works

1. **Provide a Process ID (PID)** as input to the script.
2. The script inspects the process’s `/proc/<PID>/cgroup` file to extract the Kubernetes container ID.
3. It uses the container ID to query all running Kubernetes pods via the MicroK8s `kubectl` tool.
4. If a match is found, it outputs the namespace and name of the pod associated with the process.

This script relies on the fact that MicroK8s organizes containers via `containerd` or similar runtime, and the cgroup paths include critical container metadata.

---

## 📜 Prerequisites

1. **MicroK8s**:
   - Ensure MicroK8s is installed and running on your system.
   - The script assumes the `kubectl` command provided by MicroK8s is installed and available or properly aliased (e.g., `microk8s kubectl` may be aliased to `kubectl`).

2. **jq**:
   - The script requires `jq` to parse JSON output from Kubernetes API queries.
   - Install it using:
     ```bash
     # On Debian/Ubuntu
     sudo apt-get install jq

     # On RHEL/CentOS
     sudo yum install jq

     # On macOS
     brew install jq
     ```

3. **Run the Script with Sufficient Permissions**:
   - Run the script as a user with access to the `/proc` filesystem and Kubernetes cluster configurations in MicroK8s (requires access to `kubectl`).

---

## 🔧 Installation

1. Save the script to a file:
   ```bash
   nano pod_by_pid.sh