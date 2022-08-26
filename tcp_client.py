import socket
import cv2
import numpy as np

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

HOST = '192.168.0.13'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket_created')
s.bind((HOST, PORT))
print('socket bind complete')

s.listen(1)
print('socket now listening')

conn, addr = s.accept()

while True:
    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = np.frombuffer(stringData, dtype=np.uint8)

    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)