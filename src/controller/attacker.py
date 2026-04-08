
from threading import Thread
import queue
import remote_control.src.controller.get_images as get_images
from remote_control.src.controller.mouse_capture import CoordinateSenderApp
import remote_control.src.controller.keyboard_capture as keyboard_capture
def main():
    image_queue = queue.Queue()

    server = get_images.start()
    images =Thread(target=get_images.listen_loop,args=(server, image_queue),daemon=True)
    app = CoordinateSenderApp(host="127.0.0.1", port=9000,image_queue=image_queue)
    tk_app = Thread(target=app.run,daemon=True)
    keyboard =Thread(target=keyboard_capture.start_controller() , daemon=True)

    tk_app.start()
    images.start()
    keyboard.start()

    tk_app.join()
    images.join()
    keyboard.join()



if __name__ == "__main__":
    main()
