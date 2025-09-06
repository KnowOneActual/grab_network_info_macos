
# macOS Network Connection Checker

![Python version](https://img.shields.io/badge/python-3.x-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)

A simple Python script to quickly determine the primary network connection on a macOS device, showing whether it's connected via Wi-Fi or Ethernet and displaying relevant details for the active interface.


## Features



* Detects the primary (default) network interface.
* Identifies the connection type as either **Wi-Fi** or **Ethernet**.
* Displays key connection details:
    * IPv4 Address
    * MAC Address
    * Interface Name (e.g., en0)
    * Wi-Fi Network Name (SSID), if applicable.


## Prerequisites



* macOS
* Python 3.x


## Setup



1. **Clone the repository (or download the files):** 
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git) 
cd your-repo-name 

2. Install the required Python package: 
This project depends on the psutil library. You can install it using the provided requirements.txt file. 
pip install -r requirements.txt 



## Usage

Run the script from your terminal:

```bash
python3 check_network.py 

```


The script will then print the details of your current active network connection.


### Example Output

**If connected to Wi-Fi:**

```bash
🔍 Checking active network connection on this Mac...
✅ Found default network interface: en0 via gateway 192.168.1.1

--- Connection Details ---
  Connection Type: Wi-Fi 📶
  Wi-Fi Network (SSID): Your-WiFi-Name
  IPv4 Address: 192.168.1.123
  MAC Address: a1:b2:c3:d4:e5:f6
  Interface Name: en0
--------------------------

```

**If connected via Ethernet:**
```bash
🔍 Checking active network connection on this Mac...
✅ Found default network interface: en5 via gateway 10.0.1.1

--- Connection Details ---
  Connection Type: Ethernet 📶
  IPv4 Address: 10.0.1.45
  MAC Address: a1:b2:c3:d4:e5:f7
  Interface Name: en5
--------------------------


```

How It Works
The script uses a combination of built-in macOS command-line tools and the psutil library:

netstat -rn -f inet: This command is used to find the default network route and identify the primary network interface (e.g., en0).

networksetup -getairportnetwork [interface]: By attempting to run this command, the script determines if the interface is a Wi-Fi device. If the command succeeds, it's Wi-Fi; if it fails, it's assumed to be Ethernet.

psutil: This cross-platform library is used to easily and reliably fetch network interface details like IP and MAC addresses.


## License

This project is licensed under the MIT License.
