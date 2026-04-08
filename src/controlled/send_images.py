import socket
import time
from PIL import ImageGrab
from io import BytesIO
import tkinter as tk

def send_image(sock):
    

  
    img = ImageGrab.grab()
    
    
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=70, optimize=True)#bytesIO saves to RAM
    data = buffer.getvalue()
    buffer.close()

    
    size = len(data)#mini-protocol, size header
    sock.sendall(size.to_bytes(8, "big"))

    
    sock.sendall(data)
    
    print(f"[SendImages]image sent ({size} bytes)")

def connect(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

    
def start():
        host = "127.0.0.1"
        port = 9001

        sock = connect(host, port)
        while True:
            send_image(sock)
            time.sleep(0.5)

if __name__ == "__main__":
    start()

