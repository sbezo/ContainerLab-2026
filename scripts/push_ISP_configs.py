from pathlib import Path
from netmiko import ConnectHandler
from getpass import getpass
import os

HOST = "10.208.116.71"
USERNAME = "clab"
PASSWORD = "clab@123"

workdir = os.getcwd()
CFG_DIR = f'{workdir}/Configurations/ISP'
print(CFG_DIR)

# map file/router name -> ssh port on the remote host
ROUTERS = {
    "P0": 2310,
    "PE1": 2311,
    "PE2": 2312,
    "CE1": 2313,
    "CE2": 2314,
    "RR": 2315,
    "CE3": 2316,
}

def read_cfg_lines(cfg_file: Path):
    lines = []
    with open(cfg_file, "r") as file:
        for line in file:
            s = line.strip()
            lines.append(s)
    return lines


for router, port in ROUTERS.items():
    cfg_file = f"{CFG_DIR}/{router}.cfg"

    device = {
        "device_type": "cisco_xr",
        "host": HOST,
        "port": port,
        "username": USERNAME,
        "password": PASSWORD,
        "fast_cli": False,
    }

    print(f"\n=== {router} ({HOST}:{port}) ===")
    print(cfg_file)
    try:
        commands = read_cfg_lines(cfg_file)
        print(commands)

        with ConnectHandler(**device) as conn:
            output = conn.send_config_set(commands, read_timeout=120)
            print(output)
            if "Invalid" in output:
                print(f"chybny prikaz router: {router}")
                break
            commit_out = conn.commit()
            print(commit_out)
            

    except Exception as e:
        print(f"[FAIL] {router}: {e}")