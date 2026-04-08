import socket
from PIL import Image
from io import BytesIO

def start(host="127.0.0.1", port=9001):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print(f"[get_images] Listening on {host}:{port}")
    return server

def listen_loop(server, image_queue):
   
    while True:
        conn, addr = server.accept()
        print(f"[get_images] Connection from {addr}")
        try:
            while True:
                
                size_data = conn.recv(8) # recive size header(mini protocol)
                if not size_data:
                    print("[get_images] client disconnected")
                    break

                image_size = int.from_bytes(size_data, "big")
                data = b""
                while len(data) < image_size:
                    packet = conn.recv(min(4096, image_size - len(data)))
                    if not packet:
                        break
                    data += packet

                if len(data) < image_size:
                    print("[get_images] incomplete frame, closing connection")
                    break

                
                img = Image.open(BytesIO(data)).convert("RGB")
                print("[get_images] pushing image to queue")
                image_queue.put(img)
                
        except Exception as e:
            print("[get_images] error:", e)
        finally:
            conn.close()
            print("[get_images] connection closed, waiting for next connection")
