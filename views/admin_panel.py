
import tkinter as tk
from tkinter import ttk, messagebox
from models import tour_model
from views import guides_panel

def center_window(root, width=900, height=600):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def open_admin_panel(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#2e2e2e")
    center_window(root)

    main_frame = tk.Frame(root, bg="#2e2e2e")
    main_frame.pack(expand=True)

    tk.Label(main_frame, text="Добавить новый тур", font=("Arial", 14), bg="#2e2e2e", fg="white").grid(row=0, columnspan=2, pady=10)

    labels = ["Название", "Страна", "Дата начала (YYYY-MM-DD)", "Дата конца", "Цена", "Описание"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(main_frame, text=label, bg="#2e2e2e", fg="white").grid(row=i+1, column=0, sticky='e', padx=5, pady=2)
        entry = tk.Entry(main_frame, width=40, bg="#444444", fg="white", insertbackground="white")
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

    tk.Button(main_frame, text="Добавить тур", command=on_add, bg="#666666", fg="white").grid(row=8, columnspan=2, pady=10)
    tk.Button(main_frame, text="Просмотр и удаление туров", command=lambda: show_all_tours(root), bg="#666666", fg="white").grid(row=9, columnspan=2, pady=5)
    tk.Button(main_frame, text="Гиды и экскурсоводы", command=lambda: guides_panel.open(root), bg="#666666", fg="white").grid(row=10, columnspan=2, pady=5)

def show_all_tours(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#2e2e2e")
    center_window(root)

    top_frame = tk.Frame(root, bg="#2e2e2e")
    top_frame.pack(fill="both", expand=True)
    filter_frame = tk.Frame(root, bg="#2e2e2e")
    filter_frame.pack(pady=5)

    tk.Label(filter_frame, text="Фильтр по стране:", bg="#2e2e2e", fg="white").grid(row=0, column=0)
    country_filter = tk.Entry(filter_frame, bg="#444444", fg="white", insertbackground="white")
    country_filter.grid(row=0, column=1)

    tk.Label(filter_frame, text="Макс. цена:", bg="#2e2e2e", fg="white").grid(row=0, column=2)
    price_filter = tk.Entry(filter_frame, bg="#444444", fg="white", insertbackground="white")
    price_filter.grid(row=0, column=3)

    def apply_filters():
        country = country_filter.get()
        price = price_filter.get()
        try:
            tours = tour_model.search_tours_admin(country, float(price) if price else None)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное значение цены")
            return

        tree.delete(*tree.get_children())
        for tour in tours:
            tree.insert("", "end", values=(tour["id"], tour["title"], tour["country"],
                                           tour["start_date"], tour["end_date"], tour["price"]))

    tk.Button(filter_frame, text="Применить фильтр", command=apply_filters, bg="#555555", fg="white").grid(row=0, column=4, padx=5)

    tree = ttk.Treeview(top_frame, columns=("id", "title", "country", "start", "end", "price"), show="headings")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#3a3a3a",
                    foreground="white",
                    fieldbackground="#3a3a3a",
                    rowheight=25,
                    font=("Arial", 10))
    style.map("Treeview", background=[("selected", "#5a5a5a")])

    for col in tree["columns"]:
        tree.heading(col, text=col)

    tours = tour_model.get_all_tours()
    for tour in tours:
        tree.insert("", "end", values=(tour["id"], tour["title"], tour["country"],
                                       tour["start_date"], tour["end_date"], tour["price"]))

    bottom_frame = tk.Frame(root, bg="#2e2e2e")
    bottom_frame.pack(pady=10)

    tk.Label(bottom_frame, text="Новая цена:", bg="#2e2e2e", fg="white").pack()
    price_entry = tk.Entry(bottom_frame, bg="#444444", fg="white", insertbackground="white")
    price_entry.pack()

    def on_edit():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите тур для изменения")
            return
        try:
            new_price = float(price_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную цену")
            return

        tour_id = tree.item(selected[0])["values"][0]
        tour_model.update_tour_price(tour_id, new_price)
        messagebox.showinfo("Успех", "Цена тура обновлена")
        show_all_tours(root)

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите тур для удаления")
            return
        tour_id = tree.item(selected[0])["values"][0]
        tour_model.delete_tour(tour_id)
        messagebox.showinfo("Удалено", "Тур удалён")
        show_all_tours(root)

    tk.Button(bottom_frame, text="Изменить цену", command=on_edit, bg="#666666", fg="white").pack(pady=5)
    tk.Button(bottom_frame, text="Удалить выбранный тур", command=on_delete, bg="#666666", fg="white").pack(pady=5)
    tk.Button(bottom_frame, text="Назад", command=lambda: open_admin_panel(root), bg="#666666", fg="white").pack(pady=5)
