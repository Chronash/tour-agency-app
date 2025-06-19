import tkinter as tk
from tkinter import ttk, messagebox
from models import transfer_model
from views import admin_panel

def open(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="График трансферов").pack(pady=10)

    form = tk.Frame(root)
    form.pack(pady=5)

    tk.Label(form, text="Город").grid(row=0, column=0)
    city_entry = tk.Entry(form)
    city_entry.grid(row=0, column=1)

    tk.Label(form, text="Дата (YYYY-MM-DD)").grid(row=1, column=0)
    date_entry = tk.Entry(form)
    date_entry.grid(row=1, column=1)

    tk.Label(form, text="Описание").grid(row=2, column=0)
    desc_entry = tk.Entry(form)
    desc_entry.grid(row=2, column=1)

    def on_add():
        city = city_entry.get()
        date = date_entry.get()
        description = desc_entry.get()

        if not city or not date:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        transfer_model.add_transfer(city, date, description)
        messagebox.showinfo("Успех", "Трансфер добавлен")
        city_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        refresh()

    tk.Button(root, text="Добавить трансфер", command=on_add).pack(pady=5)

    tree = ttk.Treeview(root, columns=("id", "city", "date", "description"), show="headings")
    tree.pack(fill="both", expand=True)
    for col in tree["columns"]:
        tree.heading(col, text=col)

    def refresh():
        tree.delete(*tree.get_children())
        for t in transfer_model.get_all_transfers():
            tree.insert("", "end", values=(t["id"], t["city"], t["date"], t["description"]))

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите трансфер для удаления")
            return
        transfer_id = tree.item(selected[0])["values"][0]
        transfer_model.delete_transfer(transfer_id)
        messagebox.showinfo("Удалено", "Трансфер удалён")
        refresh()

    tk.Button(root, text="Удалить выбранный трансфер", command=on_delete).pack(pady=5)
    tk.Button(root, text="Назад", command=lambda: admin_panel.open_admin_panel(root)).pack(pady=5)


    refresh()
