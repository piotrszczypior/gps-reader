import asyncio
import re
from pathlib import Path

import bluetooth
from PyOBEX.client import Client

graphics_files_regex = r'([-\w]+\.(?:jpg|jpeg|png|gif|bmp))'


def show_devices():
    devices = bluetooth.discover_devices()
    for device in devices:
        print("Device address: ", device, " name=", bluetooth.lookup_name(device))


def menu():
    while True:
        print("1. Print local devices. ")
        print("2. Connect to divice using MAC address\n")
        choice = input("Choose option: ")
        if choice == "1":
            show_devices()
        elif choice == "2":
            device_address = input("Device address: ")
            asyncio.run(connect(device_address))


async def connect(device_address: str):
    services = list(
        filter(lambda x: "OBEX Object Push" in str(x["name"]), bluetooth.find_service(address=device_address)))
    service = services[0]
    host = service["host"]
    name = service["name"]
    port = service["port"]
    print("Connecting to %s on %s" % (name, host))
    client_socket = Client(device_address, port)
    client_socket.connect()
    filepath = input("Enter filepath: ")
    file = Path(filepath)
    print(f'File size {file.stat().st_size}')
    if file.stat().st_size <= 50000 and re.search(pattern=graphics_files_regex, string=filepath):
        print(f'Sending file {file} to {bluetooth.lookup_name(device_address)} on address {device_address}')
        client_socket.put(filepath, file.read_bytes())
    client_socket.disconnect()


if __name__ == '__main__':
    menu()
