import socket
import sys
import threading
from zeroconf import ServiceBrowser, Zeroconf, ServiceListener

ENTER_DEVICE = "Select a device by index: "

class DeviceListener(ServiceListener):
    def __init__(self, devices_list, lock, prompt_event):
        self.devices_list = devices_list
        self.lock = lock
        self.prompt_event = prompt_event

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            with self.lock:
                address = socket.inet_ntoa(info.addresses[0]) if info.addresses else "Unknown"
                port = info.port
                hostname = info.server.rstrip(".local.")
                
                device_info = {
                    "name": name,
                    "hostname": hostname,
                    "address": address,
                    "port": port
                }
                
                self.devices_list.append(device_info)
                
                # Clear current line and move to column 0
                sys.stdout.write('\r\x1b[2K')
                print(f"{len(self.devices_list)}. {hostname} ({address}:{port})")
                
                if self.prompt_event.is_set():
                    sys.stdout.write(ENTER_DEVICE)
                    sys.stdout.flush()

def select_device(service_type: str) -> dict:
    zeroconf = Zeroconf()
    devices = []
    lock = threading.Lock()
    prompt_event = threading.Event()
    
    listener = DeviceListener(devices, lock, prompt_event)
    browser = ServiceBrowser(zeroconf, service_type, listener)
    
    print("Available devices:")
    prompt_event.set()
    sys.stdout.write(ENTER_DEVICE)
    sys.stdout.flush()
    
    try:
        while True:
            try:
                user_input = input().strip()
                if not user_input:
                    continue
            except EOFError:
                sys.exit(1)
                
            prompt_event.clear()
            
            try:
                index = int(user_input)
                with lock:
                    if 1 <= index <= len(devices):
                        return devices[index - 1]
            except ValueError:
                pass
            
            print("Invalid input.")
            with lock:
                print("Available devices:")
                for i, d in enumerate(devices):
                    print(f"{i + 1}. {d['hostname']} ({d['address']}:{d['port']})")
                prompt_event.set()
                sys.stdout.write(ENTER_DEVICE)
                sys.stdout.flush()
    finally:
        zeroconf.close()
