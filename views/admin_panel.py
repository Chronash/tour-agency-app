import tkinter as tk
from tkinter import messagebox
from models import tour_model

def open_admin_panel(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Добавить новый тур").grid(row=0, columnspan=2, pady=10)

    labels = ["Название", "Страна", "Дата начала (YYYY-MM-DD)", "Дата конца", "Цена", "Описание"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(root, text=label).grid(row=i+1, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(root, width=40)
        entry.grid(row=i+1, column=1, padx=5)
        entries.append(entry)

    def on_add():
        try:
            title, country, start, end, price, desc = [e.get() for e in entries]
            tour_model.add_tour(title, country, start, end, float(price), desc)
            messagebox.showinfo("Успех", "Тур добавлен!")
            for e in entries:
                e.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка добавления: {e}")

    tk.Button(root, text="Добавить тур", command=on_add).grid(row=8, columnspan=2, pady=10)
