import scapy.all as scapy 
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range")
    (options, arguments) = parser.parse_args()
    return options

def scan(IP):
    # scapy.ls(scapy.any())
    arp_request = scapy.ARP(pdst = IP)  
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request 
    # (answered, unanswered) = scapy.srp(arp_request_broadcast, timeout = 3, verbose = False)[0]
    answered = scapy.srp(arp_request_broadcast, timeout = 3, verbose = False)[0]
    captured_list = []
    for element in answered:
        captured_dict = {"IP" : element[1].psrc, "MAC" : element[1].hwsrc}
        captured_list.append(captured_dict)
    return captured_list


def view(captured_list):
    print("\n------------------------|------------------------\nIP\t\t\t|\tMAC Address\n------------------------|------------------------")
    for user in captured_list:
        print(user["IP"] + "\t\t|\t" + user["MAC"])


options = get_arguments()  
scan = scan(options.target)     
view(scan)