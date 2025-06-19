import tkinter as tk
from views import login_page

def center_window(window, width=900, height=600):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()
root.title("Турфирма Booking")
center_window(root)
login_page.open_login(root)
root.mainloop()
