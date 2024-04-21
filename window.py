import tkinter as tk

# Глобальные переменные для отслеживания начальных координат
start_x = 0
start_y = 0
start_win_x = 0
start_win_y = 0


def on_press(event, root):
    global start_x, start_y, start_win_x, start_win_y
    start_x = event.x_root
    start_y = event.y_root
    start_win_x = root.winfo_x()
    start_win_y = root.winfo_y()


def on_drag(event, root):
    global start_x, start_y, start_win_x, start_win_y
    # Используем глобальные переменные для вычисления смещения
    dx = event.x_root - start_x
    dy = event.y_root - start_y

    x = start_win_x + dx
    y = start_win_y + dy
    root.geometry(f"+{x}+{y}")


def manage_window(root, message_queue):
    while True:
        message = message_queue.get()
        if message == "show":
            root.deiconify()
        elif message == "hide":
            root.withdraw()


def center_window(root, width=600, height=370):
    # Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Вычисляем координаты для центрирования окна
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Устанавливаем размеры и позицию окна
    root.geometry(f'{width}x{height}+{x}+{y}')


def toggle_color(border_frame, current_color, color1, color2, interval):
    # Определяем новый цвет на основе текущего цвета
    new_color = color1 if current_color == color2 else color2
    # Устанавливаем новый цвет фона рамки
    border_frame.configure(bg=new_color)
    # Через 250 мс снова переключаем цвет
    border_frame.after(interval, toggle_color, border_frame, new_color, color1, color2, interval)


def create_window(add_more_time_cb):
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.attributes("-topmost", True)
    root.attributes("-toolwindow", True)
    root.title("Напоминание о перерыве")

    root.overrideredirect(True)

    border_width = 5
    border_initial_color = "#238551"  # Начальный цвет
    border_alternate_color = "#72CA9B"  # Цвет, на который переключаемся

    # Создаем рамку с красным фоном, которая действует как обводка
    border_frame = tk.Frame(root, bg=border_initial_color, bd=border_width)
    border_frame.pack(expand=True, fill=tk.BOTH)  # Растягиваем рамку, чтобы она охватывала все окно

    # Начинаем мигание рамки
    interval = 250  # Интервал 250 мс
    toggle_color(border_frame, border_initial_color, border_initial_color, border_alternate_color, interval)

    # Содержимое окна внутри рамки
    inner_frame = tk.Frame(border_frame, bg="#F6F7F9")  # Фон внутренней рамки может быть любым
    inner_frame.pack(expand=True, fill=tk.BOTH, padx=border_width, pady=border_width)

    label = tk.Label(inner_frame, text="Сделай перерыв", font=("Arial", 24), bg="#F6F7F9")
    label.pack(expand=True)

    for element in (border_frame, inner_frame, label):
        element.bind("<ButtonPress-1>", lambda event: on_press(event, root))
        element.bind("<B1-Motion>", lambda event: on_drag(event, root))

    button = tk.Button(inner_frame, text="Еще 5 минуток", font=("Arial", 14), bg="#E5E8EB",
                       command=lambda: add_more_time_cb(root))
    button.pack(pady=20)

    center_window(root)
    root.withdraw()  # Сначала окно будет скрыто

    return root
