from scapy.all import *
import eth_scapy_sd as sd
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether


class eventgroup:
    def __init__(self):
        self.eventgroup_id = 0x04
        self.control_string = ''
        self.object_dist = 0.0

    def event_1(self):
        print('object detected!')
        self.control_string = 'stop!'

    def event_2(self):
        print('object not detected')
        self.control_string = 'move forward'

class Service(eventgroup):
    def __init__(self):
        super().__init__()
        self.control_flag = False
        self.service_id = 0x1111

    def main(self):
        if self.control_flag is False:
            self.event_1()

        else:
            self.event_2()

        self.control_flag = not self.control_flag


srv = Service()
sdp = sd.SD()

# reboot flag = 0, unicast flag = 0, explicit initial data flag = 0, 나머지 비트는 무시
sdp.flags = 0x00

# type default: 0x06 (Subscribe Event Group), service id = 0x1111, instance id = 0xffff,
# ttl: 5 sec, event group id = 0x04
sdp.entry_array = [
    sd.SDEntry_EventGroup(srv_id=srv.service_id, n_opt_1=1, inst_id=0xffff, major_ver=0x03,
                          eventgroup_id=srv.eventgroup_id, cnt=0x0,
                          ttl=0x05)]

# 엔트리에 추가적인 정보를 전송하기 위해 사용
# Service Instance에 도달하기 위해 IP주소, 전송계층, 포트번호 정보를 가지고 있음
# addr = 192.168.0.1, l4_proto = 0x11 (UDP), port = 0xd903
sdp.option_array = [
    sd.SDOption_IP4_EndPoint(addr="192.168.0.116", l4_proto=0x11, port=0xd903)]

if __name__ == '__main__':
    while True:
        p = Ether() / IP(src='192.168.0.13', dst='192.168.0.116') / UDP(sport=138, dport=5355) / sdp.getSomeip(True)
        srv.main()
        p.add_payload(srv.control_string)
        sendp(p, count=1)
        p.remove_payload()