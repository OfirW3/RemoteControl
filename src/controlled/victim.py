from threading import Thread
import RemoteControl.remote_control.controlled.mouse_execute as mouse_execute
import RemoteControl.remote_control.controlled.send_images as send_images
import RemoteControl.remote_control.controlled.keyboard_execute as keyboard_execute

def main():
    
    mouse = Thread(target=mouse_execute.start, daemon=True)
    sender = Thread(target=send_images.start, daemon=True)
    keyboard  = Thread(target=keyboard_execute.start_executor() ,daemon=True)
    mouse.start()
    sender.start()
    keyboard.start()


    mouse.join()
    sender.join()
    keyboard.join()

if __name__ == "__main__":
    main()