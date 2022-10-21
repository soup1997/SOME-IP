import cv2
import socket
import numpy as np

TCP_IP = '192.168.0.13'
TCP_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

capture = cv2.VideoCapture(0)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
q
while True:
    ret, frame = capture.read()
    
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    frame = np.array(frame).tobytes()
    
    sock.sendall((str(len(frame))).encode().ljust(16)+frame)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
capture.release()
