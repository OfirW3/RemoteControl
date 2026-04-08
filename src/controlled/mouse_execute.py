import win32api
import win32con
import socket

def click(x, y):
    
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    print(f"[MouseExecute]Mouse clicked at x={x}, y={y}")

def start():
    host = '127.0.0.1'
    port = 9000

   
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    print(f"[MouseExecute] Connected")
        
    

    while True:
        data = sock.recv(1024)
        if not data:
            print("[MouseExecute]server disconnected")
            break
        try:
            decoded = data.decode().strip()
            
            if "," in decoded:
                x_str, y_str = decoded.split(",", 1)
                x, y = int(x_str), (int(y_str)+50)
                click(x, y)
            else:
                print(f"[MouseExecute]Invalid data format: {decoded}")
        except ValueError:                
           print(f"[MouseExecute]Invalid data received: {decoded}")



