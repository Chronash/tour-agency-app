
import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import register
from views import login_page

def center_window(root, width=400, height=500):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def open_register(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#2e2e2e")
    center_window(root)

    frame = tk.Frame(root, bg="#2e2e2e")
    frame.pack(expand=True)

    tk.Label(frame, text="Регистрация", font=("Arial", 16), bg="#2e2e2e", fg="white").pack(pady=10)

    tk.Label(frame, text="Логин", bg="#2e2e2e", fg="white").pack()
    username_entry = tk.Entry(frame, bg="#444444", fg="white", insertbackground="white")
    username_entry.pack()

    tk.Label(frame, text="Пароль", bg="#2e2e2e", fg="white").pack()
    password_entry = tk.Entry(frame, show="*", bg="#444444", fg="white", insertbackground="white")
    password_entry.pack()

    tk.Label(frame, text="Тип питания", bg="#2e2e2e", fg="white").pack()
    food_entry = tk.Entry(frame, bg="#444444", fg="white", insertbackground="white")
    food_entry.pack()

    tk.Label(frame, text="Аллергии", bg="#2e2e2e", fg="white").pack()
    allergy_entry = tk.Entry(frame, bg="#444444", fg="white", insertbackground="white")
    allergy_entry.pack()

    def on_register():
        success, msg = register(
            username_entry.get(),
            password_entry.get(),
            food_entry.get(),
            allergy_entry.get()
        )
        if success:
            messagebox.showinfo("Готово", msg)
            login_page.open_login(root)
        else:
            messagebox.showerror("Ошибка", msg)

    tk.Button(frame, text="Зарегистрироваться", command=on_register, bg="#666666", fg="white").pack(pady=10)
    tk.Button(frame, text="Назад", command=lambda: login_page.open_login(root), bg="#666666", fg="white").pack(pady=5)
