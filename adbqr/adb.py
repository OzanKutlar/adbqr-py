import json
import os
import shutil
import subprocess
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "adbqr"
CONFIG_FILE = CONFIG_DIR / "config.json"

def get_adb_path() -> str:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                path = data.get("adb_path")
                if path and Path(path).exists():
                    return path
        except json.JSONDecodeError:
            pass

    cwd_adb = Path("adb.exe") if os.name == "nt" else Path("adb")
    if cwd_adb.exists():
        resolved = str(cwd_adb.resolve())
        _save_config(resolved)
        return resolved

    path_adb = shutil.which("adb")
    if path_adb:
        _save_config(path_adb)
        return path_adb

    print("adb executable not found in current directory or PATH.")
    while True:
        user_path = input("Please enter the full path to adb executable: ").strip()
        user_path = user_path.strip("\"'")
        
        if Path(user_path).exists():
            try:
                subprocess.run([user_path, "version"], check=True, capture_output=True)
                _save_config(user_path)
                return user_path
            except (subprocess.SubprocessError, OSError):
                print("Failed to run adb at that path. Please try again.")
        else:
            print("Path does not exist. Please try again.")

def _save_config(path: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"adb_path": path}, f)

def run_adb(args: list[str]) -> subprocess.CompletedProcess:
    adb_path = get_adb_path()
    cmd = [adb_path] + args
    return subprocess.run(cmd, capture_output=True, text=True)
