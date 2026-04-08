import socket
import keyboard

HOST = '127.0.0.1'  
PORT = 9002        

def start_controller():
   
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[KeyboardCapture]Connecting to {HOST}...")
        try:
            s.bind((HOST, PORT))
            s.listen()
            print(f"[KeyboardCapture]Executor listening on {PORT}... Waiting for Controller.")
        
            conn, addr = s.accept()
            
            
           
            def on_key_event(event):
                if event.event_type == keyboard.KEY_DOWN:
                  
                    conn.sendall(f"{event.name}\n".encode('utf-8'))
            
            
            keyboard.hook(on_key_event)
            
            
            keyboard.wait('esc')
            
        except ConnectionRefusedError:
            print("[KeyboardCapture]Error: Could not connect. Is the Executor running?")

if __name__ == "__main__":
    start_controller()                                                                                                      