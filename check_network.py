import subprocess
import re
import psutil
import socket
from typing import Dict, Optional, Any


def get_default_interface() -> Optional[str]:
    """
    Finds the primary network interface on macOS by looking for the
    default route that has a gateway IP address, ignoring virtual interfaces.

    Returns:
        Optional[str]: The name of the interface (e.g., 'en0'), or None if not found.
    """
    try:
        command = "netstat -rn -f inet"
        result = subprocess.check_output(command, shell=True, text=True)

        for line in result.splitlines():
            if line.startswith("default"):
                parts = line.split()
                if len(parts) >= 4:
                    gateway, interface = parts[1], parts[3]
                    # Check if the gateway looks like a valid IP to avoid virtual interfaces
                    if all(c in "0123456789." for c in gateway):
                        print(
                            f"✅ Found default network interface: {interface} via gateway {gateway}"
                        )
                        return interface

        print("❌ Could not find a standard default network interface.")
        return None

    except subprocess.CalledProcessError:
        print("❌ Could not check routing table. Are you connected to a network?")
        return None


def get_connection_info(interface: str) -> Dict[str, Any]:
    """
    Gathers connection details for a specific network interface.

    Args:
        interface (str): The name of the network interface.

    Returns:
        Dict[str, Any]: A dictionary containing the connection details.
    """
    info: Dict[str, Any] = {"interface": interface}

    try:
        command = f"networksetup -getairportnetwork {interface}"
        result = subprocess.check_output(
            command, shell=True, text=True, stderr=subprocess.DEVNULL
        )
        info["type"] = "Wi-Fi"
        ssid_match = re.search(r"Current Wi-Fi Network: (.+)", result)
        if ssid_match:
            info["ssid"] = ssid_match.group(1)
    except subprocess.CalledProcessError:
        info["type"] = "Ethernet"

    try:
        addresses = psutil.net_if_addrs().get(interface, [])
        for addr in addresses:
            if addr.family == socket.AF_INET:  # IPv4
                info["ipv4_address"] = addr.address
            elif addr.family == socket.AF_INET6:  # IPv6
                info["ipv6_address"] = addr.address.split("%")[0]  # Clean up zone index
            elif addr.family == psutil.AF_LINK:  # MAC Address
                info["mac_address"] = addr.address
    except Exception as e:
        print(f"Could not get IP addresses for {interface}: {e}")

    return info


def display_connection_details(details: Dict[str, Any]):
    """Prints the formatted connection details."""
    print("\n--- Connection Details ---")
    print(f"  Connection Type: {details.get('type', 'N/A')} 📶")
    if "ssid" in details:
        print(f"  Wi-Fi Network (SSID): {details.get('ssid', 'N/A')}")
    print(f"  IPv4 Address: {details.get('ipv4_address', 'N/A')}")
    if "ipv6_address" in details:
        print(f"  IPv6 Address: {details.get('ipv6_address', 'N/A')}")
    print(f"  MAC Address: {details.get('mac_address', 'N/A')}")
    print(f"  Interface Name: {details.get('interface', 'N/A')}")
    print("--------------------------\n")


def main():
    """
    Main function to run the network check and display the results.
    """
    print("🔍 Checking active network connection on this Mac...")
    default_interface = get_default_interface()

    if default_interface:
        connection_details = get_connection_info(default_interface)
        if connection_details:
            display_connection_details(connection_details)
        else:
            print("❌ Could not retrieve details for the connection.")


if __name__ == "__main__":
    main()
