import tkinter as tk
import time
import random

# Inisialisasi
current_dot = 0
start_time = None
valid_attempt = True
last_mouse_move_time = None

def start_captcha():
    global start_time, valid_attempt, last_mouse_move_time
    start_time = time.time()
    last_mouse_move_time = time.time()
    valid_attempt = True
    root.after(15000, force_exit)  # Setelah 15 detik, panggil fungsi force_exit
    root.after(5000, check_mouse_movement)  # Setelah 5 detik, panggil fungsi check_mouse_movement

def force_exit():
    global valid_attempt
    if valid_attempt:
        print("CAPTCHA failed! Time exceeded.")
        valid_attempt = False
        root.quit()

def on_paint(event):
    global current_dot, start_time, valid_attempt
    last_mouse_move_time = time.time()

    if valid_attempt:
        canvas.create_oval(event.x - 6, event.y - 6, event.x + 6, event.y + 6, fill="black")

        # Periksa apakah posisi klik mendekati titik yang benar
        target_dot = dots_to_follow[current_dot]
        if abs(event.x - target_dot[0]) < 6 and abs(event.y - target_dot[1]) < 6:
            canvas.create_text(target_dot[0], target_dot[1], text=str(current_dot + 1), font=("Arial", 8), fill="black")
            current_dot += 1
            if current_dot == len(dots_to_follow):
                print("CAPTCHA passed!")
                root.quit()
    else:
        print("CAPTCHA failed! Invalid attempt.")
        root.quit()

def on_release(event):
    global valid_attempt
    if valid_attempt and current_dot != len(dots_to_follow):
        print("CAPTCHA failed! Released mouse prematurely.")
        valid_attempt = False
        root.quit()

    # Stop the validation if CAPTCHA already failed due to time exceeding
    if not valid_attempt:
        root.quit()

def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def check_mouse_movement():
    global last_mouse_move_time, valid_attempt
    current_time = time.time()
    if current_time - last_mouse_move_time >= 5:
        print("CAPTCHA failed! Mouse idle for 5 seconds.")
        valid_attempt = False
        root.quit()
    else:
        root.after(5000, check_mouse_movement)  # Cek lagi setelah 5 detik

root = tk.Tk()
root.title("CAPTCHA - Draw the pattern")

# Menyesuaikan ukuran jendela
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

canvas.create_text(200, 20, text="Draw the pattern", font=("Arial", 12))

# Titik-titik untuk diikuti oleh pengguna
dots_to_follow = []
for idx in range(4):
    x = random.randint(20, 380)  # Batasan kanvas horizontal
    y = random.randint(20, 280)  # Batasan kanvas vertikal
    if idx == 0:
        dot_color = "green"  # Warna titik pertama
    elif idx == 3:
        dot_color = "red"   # Warna titik keempat
    else:
        dot_color = "yellow"  # Warna titik-titik lainnya
        # Validasi jarak dari titik-titik sebelumnya
        valid_position = False
        while not valid_position:
            valid_position = True
            for dot in dots_to_follow:
                if distance(dot, (x, y)) < 20:  # Jarak minimal antara titik-titik
                    valid_position = False
                    x = random.randint(20, 380)  # Coba posisi baru
                    y = random.randint(20, 280)
                    break
    dots_to_follow.append((x, y))
    canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill=dot_color)
    canvas.create_text(x, y, text=str(len(dots_to_follow)), font=("Arial", 8), fill="black")

canvas.bind("<Button-1>", lambda event: start_captcha())
canvas.bind("<B1-Motion>", on_paint)
canvas.bind("<ButtonRelease-1>", on_release)

root.mainloop()
