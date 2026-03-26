# ContainerLab-2026

This repository automates a Cisco IOS-XRd lab running on a remote Ubuntu host. It combines Terraform, Ansible, Containerlab, and a couple of local Python helper scripts to provision the server, prepare the lab environment, deploy topologies, and push configs.

## What the repository does

The intended workflow is:

1. Terraform provisions a remote Ubuntu VM on vSphere.
2. Ansible installs Docker and Containerlab on that VM.
3. Ansible copies topologies and prepares the IOS-XRd image.
4. Local scripts connect to lab nodes and push ISP configs.

The project is currently centered around a single lab host named `SB-ContainerLab`.

## Repository structure

- `terraform/` vSphere VM provisioning
- `ansible/` remote host preparation and lab operations
- `Topologies/` Containerlab topology files
- `Configurations/ISP/` router configs for the ISP lab
- `scripts/` local helper scripts
- `config.txt` local runtime settings for helper scripts
- `makefile` main entry points for the workflow

## Topologies

### `Topologies/test-lab.clab.yml`

Small IOS-XRd topology with:

- `r1`
- `r2`
- `r3`

### `Topologies/ISP.clab.yml`

Provider/customer lab with:

- `P0`
- `PE1`
- `PE2`
- `RR`
- `CE1`
- `CE2`
- `CE3`

SSH ports exposed by the ISP topology on the remote host:

- `2310` for `P0`
- `2311` for `PE1`
- `2312` for `PE2`
- `2313` for `CE1`
- `2314` for `CE2`
- `2315` for `RR`
- `2316` for `CE3`

## Prerequisites

Local machine requirements:

- Terraform
- Python 3
- access to the vSphere environment
- SSH access to the remote Ubuntu host

Python dependencies used by the helper scripts:

- `ansible`
- `ansible-vault`
- `PyYAML`
- `netmiko`

The `connect` helper is macOS-specific because it uses AppleScript to open Terminal windows.

## Local configuration

The helper scripts read connection details from `config.txt` in the repository root:

```txt
SERVER_IP=10.208.116.71
USERNAME=clab
PASSWORD=clab@123
```

These values are used by:

- `scripts/open_terminals.py`
- `scripts/push_ISP_configs.py`

## Initial setup

1. Copy `_.env_example` to `.env`.
2. Fill in the `TF_VAR_*` values for your vSphere environment.
3. Verify the Ansible inventory matches your target host.
4. Place the IOS-XRd image in the expected local path.
5. Create the Python virtual environment and install dependencies.

Example:

```bash
cp _.env_example .env
make setup-ansible
source .venv/bin/activate
pip install pyyaml netmiko
```

## IOS-XRd image

The IOS-XRd image is not stored in this repository.

The Ansible playbook currently expects the local image file at:

```txt
Images/xrd-control-plane-container-x86.25.4.1.dms
```

## Provisioning workflow

Run commands from the repository root.

### 1. Provision the VM

```bash
make tf-init
make tf-apply
```

### 2. Prepare the remote host

```bash
make setup-ansible
make upgrade-packages
make install-docker
make install-containerlab
make prepare-iosxrd
make copy-labs
```

## Lab operations from the local machine

Copy topologies to the remote host:

```bash
make copy-labs
```

Deploy a topology:

```bash
make deploy-lab TOPO=test-lab.clab.yml
```

Deploy the ISP lab:

```bash
make deploy-lab TOPO=ISP.clab.yml
```

Open SSH sessions to all nodes defined in a topology:

```bash
make connect TOPO=test-lab.clab.yml
```

Push ISP configs with Netmiko:

```bash
make configure-ISP
```

## Operating Containerlab on the remote host

Once logged in to the lab server, you can use Containerlab directly:

```bash
containerlab deploy -t Topologies/test-lab.clab.yml --reconfigure
containerlab deploy -t Topologies/ISP.clab.yml --reconfigure
containerlab destroy -a -c
docker ps
```

Example direct node access from the remote host:

```bash
ssh clab@clab-xrd-lab-r1
```

Example access from the local machine through a forwarded port:

```bash
ssh <configured-username>@<server-ip> -p 2311
```

Use the values from `config.txt` for the username, password, and server IP.

## Notes

- `config.txt` centralizes the connection settings used by the local helper scripts.
- Some other parts of the repository still contain environment-specific values, especially in Terraform, Ansible inventory, and test files.
- `ansible/playbooks/copy_labs.yml` currently uses an absolute local source path.
- This repo is tailored to a personal lab environment, so small adjustments may be needed for reuse elsewhere.
