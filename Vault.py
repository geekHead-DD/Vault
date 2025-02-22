import customtkinter as ctk
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
from PIL import Image
from cryptography.fernet import Fernet
import os

# ---------------------------- ENCRYPTION SETUP ------------------------------- #
KEY_FILE = "key.key"
DATA_FILE = "data.json.enc"

def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

encryption_key = load_or_generate_key()
cipher = Fernet(encryption_key)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as file:
            encrypted_data = file.read()
            try:
                decrypted_data = cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data)
            except:
                return {}
    return {}

def save_data(data):
    encrypted_data = cipher.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, "wb") as file:
        file.write(encrypted_data)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'
    
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    
    password = "".join(password_list)
    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    
    # Copy password to clipboard
    pyperclip.copy(password)
    
    # Show generated password in a popup window
    popup_window = ctk.CTkToplevel(window)
    popup_window.title("Generated Password")
    popup_window.geometry("300x150")
    
    password_label = ctk.CTkLabel(popup_window, text="Generated Password:")
    password_label.pack(pady=10)
    
    password_display = ctk.CTkLabel(popup_window, text=password, font=("Helvetica", 14))
    password_display.pack(pady=10)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please fill in all fields.")
        return
    
    data = load_data()
    if website in data:
        confirm = messagebox.askyesno(title="Confirm", message=f"Password for {website} already exists. Replace it?")
        if not confirm:
            return
    
    data[website] = {"email": email, "password": password}
    save_data(data)
    
    website_entry.delete(0, "end")
    password_entry.delete(0, "end")

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    data = load_data()
    
    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        pyperclip.copy(password)
    else:
        messagebox.showinfo(title="Error", message=f"No details for {website} exist.")

# ---------------------------- UI SETUP ------------------------------- #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("Password Manager")
window.geometry("500x400")
window.resizable(False, False)

# Load the image correctly
logo_img = ctk.CTkImage(light_image=Image.open("DD.png"), size=(100, 100))

# Create label and display image
logo_label = ctk.CTkLabel(window, image=logo_img, text="")
logo_label.pack(pady=10)

# Labels and Entry Fields
website_label = ctk.CTkLabel(window, text="Website:")
website_label.pack()
website_entry = ctk.CTkEntry(window, width=300)
website_entry.pack()

email_label = ctk.CTkLabel(window, text="Email/Username:")
email_label.pack()
email_entry = ctk.CTkEntry(window, width=300)
email_entry.pack()
email_entry.insert(0, "ujan.dattaa@gmail.com")

password_label = ctk.CTkLabel(window, text="Password:")
password_label.pack()
password_entry = ctk.CTkEntry(window, width=200)
password_entry.pack()

# Buttons
search_button = ctk.CTkButton(window, text="Search", command=find_password)
search_button.pack(pady=5)

generate_password_button = ctk.CTkButton(window, text="Generate Password", command=generate_password)
generate_password_button.pack(pady=5)

add_button = ctk.CTkButton(window, text="Add", command=save)
add_button.pack(pady=10)

window.mainloop()
