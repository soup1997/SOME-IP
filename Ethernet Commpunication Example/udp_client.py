import socket
import cv2

UDP_IP = '192.168.0.13'
UDP_PORT = 49593

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = frame.flatten().tobytes()
    
    for i in range(20):
        sock.sendto(bytes([i]) + frame[i * 46080:(i+1) * 46080], (UDP_IP, UDP_PORT))
        
    if cv2.waitKey(1) & 0xff == ord('q'):
        break