
import tkinter as tk
from tkinter import ttk, messagebox
from models import transfer_model
from views import admin_panel

def center_window(root, width=800, height=500):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def open_transfer_panel(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#2e2e2e")
    center_window(root)

    tk.Label(root, text="Добавить трансфер", font=("Arial", 14), bg="#2e2e2e", fg="white").pack(pady=10)

    form = tk.Frame(root, bg="#2e2e2e")
    form.pack()

    labels = ["ID Тура", "Дата (YYYY-MM-DD)", "Тип трансфера"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(form, text=label, bg="#2e2e2e", fg="white").grid(row=i, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(form, bg="#444444", fg="white", insertbackground="white")
        entry.grid(row=i, column=1, padx=5, pady=2)
        entries.append(entry)

    def on_add():
        try:
            tour_id = int(entries[0].get())
            date = entries[1].get()
            ttype = entries[2].get()
            transfer_model.add_transfer(tour_id, date, ttype)
            messagebox.showinfo("Успех", "Трансфер добавлен!")
            refresh()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    tk.Button(root, text="Добавить", command=on_add, bg="#666666", fg="white").pack(pady=10)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
        background="#3a3a3a",
        foreground="white",
        fieldbackground="#3a3a3a",
        rowheight=25,
        font=("Arial", 10)
    )
    style.map("Treeview", background=[("selected", "#5a5a5a")])

    tree = ttk.Treeview(root, columns=("id", "tour_id", "date", "type"), show="headings")
    tree.pack(expand=True, fill="both", padx=20, pady=5)

    for col in tree["columns"]:
        tree.heading(col, text=col)

    def refresh():
        tree.delete(*tree.get_children())
        for t in transfer_model.get_all_transfers():
            tree.insert("", "end", values=(t["id"], t["tour_id"], t["date"], t["type"]))

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите трансфер для удаления")
            return
        transfer_id = tree.item(selected[0])["values"][0]
        transfer_model.delete_transfer(transfer_id)
        messagebox.showinfo("Удалено", "Трансфер удалён")
        refresh()

    tk.Button(root, text="Удалить выбранный", command=on_delete, bg="#666666", fg="white").pack(pady=5)
    tk.Button(root, text="Назад", command=lambda: admin_panel.open_admin_panel(root), bg="#666666", fg="white").pack(pady=5)

    refresh()
