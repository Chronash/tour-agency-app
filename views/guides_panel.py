import tkinter as tk
from tkinter import ttk, messagebox
from models import guide_model
from views import admin_panel


def open(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Управление гидами").pack(pady=10)

    form = tk.Frame(root)
    form.pack(pady=5)

    tk.Label(form, text="Имя и Фамилия").grid(row=0, column=0)
    name_entry = tk.Entry(form)
    name_entry.grid(row=0, column=1)

    tk.Label(form, text="Страна").grid(row=1, column=0)
    country_entry = tk.Entry(form)
    country_entry.grid(row=1, column=1)

    tk.Label(form, text="Опыт (лет)").grid(row=2, column=0)
    experience_entry = tk.Entry(form)
    experience_entry.grid(row=2, column=1)

    tk.Label(form, text="Языки").grid(row=3, column=0)
    languages_entry = tk.Entry(form)
    languages_entry.grid(row=3, column=1)

    def on_add():
        name = name_entry.get()
        country = country_entry.get()
        try:
            experience = int(experience_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Опыт должен быть числом")
            return
        languages = languages_entry.get()

        guide_model.add_guide(name, country, experience, languages)
        messagebox.showinfo("Успех", "Гид добавлен")
        name_entry.delete(0, tk.END)
        country_entry.delete(0, tk.END)
        experience_entry.delete(0, tk.END)
        languages_entry.delete(0, tk.END)
        refresh()

    tk.Button(root, text="Добавить гида", command=on_add).pack(pady=5)

    tree = ttk.Treeview(root, columns=("id", "name", "country", "experience", "languages"), show="headings")
    tree.pack(fill="both", expand=True)
    for col in tree["columns"]:
        tree.heading(col, text=col)

    def refresh():
        tree.delete(*tree.get_children())
        for g in guide_model.get_all_guides():
            tree.insert("", "end", values=(g["id"], g["name"], g["country"], g["experience"], g["languages"]))

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите гида для удаления")
            return
        guide_id = tree.item(selected[0])["values"][0]
        guide_model.delete_guide(guide_id)
        messagebox.showinfo("Удалено", "Гид удалён")
        refresh()

    tk.Button(root, text="Удалить выбранного гида", command=on_delete).pack(pady=5)
    tk.Button(root, text="Назад", command=lambda: admin_panel.open_admin_panel(root)).pack(pady=5)


    refresh()
