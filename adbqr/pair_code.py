from . import PAIRING_SERVICE
from .select import select_device
from .adb import run_adb
from .connect import auto_connect_to_ip

HELP_MESSAGE = """\
\x1B[1mPair with pairing code\x1B[0m

Make sure your Android device is on the same network as your computer.
Then, on your Android device:
1. Open \x1B[1mDeveloper options\x1B[0m.
2. Open \x1B[1mWireless debugging\x1B[0m, and enable it if necessary.
3. Select \x1B[1mPair device with pairing code\x1B[0m.
4. Complete these steps:
"""

def run():
    print(HELP_MESSAGE)
    
    info = select_device(PAIRING_SERVICE)
    address = info["address"]
    port = info["port"]
    
    password = input("Enter password: ").strip()
    print("Connecting...")
    
    result = run_adb(["pair", f"{address}:{port}", password])
    if result.returncode == 0:
        print("Paired successfully!")
        auto_connect_to_ip(address)
    else:
        print("Pairing failed.")
