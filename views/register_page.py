import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import register

from views import login_page

def open_register(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Новый логин").pack()
    username = tk.Entry(root)
    username.pack()
    tk.Label(root, text="Новый пароль").pack()
    password = tk.Entry(root, show="*")
    password.pack()

    def on_register():
        success, msg = register(username.get(), password.get())
        if success:
            messagebox.showinfo("Успех", msg)
            login_page.open_login(root)
        else:
            messagebox.showerror("Ошибка", msg)

    tk.Button(root, text="Зарегистрироваться", command=on_register).pack(pady=5)
    tk.Button(root, text="Назад", command=lambda: login_page.open_login(root)).pack()
