import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import login
from views import register_page, user_main, admin_panel


def open_login(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Логин").pack()
    username = tk.Entry(root)
    username.pack()
    tk.Label(root, text="Пароль").pack()
    password = tk.Entry(root, show="*")
    password.pack()

    def on_login():
        user = login(username.get(), password.get())
        if user:
            messagebox.showinfo("Успех", f"Добро пожаловать, {user['username']}!")
            if user['role'] == "admin":
                admin_panel.open_admin_panel(root)
            else:
                user_main.open_user_main(root,user)
        else:
            messagebox.showerror("Ошибка", "Неверные данные")

    tk.Button(root, text="Войти", command=on_login).pack(pady=5)
    tk.Button(root, text="Регистрация", command=lambda: register_page.open_register(root)).pack()
