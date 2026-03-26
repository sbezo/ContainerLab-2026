from pathlib import Path
from netmiko import ConnectHandler

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config.txt"
CFG_DIR = ROOT_DIR / "Configurations" / "ISP"
print(CFG_DIR)


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

config = read_config(CONFIG_PATH)
HOST = config["SERVER_IP"]
USERNAME = config["USERNAME"]
PASSWORD = config["PASSWORD"]

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
    cfg_file = CFG_DIR / f"{router}.cfg"

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
