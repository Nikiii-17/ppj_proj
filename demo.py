
import tkinter as tk
from tkinter import font, messagebox

from fungovani import Fungovani


# ==========================================
# DASHBOARD
# ==========================================

root = tk.Tk()
root.title("Welcome - Dashboard")

window_width = 900
window_height = 650

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.config(bg="#f8fafc")
root.resizable(True, True)


# Fonty
font_title = font.Font(family="Segoe UI", size=20, weight="bold")
font_sub = font.Font(family="Segoe UI", size=10)
font_ui = font.Font(family="Segoe UI", size=10)
font_card_title = font.Font(family="Segoe UI", size=12, weight="bold")


# ==========================================
# PRIHLASOVACI LOGIKA
# ==========================================

def login_success(username):
    login_btn.pack_forget()
    signup_btn.pack_forget()

    username_label.config(text=username)
    username_label.pack(side="left")


auth = Fungovani(on_login_success=login_success)


# ==========================================
# HLAVNI KONTEJNER
# ==========================================

main_container = tk.Frame(root, bg="#f8fafc")
main_container.pack(fill="both", expand=True, padx=40, pady=30)

top_bar = tk.Frame(main_container, bg="#f8fafc")
top_bar.pack(fill="x", pady=(0, 25))


# Vyhledavani
search_frame = tk.Frame(
    top_bar,
    bg="white",
    highlightbackground="#cbd5e1",
    highlightthickness=1
)
search_frame.pack(side="left", fill="x", expand=True, padx=(0, 20))

search_entry = tk.Entry(
    search_frame,
    font=font_ui,
    bg="white",
    fg="#334155",
    bd=0,
    highlightthickness=0
)
search_entry.pack(side="left", fill="both", expand=True, padx=12, ipady=8)
search_entry.insert(0, "Hej neco hledej idk")

search_btn = tk.Button(
    search_frame,
    text="🔍",
    font=font_ui,
    bg="white",
    fg="#64748b",
    bd=0,
    cursor="hand2",
    activebackground="white"
)
search_btn.pack(side="right", padx=10)


# Prihlasovani
auth_frame = tk.Frame(top_bar, bg="#f8fafc")
auth_frame.pack(side="right")

login_btn = tk.Button(
    auth_frame,
    text="Log In",
    font=font_ui,
    bg="#f8fafc",
    fg="#4f46e5",
    bd=0,
    activebackground="#f8fafc",
    cursor="hand2"
)
login_btn.pack(side="left", padx=(0, 15))

signup_btn = tk.Button(
    auth_frame,
    text="Create Account",
    font=font_ui,
    bg="#4f46e5",
    fg="white",
    relief="flat",
    padx=16,
    pady=8,
    cursor="hand2",
    activebackground="#4338ca",
    activeforeground="white"
)
signup_btn.pack(side="left")


username_label = tk.Button(
    auth_frame,
    text="",
    font=font_ui,
    bg="#4f46e5",
    fg="white",
    activebackground="#4338ca",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=12,
    pady=8,
    cursor="hand2",
    command=lambda: open_account_menu()
)



def open_account_menu():
    if auth.prihlaseny_uzivatel is None:
        return

    menu = tk.Toplevel(root)
    menu.title("Account")
    menu.geometry("260x180")
    menu.config(bg="#f8fafc")
    menu.resizable(False, False)
    menu.transient(root)
    menu.grab_set()

    tk.Label(
        menu,
        text=f"Logged in as\n{auth.prihlaseny_uzivatel['username']}",
        font=font_ui,
        bg="#f8fafc",
        fg="#0f172a"
    ).pack(pady=(18, 12))

    def perform_logout():
        auth.logout()
        menu.destroy()

        username_label.pack_forget()
        login_btn.pack(side="left", padx=(0, 15))
        signup_btn.pack(side="left")

    def perform_delete():
        confirmed = messagebox.askyesno(
            "Delete Account",
            "Are you sure you want to permanently delete your account?",
            parent=menu
        )

        if not confirmed:
            return

        success, message = auth.delete_account()

        if success:
            menu.destroy()
            username_label.pack_forget()
            login_btn.pack(side="left", padx=(0, 15))
            signup_btn.pack(side="left")

            messagebox.showinfo(
                "Delete Account",
                message,
                parent=root
            )
        else:
            messagebox.showerror(
                "Delete Account",
                message,
                parent=menu
            )

    tk.Button(
        menu,
        text="Log Out",
        font=font_ui,
        bg="#e2e8f0",
        fg="#0f172a",
        relief="flat",
        cursor="hand2",
        command=perform_logout
    ).pack(fill="x", padx=25, pady=(0, 8), ipady=4)

    tk.Button(
        menu,
        text="Delete Account",
        font=font_ui,
        bg="#dc2626",
        fg="white",
        activebackground="#b91c1c",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=perform_delete
    ).pack(fill="x", padx=25, pady=(0, 12), ipady=4)

# ==========================================
# PRIHLASOVACI A REGISTRACNI OKNA
# Grafika je pouze v demo.py
# ==========================================

def open_login_window():
    win = tk.Toplevel(root)
    win.title("Log In")
    win.geometry("350x300")
    win.config(bg="#f8fafc")
    win.resizable(False, False)
    win.grab_set()

    f_title = font.Font(family="Segoe UI", size=14, weight="bold")
    f_ui = font.Font(family="Segoe UI", size=10)

    tk.Label(
        win, text="Welcome Back", font=f_title,
        bg="#f8fafc", fg="#0f172a"
    ).pack(pady=(25, 15))

    tk.Label(
        win, text="Username", font=f_ui,
        bg="#f8fafc", fg="#334155"
    ).pack(anchor="w", padx=30)

    entry_user = tk.Entry(
        win, font=f_ui, bg="white", fg="#334155",
        highlightbackground="#cbd5e1",
        highlightthickness=1, bd=0
    )
    entry_user.pack(fill="x", padx=30, pady=(5, 10), ipady=5)

    tk.Label(
        win, text="Password", font=f_ui,
        bg="#f8fafc", fg="#334155"
    ).pack(anchor="w", padx=30)

    entry_pass = tk.Entry(
        win, font=f_ui, show="*", bg="white", fg="#334155",
        highlightbackground="#cbd5e1",
        highlightthickness=1, bd=0
    )
    entry_pass.pack(fill="x", padx=30, pady=(5, 20), ipady=5)

    def submit_login():
        success, message = auth.login(
            entry_user.get(),
            entry_pass.get()
        )

        if success:
            win.destroy()
            messagebox.showinfo("Log In", message, parent=root)
        else:
            messagebox.showerror("Log In", message, parent=win)

    tk.Button(
        win, text="Log In", font=f_ui,
        bg="#4f46e5", fg="white", bd=0,
        cursor="hand2", activebackground="#4338ca",
        activeforeground="white",
        command=submit_login
    ).pack(fill="x", padx=30, ipady=8)

    win.bind("<Return>", lambda event: submit_login())
    entry_user.focus_set()


def open_signup_window():
    win = tk.Toplevel(root)
    win.title("Create Account")
    win.geometry("350x320")
    win.config(bg="#f8fafc")
    win.resizable(False, False)
    win.grab_set()

    f_title = font.Font(family="Segoe UI", size=14, weight="bold")
    f_ui = font.Font(family="Segoe UI", size=10)

    tk.Label(
        win, text="Create Account", font=f_title,
        bg="#f8fafc", fg="#0f172a"
    ).pack(pady=(25, 15))

    tk.Label(
        win, text="Username", font=f_ui,
        bg="#f8fafc", fg="#334155"
    ).pack(anchor="w", padx=30)

    entry_user = tk.Entry(
        win, font=f_ui, bg="white", fg="#334155",
        highlightbackground="#cbd5e1",
        highlightthickness=1, bd=0
    )
    entry_user.pack(fill="x", padx=30, pady=(5, 10), ipady=5)

    tk.Label(
        win, text="Password", font=f_ui,
        bg="#f8fafc", fg="#334155"
    ).pack(anchor="w", padx=30)

    entry_pass = tk.Entry(
        win, font=f_ui, show="*", bg="white", fg="#334155",
        highlightbackground="#cbd5e1",
        highlightthickness=1, bd=0
    )
    entry_pass.pack(fill="x", padx=30, pady=(5, 20), ipady=5)

    def submit_signup():
        success, message = auth.register(
            entry_user.get(),
            entry_pass.get()
        )

        if success:
            win.destroy()
            messagebox.showinfo(
                "Create Account", message, parent=root
            )
        else:
            messagebox.showerror(
                "Create Account", message, parent=win
            )

    tk.Button(
        win, text="Create Account", font=f_ui,
        bg="#4f46e5", fg="white", bd=0,
        cursor="hand2", activebackground="#4338ca",
        activeforeground="white",
        command=submit_signup
    ).pack(fill="x", padx=30, ipady=8)

    win.bind("<Return>", lambda event: submit_signup())
    entry_user.focus_set()


login_btn.config(command=open_login_window)
signup_btn.config(command=open_signup_window)


# ==========================================
# UVITANI
# ==========================================

welcome_frame = tk.Frame(main_container, bg="#f8fafc")
welcome_frame.pack(fill="x", pady=(0, 30))

tk.Label(
    welcome_frame,
    text="CAUKY MNAUKY",
    font=font_title,
    bg="#f8fafc",
    fg="#0f172a"
).pack(anchor="w")

tk.Label(
    welcome_frame,
    text="tU TO MAS" " hej neco to je",
    font=font_sub,
    bg="#f8fafc",
    fg="#64748b"
).pack(anchor="w", pady=(4, 0))


# ==========================================
# KARTICKY
# ==========================================

cards_label = tk.Label(
    main_container,
    text="Cum se",
    font=font_card_title,
    bg="#f8fafc",
    fg="#334155"
)
cards_label.pack(anchor="w", pady=(0, 12))

cards_container = tk.Frame(main_container, bg="#f8fafc")
cards_container.pack(fill="both", expand=True)

for i in range(3):
    card = tk.Frame(
        cards_container,
        bg="white",
        highlightbackground="#e2e8f0",
        highlightthickness=1
    )
    card.grid(
        row=0,
        column=i,
        padx=(0 if i == 0 else 15, 0),
        sticky="nsew"
    )

    tk.Label(
        card,
        text=f"Empty Card {i+1}\n(To prijde shhhh)",
        font=font_sub,
        bg="white",
        fg="#94a3b8",
        justify="center"
    ).pack(expand=True, fill="both", pady=50)

for i in range(3):
    cards_container.columnconfigure(i, weight=1)

cards_container.rowconfigure(0, weight=1)


# Spusteni aplikace
root.mainloop()
