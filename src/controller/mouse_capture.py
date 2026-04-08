# coordinate_sender.py
import tkinter as tk
import socket
from threading import Thread
import queue
from PIL import Image, ImageTk
import os
import time

class CoordinateSenderApp:
    def __init__(self, host, port, image_queue=None, sock_connect_timeout=5):
        self.host = host
        self.port = port
        self.image_queue = image_queue or queue.Queue()

        # socket setup (unchanged)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.server.bind((host, port))
            self.server.listen(1)
            print(f"[CoordinateSenderApp]Listening on {host}:{port}...")
            
        except Exception as e:
            print("[CoordinateSenderApp] server problem:", e)

        self.send_queue = queue.Queue()
        self.running = True

        # GUI
        self.root = tk.Tk()
        self.root.title("Controler")

        frame = tk.LabelFrame(self.root, labelanchor=tk.S, text="00|00")
        frame.grid(row=0, column=0, sticky=tk.NSEW)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(frame, width=screen_width, height=screen_height - 100)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.canvas.bind("<Button-1>", self._on_click)

        
        self.imageId = None
        self.tk_img = None

        # start image polling
        self.root.after(30, self.check_new_image)

        # sender thread
        Thread(target=self.sender_loop, daemon=True).start()

        print("[CoordinateSenderApp] init complete")

    def check_new_image(self):
        latest = None
        try:
            while True:
                latest = self.image_queue.get_nowait()
                print("[UI] got image from queue")  
        except queue.Empty:
            pass

        if latest is not None:
            self.tk_img = ImageTk.PhotoImage(latest)

            if self.imageId is None:
                # first image create canvas item
                self.imageId = self.canvas.create_image(
                    self.canvas.winfo_width() // 2,
                    self.canvas.winfo_height() // 2,
                    image=self.tk_img,
                    anchor=tk.CENTER
                )
            else:
                # update existing image
                self.canvas.itemconfig(self.imageId, image=self.tk_img)

        self.root.after(30, self.check_new_image)
    def _on_click(self, event):
        
        x, y = event.x, event.y
        self.send_queue.put((x, y))
        
        print(f"[CoordinateSenderApp] click: {x},{y}")
        return x, y

    def sender_loop(self):
        
        while True:
            print("Waiting for a connection...")
            conn, addr = self.server.accept()
            print(f"Connection from {addr}")
            while self.running:
                
                x, y = self.send_queue.get()  # blocking
                msg = f"{x},{y}\n".encode("utf-8")
                try:
                    conn.sendall(msg)
                    print("[CoordinateSenderApp] sent cords", x, y)
                except Exception as e:
                    print("[CoordinateSenderApp] Socket send error:", e)
                    time.sleep(0.5)

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop() 
        

    def on_close(self):
        self.running = False
        try:
            self.server.close()
        except:
            pass
        self.root.destroy()
