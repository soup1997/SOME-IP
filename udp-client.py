import socket
import numpy as np
import cv2

UDP_IP = "192.168.0.13"
UDP_PORT = 49593
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
# 640 x 480 x 3 = 921,600 Byte
s = [b'\xff' * 46080 for x in range(20)] # 921,600 / 20 = 46,080 Byte
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))

while True:
    picture = b''
    data, addr = sock.recvfrom(46081)
    s[data[0]] = data[1:46081]

    if data[0] == 19:
        for i in range(20):
            picture += s[i]
        frame = np.fromstring(picture, dtype=np.uint8)
        frame = frame.reshape(480, 640, 3)
        cv2.imshow("frame", frame)# 비디오 출력
        out.write(frame)# 프레임 저장
        if cv2.waitKey(1) & 0xFF == ord('q'): # 'q' 누르면 종료
            cv2.destroyAllWindows()
            break