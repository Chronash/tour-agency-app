
import tkinter as tk
from tkinter import ttk, messagebox
from models import guide_model
from views import admin_panel

def center_window(root, width=800, height=500):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def open(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#2e2e2e")
    center_window(root)

    frame = tk.Frame(root, bg="#2e2e2e")
    frame.pack(pady=20)

    tk.Label(frame, text="Добавить гида", font=("Arial", 14), bg="#2e2e2e", fg="white").grid(row=0, columnspan=2, pady=10)

    fields = ["ФИО", "Страна", "Опыт (лет)", "Языки через запятую"]
    entries = []
    for i, label in enumerate(fields):
        tk.Label(frame, text=label, bg="#2e2e2e", fg="white").grid(row=i+1, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(frame, bg="#444444", fg="white", insertbackground="white", width=30)
        entry.grid(row=i+1, column=1, padx=5)
        entries.append(entry)

    def on_add():
        name, country, exp, langs = [e.get() for e in entries]
        try:
            guide_model.add_guide(name, country, int(exp), langs)
            messagebox.showinfo("Успех", "Гид добавлен")
            refresh()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите гида для удаления")
            return
        guide_id = tree.item(selected[0])["values"][0]
        guide_model.delete_guide(guide_id)
        messagebox.showinfo("Удалено", "Гид удалён")
        refresh()

    tk.Button(frame, text="Добавить гида", command=on_add, bg="#666666", fg="white").grid(row=6, columnspan=2, pady=10)

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

    tree = ttk.Treeview(root, columns=("id", "name", "country", "experience", "langs"), show="headings", height=10)
    tree.pack(expand=True, fill="both", padx=20)

    for col, title in zip(tree["columns"], ["ID", "ФИО", "Страна", "Опыт", "Языки"]):
        tree.heading(col, text=title)

    def refresh():
        tree.delete(*tree.get_children())
        for g in guide_model.get_all_guides():
            tree.insert("", "end", values=(g["id"], g["name"], g["country"], g["experience"], g["languages"]))

    refresh()

    tk.Button(root, text="Удалить выбранного", command=on_delete, bg="#666666", fg="white").pack(pady=5)
    tk.Button(root, text="Назад", command=lambda: admin_panel.open_admin_panel(root),
          bg="#666666", fg="white").pack(pady=10)
