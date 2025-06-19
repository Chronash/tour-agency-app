import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import login
from views import register_page, user_main, admin_panel

def style_widget(widget, bg="#2e2e2e", fg="#ffffff", font=("Arial", 12)):
    widget.configure(bg=bg, fg=fg, font=font)

def open_login(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#2e2e2e")

    frame = tk.Frame(root, bg="#2e2e2e")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title = tk.Label(frame, text="Вход в систему", bg="#2e2e2e", fg="#ffffff", font=("Arial", 16, "bold"))
    title.pack(pady=(0, 10))

    tk.Label(frame, text="Логин", bg="#2e2e2e", fg="#ffffff").pack()
    username = tk.Entry(frame, bg="#444444", fg="#ffffff", insertbackground="#ffffff")
    username.pack()

    tk.Label(frame, text="Пароль", bg="#2e2e2e", fg="#ffffff").pack()
    password = tk.Entry(frame, show="*", bg="#444444", fg="#ffffff", insertbackground="#ffffff")
    password.pack()

    def on_login():
        user = login(username.get(), password.get())
        if user:
            messagebox.showinfo("Успех", f"Добро пожаловать, {user['username']}!")
            if user['role'] == "admin":
                admin_panel.open_admin_panel(root)
            else:
                user_main.open_user_main(root, user)
        else:
            messagebox.showerror("Ошибка", "Неверные данные")

    tk.Button(frame, text="Войти", command=on_login, bg="#555555", fg="#ffffff").pack(pady=5)
    tk.Button(frame, text="Регистрация", command=lambda: register_page.open_register(root),
              bg="#555555", fg="#ffffff").pack(pady=2)