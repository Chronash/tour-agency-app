import tkinter as tk
from tkinter import ttk, messagebox
from models import tour_model, booking_model

def open_user_main(root, user):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Добро пожаловать, {user['username']}").pack()
    prefs = []
    if user.get("food_preferences"):
        prefs.append(f"Тип питания: {user['food_preferences']}")
    if user.get("allergies"):
        prefs.append(f"Аллергии: {user['allergies']}")

    if prefs:
        tk.Label(root, text="Ваши предпочтения:").pack()
        for p in prefs:
            tk.Label(root, text=p).pack()

    raw_allergies = user.get("allergies") or ""
    allergy_list = [a.strip().lower() for a in raw_allergies.split(",") if a.strip()]

    food_pref = (user.get("food_preferences") or "").strip().lower()


    # Получение подходящих стран
    from collections import Counter

    matching_tours = tour_model.search_tours(
    allergy_exclude=allergy_list if allergy_list else None,
    food_preference=food_pref if food_pref else None
    )
    country_counts = Counter(t["country"] for t in matching_tours)

    if country_counts:
        tk.Label(root, text="Страны, соответствующие вашим предпочтениям:").pack()
        countries_text = ", ".join(f"{country} ({count})" for country, count in country_counts.items())
        tk.Label(root, text=countries_text, wraplength=800, justify="center").pack(pady=5)

    frm = tk.Frame(root)
    frm.pack()

    tk.Label(frm, text="Страна").grid(row=0, column=0)
    country_entry = tk.Entry(frm)
    country_entry.grid(row=0, column=1)

    tk.Label(frm, text="Макс. цена").grid(row=0, column=2)
    price_entry = tk.Entry(frm)
    price_entry.grid(row=0, column=3)

    tk.Button(frm, text="Найти тур", command=lambda: on_search()).grid(row=0, column=4, padx=10)

    tree = ttk.Treeview(root, columns=("id", "title", "country", "price"), show="headings")
    tree.pack(expand=True, fill="both", pady=10)

    for col in tree["columns"]:
        tree.heading(col, text=col)

    tk.Button(root, text="Забронировать выбранный тур", command=lambda: on_book()).pack(pady=5)
    tk.Button(root, text="Мои бронирования", command=lambda: show_bookings(root, user)).pack(pady=5)

    visa_required_countries = ["США", "Канада", "Австралия", "Великобритания", "Япония", "Китай"]
    vaccination_required_countries = ["Индия", "Египет", "Бразилия", "Таиланд"]

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

    def on_book():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите тур!")
            return

        tour_id = tree.item(selected[0])["values"][0]
        selected_country = tree.item(selected[0])["values"][2]

        alerts = []
        if selected_country in visa_required_countries:
            alerts.append(f"Виза обязательна для поездки в {selected_country}")
        if selected_country in vaccination_required_countries:
            alerts.append(f"Для поездки в {selected_country} необходимы прививки")
        if alerts:
            messagebox.showinfo("Внимание", "\n".join(alerts))

        booking_model.book_tour(user["id"], tour_id)
        messagebox.showinfo("Успех", f"Вы успешно забронировали тур!\n\n(Псевдо-договор сформирован)")

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

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите бронирование для удаления")
            return
        booking_id = tree.item(selected[0])["values"][0]
        booking_model.delete_booking(booking_id)
        messagebox.showinfo("Удалено", "Бронирование удалено")
        show_bookings(root, user)

    tk.Button(root, text="Отменить бронирование", command=on_delete).pack(pady=5)
    tk.Button(root, text="Назад", command=lambda: open_user_main(root, user)).pack(pady=5)
