# 💬 Python Chat Application with Tkinter

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)

A desktop chat application featuring user authentication, emoji support, and theme customization built with Python and Tkinter.


## 🌟 Features

- **Secure User Authentication** (Login/Registration)
- **Emoji Picker** with 10+ emojis
- **Theme Customization** (Light/Dark modes)
- **Interactive Chat Interface** with timestamps
- **Responsive Design** for different screen sizes
- **JSON-based** user data storage

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/k-vamshi17/Chat_Application.git
cd Chat_Application
```
2. Run the application:
```bash
python chat.py
```
##### Note: Requires Python 3.6+ (Tkinter included in standard library)

## 🖥️ Usage
1. First Launch:
- Register a new account
- Login with your credentials

2. Chat Interface:
- Type messages in the bottom text field
- Press Enter or click Send
- Click the 😊 button for emoji picker

3. Customization:

- Change themes via the Theme menu
- Messages are color-coded by sender

## 🔧 Code Highlights
### Authentication System
```python
def authenticate_user(self, username, password):
    if not os.path.exists("users.json"):
        return False
    with open("users.json", "r") as f:
        users = json.load(f)
        return users.get(username) == password
```
### Theme Switching
```python
def set_theme(self, theme_name):
    bg = 'white' if theme_name == "light" else '#2d2d2d'
    fg = 'black' if theme_name == "light" else 'white'
    self.chat_area.configure(bg=bg, fg=fg)
```
### Emoji Picker
```python
def show_emoji_picker(self):
    emojis = ["😀", "😂", "😍", "😎", "🤔", "👍", "❤️", "🎉", "🙏", "🔥"]
    # ... creates interactive emoji selection window
```
## 🤖 Chatbot Logic
### The chatbot responds to a few preset messages like:

- "hi"
- "hello"
- "who are you"
- "how are you"
- "bye"

Any unknown input gets an echo-style response.

## 💡 Future Improvements
- Save and load chat history
- Add encryption to user data
- Improve chatbot intelligence using NLP libraries
- Support for sending images or files

## 🙋‍♂️ Author
Created by Kuncha Vamshi Reddy
