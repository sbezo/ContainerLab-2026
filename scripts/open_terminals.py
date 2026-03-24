# this script open terminal on macos, call ssh to forwarded port (directly to router) and send default password)
import subprocess
import sys
import yaml
import time
import os

topo = sys.argv[1]
workdir = os.getcwd()
topo_path = f'{workdir}/Topologies/{topo}'
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
        clab@10.208.116.71 -p " + port
    passw = "clab@123"

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