import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from datetime import datetime
import json
import os

class ChatApplication:
    def __init__(self, root):
        self.root = root
        self.current_user = None
        self.theme = "light"  # default theme
        self.setup_ui()
        self.show_login()
        
    def setup_ui(self):
        self.root.title("Python Chat App")
        self.root.geometry("600x700")
        
        # Configure styles for light/dark themes
        self.style = ttk.Style()
        self.configure_themes()
        
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(
            self.main_frame, wrap=tk.WORD, state='disabled', font=('Arial', 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Initialize text tags
        self.chat_area.tag_configure("System", foreground="blue")
        self.chat_area.tag_configure("ChatBot", foreground="green")
        self.chat_area.tag_configure("You", foreground="purple")
        
        # Bottom frame for message entry and buttons
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        # Emoji button
        self.emoji_button = ttk.Button(
            self.bottom_frame, text="😊", command=self.show_emoji_picker)
        self.emoji_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Message entry
        self.msg_entry = ttk.Entry(self.bottom_frame, font=('Arial', 12))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.msg_entry.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = ttk.Button(
            self.bottom_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Theme switcher in menu
        self.menubar = tk.Menu(self.root)
        self.theme_menu = tk.Menu(self.menubar, tearoff=0)
        self.theme_menu.add_command(label="Light", command=lambda: self.set_theme("light"))
        self.theme_menu.add_command(label="Dark", command=lambda: self.set_theme("dark"))
        self.menubar.add_cascade(label="Theme", menu=self.theme_menu)
        self.root.config(menu=self.menubar)
        
        # Hide main UI until login
        self.hide_chat_ui()
    
    def configure_themes(self):
        # Light theme
        self.style.configure('light.TFrame', background='white')
        self.style.configure('light.TLabel', background='white', foreground='black')
        self.style.configure('light.TButton', background='#f0f0f0', foreground='black')
        self.style.configure('light.TEntry', fieldbackground='white', foreground='black')
        
        # Dark theme
        self.style.configure('dark.TFrame', background='#2d2d2d')
        self.style.configure('dark.TLabel', background='#2d2d2d', foreground='white')
        self.style.configure('dark.TButton', background='#3d3d3d', foreground='white')
        self.style.configure('dark.TEntry', fieldbackground='#3d3d3d', foreground='white')
        
        # Text widget colors
        self.light_text_bg = 'white'
        self.light_text_fg = 'black'
        self.dark_text_bg = '#2d2d2d'
        self.dark_text_fg = 'white'
    
    def set_theme(self, theme_name):
        self.theme = theme_name
        suffix = f"{theme_name}.TFrame"
        
        # Update widget styles
        self.main_frame.configure(style=suffix)
        self.bottom_frame.configure(style=suffix)
        
        # Update text widget colors
        bg = self.light_text_bg if theme_name == "light" else self.dark_text_bg
        fg = self.light_text_fg if theme_name == "light" else self.dark_text_fg
        self.chat_area.configure(bg=bg, fg=fg, insertbackground=fg)
        self.msg_entry.configure(style=f"{theme_name}.TEntry")
        
        # Update all buttons
        for widget in self.bottom_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.configure(style=f"{theme_name}.TButton")
    
    def show_login(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")
        self.login_window.geometry("300x200")
        self.login_window.resizable(False, False)
        self.login_window.grab_set()
        
        ttk.Label(self.login_window, text="Username:").pack(pady=(20, 0))
        self.username_entry = ttk.Entry(self.login_window)
        self.username_entry.pack(pady=5)
        
        ttk.Label(self.login_window, text="Password:").pack()
        self.password_entry = ttk.Entry(self.login_window, show="*")
        self.password_entry.pack(pady=5)
        
        buttons_frame = ttk.Frame(self.login_window)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Login", 
                 command=self.handle_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Register", 
                 command=self.show_register).pack(side=tk.LEFT, padx=5)
    
    def show_register(self):
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("Register")
        self.register_window.geometry("300x250")
        self.register_window.resizable(False, False)
        self.register_window.grab_set()
        
        ttk.Label(self.register_window, text="Choose a username:").pack(pady=(20, 0))
        self.reg_username = ttk.Entry(self.register_window)
        self.reg_username.pack(pady=5)
        
        ttk.Label(self.register_window, text="Choose a password:").pack()
        self.reg_password = ttk.Entry(self.register_window, show="*")
        self.reg_password.pack(pady=5)
        
        ttk.Label(self.register_window, text="Confirm password:").pack()
        self.reg_confirm = ttk.Entry(self.register_window, show="*")
        self.reg_confirm.pack(pady=5)
        
        ttk.Button(self.register_window, text="Register", 
                  command=self.handle_register).pack(pady=10)
    
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if self.authenticate_user(username, password):
            self.current_user = username
            self.login_window.destroy()
            self.show_chat_ui()
            self.display_message("System", f"Welcome, {username}!")
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def handle_register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords don't match")
            return
        
        if self.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.register_window.destroy()
        else:
            messagebox.showerror("Error", "Username already exists")
    
    def authenticate_user(self, username, password):
        if not os.path.exists("users.json"):
            return False
        
        with open("users.json", "r") as f:
            users = json.load(f)
            return users.get(username) == password
    
    def register_user(self, username, password):
        users = {}
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                users = json.load(f)
        
        if username in users:
            return False
        
        users[username] = password
        with open("users.json", "w") as f:
            json.dump(users, f)
        return True
    
    def show_chat_ui(self):
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.root.config(menu=self.menubar)
    
    def hide_chat_ui(self):
        self.main_frame.pack_forget()
        self.root.config(menu=tk.Menu(self.root))
    
    def show_emoji_picker(self):
        emoji_window = tk.Toplevel(self.root)
        emoji_window.title("Select Emoji")
        emoji_window.geometry("300x200")
        
        emojis = ["😀", "😂", "😍", "😎", "🤔", "👍", "❤️", "🎉", "🙏", "🔥"]
        
        for i, emoji in enumerate(emojis):
            btn = ttk.Button(emoji_window, text=emoji, 
                           command=lambda e=emoji: self.insert_emoji(e, emoji_window))
            btn.grid(row=i//5, column=i%5, padx=5, pady=5)
    
    def insert_emoji(self, emoji, window):
        self.msg_entry.insert(tk.END, emoji)
        window.destroy()
    
    def send_message(self, event=None):
        msg = self.msg_entry.get()
        if msg:
            self.display_message(self.current_user, msg)
            self.msg_entry.delete(0, tk.END)
            self.root.after(1000, self.simulate_response, msg)
    
    def simulate_response(self, user_msg):
        responses = {
            "hi": "Hello there!",
            "hello": f"Hi {self.current_user}! How can I help you?",
            "who are you": "Iam chat application created by vamshi",
            "how are you": "I'm just a program, but thanks for asking!",
            "bye": "Goodbye! Have a great day!",
            "default": f"You said: '{user_msg}'. Interesting!"
        }
        
        response = responses.get(user_msg.lower(), responses['default'])
        self.display_message("ChatBot", response)
    
    def display_message(self, sender, message):
        self.chat_area.configure(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Special formatting for the current user
        if sender == self.current_user:
            self.chat_area.insert(tk.END, f"[{timestamp}] You: ", "You")
        else:
            self.chat_area.insert(tk.END, f"[{timestamp}] {sender}: ", sender)
        
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()