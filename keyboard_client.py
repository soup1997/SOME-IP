from scapy.all import *
import eth_scapy_someip as someip
from scapy.layers.inet import UDP, IP


def receive(msg):
    sippacket = bytes(msg[UDP].payload)
    print(sippacket)


if __name__ == '__main__':
    sniff(count=0, prn=receive, filter='udp port 138')  # call back function