from scapy.all import *
import eth_scapy_sd as sd
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether
import cv2

class event_group:
    def __init__(self):
        self.eventgroup_id = 0x04
        self.event_string = b''

    def event_1(self):
        self.event_string = b'face detected!'

    def event_2(self):
        self.event_string = b'face not detected!'

    def processing(self, img):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # detect faces
        faces = face_cascade.detectMultiScale(gray_img, 1.1, 4)

        # draw rectangle around the faces
        if len(faces) != 0:
            self.event_1()
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, 'Detected', (x, y - 20), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        else:
            self.event_2()

        # display the output
        cv2.imshow('face_detection', img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            exit()


class face_recognition(event_group):
    def __init__(self):
        super().__init__()
        self.service_id = 0x1111
        self.n_opt_1 = 1
        self.inst_id = 0xffff
        self.major_ver = 0x03
        self.cnt = 0x0
        self.ttl = 0x05

        self.sdp = sd.SD()
        self.cap = cv2.VideoCapture(0)
        self.set_array()

    def set_array(self):
        # type default: 0x06 (Subscribe Event Group), service id = 0x1111, instance id = 0xffff,
        # ttl: 5 sec, event group id = 0x04
        entry_array = [sd.SDEntry_EventGroup(srv_id=self.service_id, n_opt_1=self.n_opt_1, inst_id=self.inst_id,
                                             major_ver=self.major_ver,
                                             eventgroup_id=self.eventgroup_id, cnt=self.cnt,
                                             ttl=self.ttl)]
        self.sdp.setEntryArray(entry_array)
        self.sdp.entry_array[0].type = None

        option_array = [sd.SDOption_IP4_EndPoint(addr="192.168.0.7", l4_proto=0x11, port=0xd903)]
        self.sdp.setOptionArray(option_array)

    def receive(self, msg):
        sippacket = bytes(msg[UDP].payload)
        self.sdp.entry_array[0].type = int.from_bytes(sippacket[24:25], byteorder='little')

        try:
            data = sippacket[56:].decode()
            print(data)

        except UnicodeDecodeError:
            pass

        finally:
            self.comm()

    def comm(self):
        p = Ether() / IP(src='192.168.0.13', dst='192.168.0.7') / UDP(sport=138, dport=5355) / self.sdp.getSomeip(True)

        if self.sdp.entry_array[0].type is None:
            print('Waiting For Find Service Request...')

        elif self.sdp.entry_array[0].type == sd.SDEntry_Service.TYPE_SRV_FINDSERVICE:  # offer service
            p['SD'].entry_array[0].type = sd.SDEntry_Service.TYPE_SRV_OFFERSERVICE
            print("Receiving Find Service")
            print("Sending Offer Service")
            sendp(p, count=1)

        elif self.sdp.entry_array[0].type == sd.SDEntry_EventGroup.TYPE_EVTGRP_SUBSCRIBE:  # Subscribe EventGroup
            p['SD'].entry_array[0].type = sd.SDEntry_Service.TYPE_EVTGRP_SUBSCRIBE_ACK
            print("Receiving Subscribe EventGroup")
            print("Sending SubScribe EventGroup ACK")
            sendp(p, count=1)

        elif self.sdp.entry_array[0].type == sd.SDEntry_Service.TYPE_EVTGRP_SUBSCRIBE_ACK:
            print('Now Sending UDP Event Payload')
            _, img = self.cap.read()
            self.processing(img)
            p.add_payload(self.event_string)
            sendp(p, count=1)


if __name__ == '__main__':
    srv = face_recognition()
    srv.comm()
    sniff(count=0, prn=srv.receive, filter='udp port 5355')
