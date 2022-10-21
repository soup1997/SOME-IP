from scapy.all import *
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether
import eth_scapy_someip as someip
import numpy as np
import cv2
import sys, keyboard


# Header 패키지 생성
def MakeSOMEIPPackage():
    package = someip.SOMEIP()
    # Message ID
    package.msg_id.srv_id = 0xffff  # Service ID [16bits]
    package.msg_id.sub_id = 0x00
    package.msg_id.method_id = 0x0000  # Method ID [16bits]

    # Request ID
    package.req_id.client_id = 0xdead  # Client ID [16bits]
    package.req_id.session_id = 0xbeef  # Session ID [16bits]

    package.msg_type = 0x01  # Message Type [8bits] -- TYPE_REQUEST
    package.retcode = 0x00  # Return Code [8bits] -- RET_E_OK

    return package


# stack 생성
def MakeEthPackage():
    package = Ether() / IP(src="192.168.0.13", dst="192.168.0.7") / UDP(sport=138,
                                                                          dport=5900) / MakeSOMEIPPackage()  # com vs com
    return package

cap = cv2.VideoCapture(0)
ext = 7
print('Space to start, q to stop')
while True:
    key_value = keyboard.read_key()
    if key_value == 'space':
        while cap.isOpened():
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            # frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
            frame = cv2.resize(frame, (100, 100), interpolation=cv2.INTER_CUBIC)
            b_frame, g_frame, r_frame = cv2.split(frame)
            b_frame_flatten = b_frame.reshape(-1)  # flatten , reshape, ravel 중 flatten 은 값복사가 이루어져 메모리가 불안하다.
            g_frame_flatten = g_frame.reshape(-1)  # flatten , reshape, ravel 중 flatten 은 값복사가 이루어져 메모리가 불안하다.
            r_frame_flatten = r_frame.reshape(-1)  # flatten , reshape, ravel 중 flatten 은 값복사가 이루어져 메모리가 불안하다.

            a = np.array_split(b_frame_flatten, ext)  # b_frame_flatten을 동일한 길이의 7개의 배열로 나눔
            b = np.array_split(g_frame_flatten, ext)  # g_frame_flatten을 동일한 길이 7개의 배열로 나눔
            c = np.array_split(r_frame_flatten, ext)  # r_frame_flatten을 동일한 길이 7개의 배열로 나눔

            for i in range(ext):
                a[i] = np.insert(arr=a[i], obj=0, values=i)  # a[i]에 0번 인덱스를 가지는 곳에 i값을 넣는다.
                print(len(a[i]))
                package10 = MakeEthPackage()  # UDP 프로토콜 객체 생성
                package10.add_payload(bytes(a[i]))  # payload에 a[i]를 추가
                sendp(package10, count=1)  # 1 패킷씩 전송 시작

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        break

cv2.destroyAllWindows()
sys.exit()