from scapy.all import *
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether

import eth_scapy_someip as someip
import keyboard


class pipeline:
    def __init__(self):
        self.sip = someip.SOMEIP()
        self.sip.msg_id.srv_id = 0xffff
        self.sip.msg_id.sub_id = 0x0
        self.sip.msg_id.method_id = 0x0000

        self.sip.req_id.client_id = 0xdead
        self.sip.req_id.session_id = 0xbeaf

        self.sip.msg_type = 0x01
        self.sip.retcode = 0x00

    def send_message(self, msg):
        p = Ether() / IP(src='192.168.0.13', dst='192.168.0.116') / UDP(sport=138, dport=5355) / self.sip
        p.add_payload(msg)
        sendp(p, count=1)


if __name__ == '__main__':
    sip = pipeline()
    cnt = 0
    while True:
        sip.send_message('hello_someip' + str(cnt))
        cnt += 1

        if keyboard.read_key() == 'q':
            print('Stop sending Message')
            del sip
            break
