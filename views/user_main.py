
import tkinter as tk
from tkinter import ttk, messagebox
from models import tour_model, booking_model
from collections import Counter

def center_window(root, width=900, height=600):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def open_user_main(root, user):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#2e2e2e")
    center_window(root)

    main_frame = tk.Frame(root, bg="#2e2e2e")
    main_frame.pack(expand=True)

    tk.Label(main_frame, text=f"Добро пожаловать, {user['username']}", font=("Arial", 14), bg="#2e2e2e", fg="white").pack(pady=5)

    prefs = []
    if user.get("food_preferences"):
        prefs.append(f"Тип питания: {user['food_preferences']}")
    if user.get("allergies"):
        prefs.append(f"Аллергии: {user['allergies']}")

    if prefs:
        tk.Label(main_frame, text="Ваши предпочтения:", bg="#2e2e2e", fg="white").pack()
        for p in prefs:
            tk.Label(main_frame, text=p, bg="#2e2e2e", fg="white").pack()

    raw_allergies = user.get("allergies") or ""
    allergy_list = [a.strip().lower() for a in raw_allergies.split(",") if a.strip()]
    food_pref = (user.get("food_preferences") or "").strip().lower()

    matching_tours = tour_model.search_tours(
        allergy_exclude=allergy_list if allergy_list else None,
        food_preference=food_pref if food_pref else None
    )
    country_counts = Counter(t["country"] for t in matching_tours)

    if country_counts:
        countries_text = ", ".join(f"{country} ({count})" for country, count in country_counts.items())
        tk.Label(main_frame, text="Страны, соответствующие вашим предпочтениям:", bg="#2e2e2e", fg="white").pack()
        tk.Label(main_frame, text=countries_text, bg="#2e2e2e", fg="white", wraplength=800, justify="center").pack(pady=5)

    # Форма фильтрации
    filter_frame = tk.Frame(main_frame, bg="#2e2e2e")
    filter_frame.pack(pady=5)

    tk.Label(filter_frame, text="Страна", bg="#2e2e2e", fg="white").grid(row=0, column=0, padx=5)
    country_entry = tk.Entry(filter_frame, bg="#444444", fg="white", insertbackground="white")
    country_entry.grid(row=0, column=1)

    tk.Label(filter_frame, text="Макс. цена", bg="#2e2e2e", fg="white").grid(row=0, column=2, padx=5)
    price_entry = tk.Entry(filter_frame, bg="#444444", fg="white", insertbackground="white")
    price_entry.grid(row=0, column=3)

    def on_search():
        country = country_entry.get()
        price = price_entry.get()
        tours = tour_model.search_tours(
            country,
            price if price else None,
            allergy_exclude=allergy_list,
            food_preference=food_pref if food_pref else None
        )
        tree.delete(*tree.get_children())
        for tour in tours:
            tree.insert("", "end", values=(tour["id"], tour["title"], tour["country"], tour["price"]))

    tk.Button(filter_frame, text="Найти тур", command=on_search, bg="#555555", fg="white").grid(row=0, column=4, padx=10)

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

    tree = ttk.Treeview(main_frame, columns=("id", "title", "country", "price"), show="headings", height=10)
    tree.pack(expand=True, fill="both", pady=10)
    for col in tree["columns"]:
        tree.heading(col, text=col)

    def on_book():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите тур!")
            return
        tour_id = tree.item(selected[0])["values"][0]
        selected_country = tree.item(selected[0])["values"][2]

        alerts = []
        if selected_country in ["США", "Канада", "Австралия", "Великобритания", "Япония", "Китай"]:
            alerts.append(f"Виза обязательна для поездки в {selected_country}")
        if selected_country in ["Индия", "Египет", "Бразилия", "Таиланд"]:
            alerts.append(f"Для поездки в {selected_country} необходимы прививки")
        if alerts:
            messagebox.showinfo("Внимание", "\n".join(alerts))

        booking_model.book_tour(user["id"], tour_id)
        messagebox.showinfo("Успех", f"Вы успешно забронировали тур!\n\n(Псевдо-договор сформирован)")

    tk.Button(main_frame, text="Забронировать выбранный тур", command=on_book, bg="#666666", fg="white").pack(pady=5)
    tk.Button(main_frame, text="Мои бронирования", command=lambda: show_bookings(root, user), bg="#666666", fg="white").pack(pady=5)

def show_bookings(root, user):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#2e2e2e")
    center_window(root)

    tk.Label(root, text=f"Бронирования: {user['username']}", bg="#2e2e2e", fg="white").pack()

    tree = ttk.Treeview(root, columns=("id", "title", "country", "start", "end", "price"), show="headings")
    tree.pack(expand=True, fill="both", pady=10)
    for col in tree["columns"]:
        tree.heading(col, text=col)

    bookings = booking_model.get_bookings_for_user(user["id"])
    for b in bookings:
        tree.insert("", "end", values=(b["id"], b["title"], b["country"], b["start_date"], b["end_date"], b["price"]))

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите бронирование для удаления")
            return
        booking_id = tree.item(selected[0])["values"][0]
        booking_model.delete_booking(booking_id)
        messagebox.showinfo("Удалено", "Бронирование удалено")
        show_bookings(root, user)

    tk.Button(root, text="Отменить бронирование", command=on_delete, bg="#666666", fg="white").pack(pady=5)
    tk.Button(root, text="Назад", command=lambda: open_user_main(root, user), bg="#666666", fg="white").pack(pady=5)
