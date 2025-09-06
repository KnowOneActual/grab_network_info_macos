import subprocess
import re
import psutil
import socket  # Added for network constants


def get_default_interface():
    """
    Finds the primary network interface on macOS by looking for the
    default route that has a gateway IP address, ignoring virtual interfaces.
    """
    try:
        # Get the IPv4 routing table.
        command = "netstat -rn -f inet"
        result = subprocess.check_output(command, shell=True, text=True)

        # Search for the line defining the default route
        for line in result.splitlines():
            # A typical default route looks like: 'default 192.168.1.1 UGSc en0'
            if line.startswith("default"):
                parts = line.split()
                if len(parts) >= 4:
                    # The gateway is the 2nd part, interface is the 4th (or last)
                    gateway = parts[1]
                    interface = parts[3]
                    # Check if the gateway is a valid IP to avoid virtual interfaces
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


def get_connection_info(interface):
    """
    Gathers connection details for a specific network interface.
    """
    info = {"interface": interface}

    # Use networksetup to determine if the interface is Wi-Fi or Ethernet
    try:
        # This command fails if the interface is not a Wi-Fi device
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

    # Use psutil to get IP address information
    try:
        addresses = psutil.net_if_addrs().get(interface, [])
        for addr in addresses:
            # CORRECTED LOGIC: Check for IPv4 and MAC addresses
            if addr.family == socket.AF_INET:  # AF_INET is for IPv4
                info["ipv4_address"] = addr.address
            elif addr.family == psutil.AF_LINK:  # AF_LINK is for the MAC Address
                info["mac_address"] = addr.address
    except Exception as e:
        print(f"Could not get IP addresses for {interface}: {e}")

    return info


def main():
    """
    Main function to run the network check and display the results.
    """
    print("🔍 Checking active network connection on this Mac...")

    default_interface = get_default_interface()

    if default_interface:
        connection_details = get_connection_info(default_interface)

        print("\n--- Connection Details ---")
        if connection_details:
            print(f"  Connection Type: {connection_details.get('type', 'N/A')} 📶")
            if "ssid" in connection_details:
                print(
                    f"  Wi-Fi Network (SSID): {connection_details.get('ssid', 'N/A')}"
                )
            print(f"  IP Address: {connection_details.get('ipv4_address', 'N/A')}")
            print(f"  MAC Address: {connection_details.get('mac_address', 'N/A')}")
            print(f"  Interface Name: {connection_details.get('interface', 'N/A')}")
            print("--------------------------\n")
        else:
            print("❌ Could not retrieve details for the connection.")


if __name__ == "__main__":
    main()
