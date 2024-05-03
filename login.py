import tkinter as tk
from firebase_admin import credentials, db, initialize_app
import interface
from tkinter import messagebox

#cred = credentials.Certificate("serviceAccountKey.json")
#initialize_app(cred, {
    #'databaseURL': "https://faceattendance-8a4e1-default-rtdb.firebaseio.com/"
#})

reference = db.reference("Login")

def login():
    username = username_entry.get()
    password = password_entry.get()

    userData = reference.get()

    if  userData.get('paswword') == password:
        root.withdraw()  # Hide login window
        root.after(100, lambda: interface.Face_recognition_System(tk.Toplevel()))  # Open Face Recognition System window
    else:
        messagebox.showerror("Error", "Invalid username or password")

def create_login_interface():
    # Create Tkinter window
    global root  # Make root a global variable
    root = tk.Tk()
    root.title("Login")
    root.geometry("800x600")  # Set width and height of the window

    # Create username label and entry
    username_label = tk.Label(root, text="Username:")
    username_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)  # Center horizontally, 30% from the top
    global username_entry
    username_entry = tk.Entry(root, width=50)
    username_entry.place(relx=0.5, rely=0.35, anchor=tk.CENTER)  # Center horizontally, 35% from the top

    # Create password label and entry
    password_label = tk.Label(root, text="Password:")
    password_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)  # Center horizontally, 45% from the top
    global password_entry
    password_entry = tk.Entry(root, show="*", width=50)
    password_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center horizontally, 50% from the top

    # Create login button
    login_button = tk.Button(root, text="Login", command=login, width=20)
    login_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)  # Center horizontally, 65% from the top

    root.mainloop()

# Call the function to create the login interface
create_login_interface()
