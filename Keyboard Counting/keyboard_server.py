from scapy.all import *
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether

import eth_scapy_someip as someip
import keyboard


class pipeline:
    def __init__(self):
        # some ip header 설정
        self.sip = someip.SOMEIP()

        # message id
        self.sip.msg_id.srv_id = 0xffff
        self.sip.msg_id.sub_id = 0x0
        self.sip.msg_id.method_id = 0x0000

        # request id
        self.sip.req_id.client_id = 0xdead
        self.sip.req_id.session_id = 0xbeaf

        # Message Type, Return Code
        self.sip.msg_type = 0x01
        self.sip.retcode = 0x00

    def send_message(self, msg):
        # stack 생성
        # 링크 계층: Ether()
        # 네트워크 계층: IP(src='192.168.0.13', dst='192.168.0.116')
        # 전송 계층: UDP(sport=138, dport=5355)
        # 어플리케이션 계층: SOME/IP
        p = Ether() / IP(src='192.168.0.13', dst='192.168.0.116') / UDP(sport=138, dport=5355) / self.sip
        p.add_payload(msg)  # payload에 msg를 추가
        sendp(p, count=1)  # payload 전송


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
