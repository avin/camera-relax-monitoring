import cv2
import threading
import cvlib as cv
import time
import tkinter as tk
from queue import Queue

# SLEEP_TIME = 10  # 10sec
# SCREEN_TIME = 1800 / SLEEP_TIME  # 30min
# ADD_MORE_TIME = 300 / SLEEP_TIME  # 5min
# RELAX_TIME = 180 / SLEEP_TIME  # 3min
# ENABLE_GPU = True

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
    in_camera_count = SCREEN_TIME - ADD_MORE_TIME
    notification_shown = False
    root.withdraw()


def manage_window(root, message_queue):
    while True:
        message = message_queue.get()
        if message == "show":
            root.deiconify()
        elif message == "hide":
            root.withdraw()


def center_window(root, width=600, height=600):
    # Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Вычисляем координаты для центрирования окна
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Устанавливаем размеры и позицию окна
    root.geometry(f'{width}x{height}+{x}+{y}')


def create_window():
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.attributes("-topmost", True)
    root.attributes("-toolwindow", True)
    root.title("Напоминание о перерыве")

    label = tk.Label(root, text="Сделай перерыв", font=("Arial", 24))
    label.pack(expand=True)

    button = tk.Button(root, text="Еще 5 минуток", font=("Arial", 14), command=lambda: add_more_time(root))
    button.pack(pady=20)

    root.geometry("600x600")

    center_window(root)
    root.withdraw()  # Сначала окно будет скрыто

    return root


if __name__ == "__main__":
    message_queue = Queue()

    root = create_window()

    # Запуск потока управления окном
    window_thread = threading.Thread(target=manage_window, args=(root, message_queue))
    window_thread.daemon = True
    window_thread.start()

    # Запуск потока счётчика
    video_analysis_thread = threading.Thread(target=video_analysis, args=(message_queue,))
    video_analysis_thread.daemon = True
    video_analysis_thread.start()

    # Запуск главного цикла Tkinter в основном потоке
    root.mainloop()
