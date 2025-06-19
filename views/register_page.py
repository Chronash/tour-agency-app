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
    tk.Label(root, text="Тип питания").pack()
    food_entry = tk.Entry(root)
    food_entry.pack()
    tk.Label(root, text="Аллергии").pack()
    allergy_entry = tk.Entry(root)
    allergy_entry.pack()


    def on_register():
        username_val = username.get()
        password_val = password.get()
        food_val = food_entry.get()
        allergy_val = allergy_entry.get()
        success, msg = register(username_val, password_val, food_val, allergy_val)
        if success:
            messagebox.showinfo("Успех", msg)
            login_page.open_login(root)
        else:
            messagebox.showerror("Ошибка", msg)

    tk.Button(root, text="Зарегистрироваться", command=on_register).pack(pady=5)
    tk.Button(root, text="Назад", command=lambda: login_page.open_login(root)).pack()
