import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="new mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Interface not specified, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] New mac address not specified, use --help for more info")
    return options

def mac_changer(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_mac_address(interface):
    output = subprocess.check_output(["ifconfig", interface])
    mac_addresses = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(output))
    if mac_addresses:
        return mac_addresses.group(0)
    else:
        print("No mac address available with " + interface)


options = get_arguments()  
current_mac = get_mac_address(options.interface)
print("[+] Current MAC address -> " + str(current_mac))
mac_changer(options.interface, options.new_mac)
current_mac = get_mac_address(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address changed sucessfully to " + current_mac)
else:
    print("[-] MAC address not changed!")