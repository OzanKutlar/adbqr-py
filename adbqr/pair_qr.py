import socket
import threading
from nanoid import generate
from zeroconf import ServiceBrowser, Zeroconf, ServiceListener

from . import PAIRING_SERVICE
from .qr import QrRenderer
from .adb import run_adb

HELP_MESSAGE = """\
\x1B[1mPair with QR code\x1B[0m

Make sure your Android device is on the same network as your computer.
Then, on your Android device:
1. Open \x1B[1mDeveloper options\x1B[0m.
2. Open \x1B[1mWireless debugging\x1B[0m, and enable it if necessary.
3. Select \x1B[1mPair device with QR code\x1B[0m.
4. Scan the following QR code:
"""

class PairingListener(ServiceListener):
    def __init__(self, service_name, match_event, device_info):
        self.service_name = service_name
        self.match_event = match_event
        self.device_info = device_info

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        if name.startswith(self.service_name):
            info = zc.get_service_info(type_, name)
            if info:
                self.device_info['address'] = socket.inet_ntoa(info.addresses[0])
                self.device_info['port'] = info.port
                self.match_event.set()

def run():
    print(HELP_MESSAGE)
    
    service_name = f"adbqr-{generate(size=4)}"
    password = generate(size=6)
    
    data = f"WIFI:T:ADB;S:{service_name};P:{password};;"
    renderer = QrRenderer(data)
    renderer.render()
    
    zeroconf = Zeroconf()
    match_event = threading.Event()
    device_info = {}
    
    listener = PairingListener(service_name, match_event, device_info)
    browser = ServiceBrowser(zeroconf, PAIRING_SERVICE, listener)
    
    try:
        match_event.wait()
        print("Pairing...")
        
        address = device_info.get("address")
        port = device_info.get("port")
        
        result = run_adb(["pair", f"{address}:{port}", password])
        
        if result.returncode == 0:
            print("Paired!")
        else:
            print("Pairing failed.")
    finally:
        zeroconf.close()
