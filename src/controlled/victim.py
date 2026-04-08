from threading import Thread
import MouseExecute
import SendImages
import KeyboardExecute

def main():
    
    mouse = Thread(target=MouseExecute.start, daemon=True)
    sender = Thread(target=SendImages.start, daemon=True)
    keyboard  = Thread(target=KeyboardExecute.start_executor() ,daemon=True)
    mouse.start()
    sender.start()
    keyboard.start()


    mouse.join()
    sender.join()
    keyboard.join()

if __name__ == "__main__":
    main()