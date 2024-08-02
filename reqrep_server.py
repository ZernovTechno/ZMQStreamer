import zmq
import numpy
import cv2
import base64
import pyautogui
import socket
import segno
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
r = s.getsockname()[0]
s.close()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:12345")

if __name__ == "__main__":
    qrcode = segno.make_qr(r)
    qrcode.show()
    while True:
        message_rx = socket.recv()
    
        retval, buffer = cv2.imencode('.jpg', cv2.resize(cv2.cvtColor(numpy.array(pyautogui.screenshot()),cv2.COLOR_RGB2BGR), (1920, 1080)), [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        socket.send(base64.b64encode(buffer))