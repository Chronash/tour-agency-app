import tkinter as tk
from tkinter import ttk, messagebox
from models import tour_model, booking_model

def open_user_main(root, user):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Добро пожаловать, {user['username']}").pack()

    frm = tk.Frame(root)
    frm.pack()

    tk.Label(frm, text="Страна").grid(row=0, column=0)
    country_entry = tk.Entry(frm)
    country_entry.grid(row=0, column=1)

    tk.Label(frm, text="Макс. цена").grid(row=0, column=2)
    price_entry = tk.Entry(frm)
    price_entry.grid(row=0, column=3)

    tree = ttk.Treeview(root, columns=("id", "title", "country", "price"), show="headings")
    tree.pack(expand=True, fill="both", pady=10)
    tk.Button(root, text="Мои бронирования", command=lambda: show_bookings(root, user)).pack(pady=5)



    for col in tree["columns"]:
        tree.heading(col, text=col)

    def on_search():
        country = country_entry.get()
        price = price_entry.get()
        tours = tour_model.search_tours(country, price if price else None)
        tree.delete(*tree.get_children())
        for tour in tours:
            tree.insert("", "end", values=(tour["id"], tour["title"], tour["country"], tour["price"]))

    def on_book():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите тур!")
            return
        tour_id = tree.item(selected[0])["values"][0]
        booking_model.book_tour(user["id"], tour_id)
        messagebox.showinfo("Успех", f"Вы успешно забронировали тур!\n\n(Псевдо-договор сформирован)")

    tk.Button(root, text="Найти тур", command=on_search).pack(pady=5)
    tk.Button(root, text="Забронировать выбранный тур", command=on_book).pack()
    
def show_bookings(root, user):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Бронирования: {user['username']}").pack()

    tree = ttk.Treeview(root, columns=("id", "title", "country", "start", "end", "price"), show="headings")
    tree.pack(expand=True, fill="both", pady=10)

    for col in tree["columns"]:
        tree.heading(col, text=col)

    bookings = booking_model.get_bookings_for_user(user["id"])
    for b in bookings:
        tree.insert("", "end", values=(
            b["id"], b["title"], b["country"], b["start_date"], b["end_date"], b["price"]
        ))

    # ⬇️ сначала объявляем on_delete
    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите бронирование для удаления")
            return
        booking_id = tree.item(selected[0])["values"][0]
        booking_model.delete_booking(booking_id)
        messagebox.showinfo("Удалено", "Бронирование удалено")
        show_bookings(root, user)  # обновить таблицу

    # ⬇️ теперь используем её в кнопке
    tk.Button(root, text="Отменить бронирование", command=on_delete).pack(pady=5)
    tk.Button(root, text="Назад", command=lambda: open_user_main(root, user)).pack(pady=5)


