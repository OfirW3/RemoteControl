import socket
import keyboard


HOST = '127.0.0.1' 
PORT = 9002

def start_executor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("[keyboardExecute]Connected! Start typing...")
        with s:
           
            buffer = ""
            while True:
                data = s.recv(1024).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                
                if '\n' in buffer:
                    keys = buffer.split('\n')
                    
                    for key in keys[:-1]:
                        if key:
                            print(f"[keyboardExecute]Executing: {key}")
                            try:
                                keyboard.press_and_release(key)
                            except ValueError:
                                
                                pass
                    buffer = keys[-1]

if __name__ == "__main__":
    start_executor()