import zmq
import numpy as np
import cv2
import base64
import pyautogui
import socket
import segno
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

# Определяем IP-адрес
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
r = s.getsockname()[0]
s.close()

# Создаем контекст и сокет для ZeroMQ
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:12345")  # Порт оставляем без изменений

# Создаем QR-код
qrcode = segno.make_qr(r)

# Сохраняем QR-код в файл
qrcode_file = 'qrcode.png'
qrcode.save(qrcode_file, scale=10)  # Увеличиваем размер QR-кода

# Функция для отображения QR-кода и видеопотока
def show_qrcode():
    root = tk.Tk()
    root.title("QR Code and Video Stream")
    root.geometry("800x400")

    # Панель для разделения окна
    paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Панель для QR-кода
    qrcode_frame = tk.Frame(paned_window, width=800)
    qrcode_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
    paned_window.add(qrcode_frame)

    # Панель для видеопотока и лога
    video_frame = tk.Frame(paned_window, width=100)
    video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    paned_window.add(video_frame)

    # Открываем изображение QR-кода с использованием Pillow
    qr_img_pil = Image.open(qrcode_file)
    qr_img_tk = ImageTk.PhotoImage(qr_img_pil)

    # Создаем и добавляем виджет с изображением QR-кода
    label_qrcode = tk.Label(qrcode_frame, image=qr_img_tk)
    label_qrcode.photo = qr_img_tk  # Сохраняем ссылку, чтобы избежать сборки мусора
    label_qrcode.pack(fill=tk.BOTH, expand=True)

    # Создаем виджет для отображения видеопотока
    label_video = tk.Label(video_frame)
    label_video.pack(fill=tk.BOTH, expand=True)

    # Создаем виджет для отображения лога
    log_label = tk.Label(video_frame, text="Лог трансляции:")
    log_label.pack(anchor='n')  # Прижимаем к верхнему краю

    # Создаем текстовое поле для лога и прижимаем его к верхнему краю
    log_text = tk.Text(video_frame, font=("Helvetica", 12))
    log_text.pack(fill=tk.BOTH, expand=True)
    log_text.pack_propagate(False)  # Отключаем автоматическое изменение размера

    # Функция для обновления лога
    def update_log(message):
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)  # Прокручиваем лог до последней строки

    # Обновляем изображение видеопотока
    def update_video():
        frame_counter = 0  # Счётчик кадров
        while True:
            try:
                # Захват экрана
                screenshot = np.array(pyautogui.screenshot())
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
                resized_screenshot = cv2.resize(screenshot, (1024, 600))

                # Получаем координаты мыши
                mouse_x, mouse_y = pyautogui.position()

                # Рисуем круг в позиции мыши
                cv2.circle(resized_screenshot, (mouse_x, mouse_y), 10, (0, 255, 0), 2)
                
                # Кодирование изображения в JPEG
                retval, buffer = cv2.imencode('.jpg', resized_screenshot, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                if retval:
                    encoded_image = base64.b64encode(buffer)

                    # Проверяем, есть ли запрос
                    if not socket.poll(timeout=1000):  # Проверяем, есть ли запрос в течение 1 секунды
                        continue  # Если нет, продолжаем без отправки
                    message_rx = socket.recv()
                    socket.send(encoded_image)

                    # Увеличиваем счетчик кадров и обновляем лог
                    frame_counter += 1
                    update_log(f"Изображение #{frame_counter} отправлено в {time.strftime('%H:%M:%S')}")

            except Exception as e:
                update_log(f"Ошибка: {e}")

            time.sleep(0.1)  # Обновляем каждые 0.1 секунды для более плавного видеопотока

    # Запускаем поток обновления видеопотока
    video_thread = threading.Thread(target=update_video, daemon=True)
    video_thread.start()

    # Запускаем главный цикл событий Tkinter
    root.mainloop()

# Запускаем GUI и сервер в отдельных потоках
def start_threads():
    # Поток для отображения QR-кода
    gui_thread = threading.Thread(target=show_qrcode, daemon=True)
    gui_thread.start()

    # Запускаем главный цикл, поток GUI будет работать в основном процессе
    gui_thread.join()

# Запускаем GUI
start_threads()
