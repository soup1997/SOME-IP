from scapy.all import *
from scapy.layers.inet import UDP


def receive(msg):
    sippacket = bytes(msg[UDP].payload)
    print(sippacket)


if __name__ == '__main__':
    sniff(count=0, prn=receive, filter='udp port 138')
