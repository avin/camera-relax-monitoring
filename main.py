import cv2
import threading
import cvlib as cv
import time
import window
from queue import Queue

SLEEP_TIME = 10  # 10sec
SCREEN_TIME = 1800 / SLEEP_TIME  # 30min
ADD_MORE_TIME = 300 / SLEEP_TIME  # 5min
RELAX_TIME = 180 / SLEEP_TIME  # 3min
ENABLE_GPU = not not cv2.cuda.getCudaEnabledDeviceCount()

SLEEP_TIME = .5  # 10sec
SCREEN_TIME = 30  # 30min
ADD_MORE_TIME = 10  # 5min
RELAX_TIME = 10  # 3min

print(f'ENABLE_GPU={ENABLE_GPU}')

# -----------------------------------------------------------

notification_shown = False
in_camera_count = 0
off_camera_count = 0


def video_analysis(message_queue):
    global in_camera_count, off_camera_count, notification_shown
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        if not ret:
            continue

        bbox, label, conf = cv.detect_common_objects(frame, model='yolov4-tiny', enable_gpu=ENABLE_GPU)
        if 'person' in label:
            print("Человек обнаружен в кадре.", in_camera_count, off_camera_count)
            if not notification_shown:
                in_camera_count += 1
                off_camera_count = max(off_camera_count - 1, 0)
            if in_camera_count >= SCREEN_TIME and not notification_shown:
                in_camera_count = 0
                off_camera_count = 0
                message_queue.put("show")
                notification_shown = True
        else:
            print("Человека нет в кадре.", in_camera_count, off_camera_count)
            off_camera_count += 1
            in_camera_count = max(in_camera_count - 1, 0)
            if notification_shown and off_camera_count >= RELAX_TIME:
                off_camera_count = 0
                message_queue.put("hide")
                notification_shown = False
            if not notification_shown and off_camera_count >= RELAX_TIME:
                off_camera_count = 0
                in_camera_count = 0

        time.sleep(SLEEP_TIME)


def add_more_time(root):
    global in_camera_count, off_camera_count, notification_shown
    global SCREEN_TIME, ADD_MORE_TIME
    in_camera_count = SCREEN_TIME - ADD_MORE_TIME
    notification_shown = False
    root.withdraw()


if __name__ == "__main__":
    message_queue = Queue()

    root = window.create_window(add_more_time)

    # Запуск потока управления окном
    window_thread = threading.Thread(target=window.manage_window, args=(root, message_queue))
    window_thread.daemon = True
    window_thread.start()

    # Запуск потока счётчика
    video_analysis_thread = threading.Thread(target=video_analysis, args=(message_queue,))
    video_analysis_thread.daemon = True
    video_analysis_thread.start()

    # Запуск главного цикла Tkinter в основном потоке
    root.mainloop()
