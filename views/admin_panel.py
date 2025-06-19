import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models import tour_model
from views import guides_panel
from views import transfer_panel


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
    tk.Button(root, text="Просмотр и удаление туров", command=lambda: show_all_tours(root)).grid(row=9, columnspan=2, pady=5)
    tk.Button(root, text="Гиды и экскурсоводы", command=lambda: guides_panel.open(root)).grid(row=10, columnspan=2, pady=5)
    tk.Button(root, text="График трансферов", command=lambda: transfer_panel.open(root)).grid(row=11, columnspan=2, pady=5)

def show_all_tours(root):
    for widget in root.winfo_children():
        widget.destroy()

    top_frame = tk.Frame(root)
    top_frame.pack(fill="both", expand=True)
    filter_frame = tk.Frame(root)
    filter_frame.pack(pady=5)

    tk.Label(filter_frame, text="Фильтр по стране:").grid(row=0, column=0)
    country_filter = tk.Entry(filter_frame)
    country_filter.grid(row=0, column=1)

    tk.Label(filter_frame, text="Макс. цена:").grid(row=0, column=2)
    price_filter = tk.Entry(filter_frame)
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

    tk.Button(filter_frame, text="Применить фильтр", command=apply_filters).grid(row=0, column=4, padx=5)


    bottom_frame = tk.Frame(root)
    bottom_frame.pack(pady=10)

    tk.Label(top_frame, text="Все туры").pack()

    tree = ttk.Treeview(top_frame, columns=("id", "title", "country", "start", "end", "price"), show="headings")
    tree.pack(expand=True, fill="both")

    for col in tree["columns"]:
        tree.heading(col, text=col)

    tours = tour_model.get_all_tours()
    for tour in tours:
        tree.insert("", "end", values=(tour["id"], tour["title"], tour["country"],
                                       tour["start_date"], tour["end_date"], tour["price"]))

    tk.Label(bottom_frame, text="Новая цена:").pack()
    price_entry = tk.Entry(bottom_frame)
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

    tk.Button(bottom_frame, text="Изменить цену", command=on_edit).pack(pady=5)
    tk.Button(bottom_frame, text="Удалить выбранный тур", command=on_delete).pack(pady=5)
    tk.Button(bottom_frame, text="Назад", command=lambda: open_admin_panel(root)).pack(pady=5)
    tk.Button(root, text="Гиды и экскурсоводы", command=lambda: guides_panel.open(root)).grid(row=10, columnspan=2, pady=5)