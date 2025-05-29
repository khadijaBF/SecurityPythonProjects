from scapy.all import sniff, Ether, IP, TCP, UDP, Raw
from colorama import Fore, Style, init

# Initialize colorama
init()

def packet_callback(packet):
    """
    Callback function to process each captured packet.
    """
    # Check if the packet has an IP layer
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        protocol = packet[IP].proto

        # Print IP packet info in blue
        print(f"{Fore.BLUE}IP Packet: {ip_src} -> {ip_dst} | Protocol: {protocol}{Style.RESET_ALL}")

        # Check for TCP layer
        if TCP in packet:
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport
            # Print TCP info in green
            print(f"{Fore.GREEN}TCP: {ip_src}:{tcp_sport} -> {ip_dst}:{tcp_dport}{Style.RESET_ALL}")

            # Check for raw data (payload)
            if Raw in packet:
                payload = packet[Raw].load
                # Print payload in yellow
                print(f"{Fore.YELLOW}Payload: {payload}{Style.RESET_ALL}")

        # Check for UDP layer
        elif UDP in packet:
            udp_sport = packet[UDP].sport
            udp_dport = packet[UDP].dport
            # Print UDP info in cyan
            print(f"{Fore.CYAN}UDP: {ip_src}:{udp_sport} -> {ip_dst}:{udp_dport}{Style.RESET_ALL}")

def start_sniffer(interface=None, count=0):
    """
    Start sniffing network traffic.
    :param interface: Network interface to sniff on (e.g., 'eth0'). If None, uses the default interface.
    :param count: Number of packets to capture. If 0, captures indefinitely.
    """
    print(f"{Fore.MAGENTA}Starting sniffer on interface {interface if interface else 'default'}...{Style.RESET_ALL}")
    sniff(iface=interface, prn=packet_callback, count=count)

if __name__ == "__main__":
    # Specify the network interface (e.g., 'eth0', 'wlan0') or leave as None for the default interface
    interface = None

    # Start the sniffer
    start_sniffer(interface=interface)
