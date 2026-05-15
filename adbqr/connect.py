import socket
import threading
from zeroconf import ServiceBrowser, Zeroconf, ServiceListener

from . import CONNECT_SERVICE
from .select import select_device
from .adb import run_adb

class AutoConnectListener(ServiceListener):
    def __init__(self, target_ip, event, info_dict):
        self.target_ip = target_ip
        self.event = event
        self.info_dict = info_dict

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            address = socket.inet_ntoa(info.addresses[0]) if info.addresses else None
            if address == self.target_ip:
                self.info_dict['port'] = info.port
                self.event.set()

def auto_connect_to_ip(ip_address: str):
    print("Waiting for device to broadcast connection service...")
    zeroconf = Zeroconf()
    event = threading.Event()
    info_dict = {}
    
    listener = AutoConnectListener(ip_address, event, info_dict)
    browser = ServiceBrowser(zeroconf, CONNECT_SERVICE, listener)
    
    try:
        # Wait up to 15 seconds for the connection mDNS broadcast
        if event.wait(timeout=15.0):
            port = info_dict.get('port')
            print(f"Connecting to {ip_address}:{port}...")
            result = run_adb(["connect", f"{ip_address}:{port}"])
            
            # ADB connect returns 0 even on failure, so we must check stdout
            if result.returncode == 0 and "failed" not in result.stdout.lower():
                print("Connection successful!")
            else:
                print("Connection failed.")
                if result.stdout:
                    print(f"ADB output: {result.stdout.strip()}")
        else:
            print("Timed out waiting for connection broadcast. You might need to toggle Wireless Debugging off and on, then run 'adbqr connect'.")
    finally:
        zeroconf.close()

def run():
    info = select_device(CONNECT_SERVICE)
    address = info["address"]
    port = info["port"]
    
    print("Connecting...")
    
    result = run_adb(["connect", f"{address}:{port}"])
    if result.returncode == 0 and "failed" not in result.stdout.lower():
        print("Connected!")
    else:
        print("Connection failed.")
        if result.stdout:
            print(f"ADB output: {result.stdout.strip()}")
