import subprocess
import re
import psutil


def get_default_interface():
    """
    Finds the primary network interface (e.g., 'en0') on macOS
    by parsing the output of the 'netstat -rn' command.
    """
    try:
        # This command lists the routing tables; the default route is our target.
        command = "netstat -rn | grep default"
        result = subprocess.check_output(command, shell=True, text=True)

        # The interface name is usually the last word on the 'default' line.
        default_interface = result.strip().split()[-1]
        print(f"✅ Found default network interface: {default_interface}")
        return default_interface
    except subprocess.CalledProcessError:
        print(
            "❌ Could not determine the default network interface. Are you connected to a network?"
        )
        return None


def get_connection_info(interface):
    """
    Gathers connection details for a specific network interface.
    """
    info = {"interface": interface}

    # Use networksetup to determine if the interface is Wi-Fi or Ethernet
    try:
        command = f"networksetup -getairportnetwork {interface}"
        result = subprocess.check_output(
            command, shell=True, text=True, stderr=subprocess.DEVNULL
        )

        # If the command succeeds, it's a Wi-Fi connection
        info["type"] = "Wi-Fi"
        ssid_match = re.search(r"Current Wi-Fi Network: (.+)", result)
        if ssid_match:
            info["ssid"] = ssid_match.group(1)

    except subprocess.CalledProcessError:
        # If the command fails, it's likely an Ethernet or other wired connection
        info["type"] = "Ethernet"

    # Use psutil to get IP address information for the interface
    try:
        addresses = psutil.net_if_addrs().get(interface, [])
        for addr in addresses:
            # We are looking for the IPv4 address
            if (
                addr.family == psutil.AF_LINK.family
            ):  # In Python 3.9+ this is socket.AF_INET
                info["mac_address"] = addr.address
            elif (
                addr.family == psutil.AF_INET6.family
            ):  # In Python 3.9+ this is socket.AF_INET6
                info["ipv6_address"] = addr.address
            else:
                info["ipv4_address"] = addr.address

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
            print(f"  Interface Name: {connection_details.get('interface', 'N/A')}")
            print("--------------------------\n")
        else:
            print("❌ Could not retrieve details for the connection.")


if __name__ == "__main__":
    main()
