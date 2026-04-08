
from threading import Thread
import queue
import GetImages
from mouseCapture import CoordinateSenderApp
import KeyboardCapture
def main():
    image_queue = queue.Queue()

    server = GetImages.start()
    images =Thread(target=GetImages.listen_loop,args=(server, image_queue),daemon=True)
    app = CoordinateSenderApp(host="127.0.0.1", port=9000,image_queue=image_queue)
    tk_app = Thread(target=app.run,daemon=True)
    keyboard =Thread(target=KeyboardCapture.start_controller() , daemon=True)

    tk_app.start()
    images.start()
    keyboard.start()

    tk_app.join()
    images.join()
    keyboard.join()



if __name__ == "__main__":
    main()
