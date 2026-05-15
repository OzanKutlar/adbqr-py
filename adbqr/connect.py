from . import CONNECT_SERVICE
from .select import select_device
from .adb import run_adb

def run():
    info = select_device(CONNECT_SERVICE)
    address = info["address"]
    port = info["port"]
    
    print("Connecting...")
    
    result = run_adb(["connect", f"{address}:{port}"])
    if result.returncode == 0:
        print("Connected!")
    else:
        print("Connection failed.")
