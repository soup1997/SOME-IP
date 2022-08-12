from scapy.all import *
import eth_scapy_sd as sd
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether
import cv2


class event_group:
    def __init__(self):
        self.eventgroup_id = 0x04
        self.detected_check = ''

    def event_1(self):
        self.detected_check = 'face detected!'

    def event_2(self):
        self.detected_check = 'face not detected!'

    def pipeline(self, img):
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


class face_recognition(event_group):
    def __init__(self):
        super().__init__()
        self.service_id = 0x1111
        self.n_opt_1 = 1
        self.inst_id = 0xffff
        self.major_ver = 0x03
        self.cnt = 0x0
        self.ttl = 0x05
        self.control_flag = False

        self.sdp = sd.SD()

    def set_entry(self):
        # reboot flag = 0, unicast flag = 0, explicit initial data flag = 0, 나머지 비트는 무시
        self.sdp.flags = 0x00

        # type default: 0x06 (Subscribe Event Group), service id = 0x1111, instance id = 0xffff,
        # ttl: 5 sec, event group id = 0x04
        self.sdp.entry_array = [
            sd.SDEntry_EventGroup(srv_id=self.service_id, n_opt_1=self.n_opt_1, inst_id=self.inst_id,
                                  major_ver=self.major_ver,
                                  eventgroup_id=self.eventgroup_id, cnt=self.cnt,
                                  ttl=self.ttl)]

        # type default: 0x06 (Subscribe Event Group), service id = 0x1111, instance id = 0xffff,
        # ttl: 5 sec, event group id = 0x04
        self.sdp.option_array = [
            sd.SDOption_IP4_EndPoint(addr="192.168.0.116", l4_proto=0x11, port=0xd903)]

if __name__ == '__main__':
    srv = face_recognition()
    srv.set_entry()
    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()
        srv.pipeline(img)
        p = Ether() / IP(src='192.168.0.13', dst='192.168.0.116') / UDP(sport=138, dport=5355) / srv.sdp.getSomeip(True)
        p.add_payload(srv.detected_check)
        sendp(p, count=1)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break
