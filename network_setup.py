#!/usr/bin/env python3

import subprocess
import os

def is_root():
    return os.geteuid() == 0

def check_network():
    try:
        response = subprocess.check_call(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return response == 0
    except subprocess.CalledProcessError:
        return False

def fix_ethernet():
    try:
        print("Attempting to restart network service...")
        subprocess.run(["systemctl", "restart", "NetworkManager"], check=True)
        if check_network():
            print("✅ Network is now up!")
            return True
        else:
            print("❌ Failed to fix the network issue. Starting the setup wizard...")
            return setup_wizard()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def setup_wizard():
    print("---------------------------------")
    print("🛠 Network Setup Wizard")
    print("---------------------------------")

    try:
        conn_name = input("Enter connection name (e.g., MyConnection): ")
        if_name = input("Enter interface name (usually like eth0, enp2s0): ")
        ip_addr = input("Enter IP Address (e.g., 192.168.1.10): ")
        gateway = input("Enter Gateway (e.g., 192.168.1.1): ")
        dns = input("Enter DNS (e.g., 8.8.8.8,8.8.4.4): ")

        # Basic validation
        if not all([conn_name, if_name, ip_addr, gateway, dns]):
            print("❌ All fields must be filled!")
            return False

        # Configure the connection
        subprocess.run(["nmcli", "con", "add", "type", "ethernet", "con-name", conn_name, "ifname", if_name, "ip4", ip_addr, "gw4", gateway], check=True)
        subprocess.run(["nmcli", "con", "mod", conn_name, "ipv4.dns", dns], check=True)

        # Activate the connection
        subprocess.run(["nmcli", "con", "up", conn_name], check=True)
        return check_network()

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if not is_root():
        print("❌ This script must be run as root")
        exit(1)

    print("🌐 Checking network connectivity...")
    if not check_network():
        print("❌ Network is down. Attempting to fix...")
        if fix_ethernet():
            print("✅ Network setup successful and now up!")
        else:
            print("❌ Failed to establish the network connection. Please check your settings.")
    else:
        print("✅ Network is up. No issues detected.")
