# this script open terminal on macos, call ssh to forwarded port (directly to router) and send default password)
from pathlib import Path
import subprocess
import sys
import yaml
import time

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config.txt"
TOPOLOGIES_DIR = ROOT_DIR / "Topologies"


def read_config(config_path: Path) -> dict[str, str]:
    config = {}

    with open(config_path, "r") as config_file:
        for line in config_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            key, separator, value = stripped.partition("=")
            if separator:
                config[key.strip()] = value.strip()

    required_keys = ("SERVER_IP", "USERNAME", "PASSWORD")
    missing_keys = [
        key for key in required_keys
        if not config.get(key) or config[key] == "CHANGE_ME"
    ]
    if missing_keys:
        missing = ", ".join(missing_keys)
        raise ValueError(f"Missing valid {missing} in {config_path}")

    return config


if len(sys.argv) < 2:
    raise SystemExit("Usage: python3 scripts/open_terminals.py <topology-file>")

topo = sys.argv[1]
config = read_config(CONFIG_PATH)
server_ip = config["SERVER_IP"]
username = config["USERNAME"]
password = config["PASSWORD"]
topo_path = TOPOLOGIES_DIR / topo
print(topo_path)
with open(topo_path, 'r') as f:
    topology = yaml.safe_load(f)

# Extract all higher ports
higher_ports = []
for node in topology['topology']['nodes'].items():
    port_mapping = node[1]['ports'][0]  # Get '2201:22'
    higher_port = port_mapping.split(':')[0]  # Get '2201'
    higher_ports.append(higher_port)


# calling the open_task.py script
for port in higher_ports:
    cmd = "ssh -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        " + username + "@" + server_ip + " -p " + port
    passw = password

    osascript_command = f'''
    tell application "Terminal"
        activate
        do script "{cmd}"
        delay 1
        do script "{passw}" in front window
    end tell
    '''

    subprocess.Popen(["osascript", "-e", osascript_command])
    time.sleep(2)
