import firebase_admin
from firebase_admin import credentials, db, storage
from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import os
import random
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your service account key
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-8a4e1-default-rtdb.firebaseio.com/",
    'storageBucket': 'faceattendance-8a4e1.appspot.com'
})
bucket = storage.bucket()


def generate_unique_id():
    return str(random.randint(100000, 999999))


class EmployeeManagementSystem:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.geometry("900x700")
        self.root.title("Employee Management System")

        self.db = db.reference('Students')

        # Employee Treeview
        self.tree_style = ttk.Style()
        self.tree_style.theme_use("clam")
        self.tree_style.configure("Treeview", background="#f0f0f0", foreground="#333333", fieldbackground="#f0f0f0",
                                  font=("Arial", 10))
        self.tree_style.map("Treeview", background=[("selected", "#0078d7")])

        self.tree = ttk.Treeview(root, columns=(
            "ID", "Name", "Position", "Starting Year", "Last Attendance", "Total Attendance"),
                                 selectmode="extended", style="Treeview")
        self.tree.heading("#0", text="", anchor=CENTER)
        self.tree.heading("ID", text="ID", anchor=CENTER)
        self.tree.heading("Name", text="Name", anchor=CENTER)
        self.tree.heading("Position", text="Position", anchor=CENTER)
        self.tree.heading("Starting Year", text="Starting Year", anchor=CENTER)
        self.tree.heading("Last Attendance", text="Last Attendance", anchor=CENTER)
        self.tree.heading("Total Attendance", text="Total Attendance", anchor=CENTER)
        self.tree.column("#0", width=0, stretch=NO)  # Hide the first column
        self.tree.column("ID", width=100, anchor=CENTER)
        self.tree.column("Name", width=150, anchor=W)
        self.tree.column("Position", width=150, anchor=CENTER)
        self.tree.column("Starting Year", width=150, anchor=CENTER)
        self.tree.column("Last Attendance", width=150, anchor=CENTER)
        self.tree.column("Total Attendance", width=150, anchor=CENTER)
        self.tree.pack(fill=BOTH, expand=True)

        # Add employees to the Treeview
        self.refresh_treeview()

        # Search Entry
        search_frame = Frame(root)
        search_frame.pack(pady=10)
        search_label = Label(search_frame, text="Search:")
        search_label.grid(row=0, column=0, padx=5)
        self.search_var = StringVar()
        self.search_entry = Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_var.trace("w", self.filter_treeview)

        # Buttons
        button_frame = Frame(root)
        button_frame.pack(pady=10)

        self.add_button = Button(button_frame, text="Add Employee", command=self.open_add_employee_window)
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = Button(button_frame, text="Edit Employee", command=self.edit_employee)
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = Button(button_frame, text="Delete Employee", command=self.delete_employee)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.refresh_button = Button(button_frame, text="Refresh", command=self.refresh_treeview)
        self.refresh_button.grid(row=0, column=3, padx=5)

    def refresh_treeview(self):
        self.tree.delete(*self.tree.get_children())
        employees_data = self.db.get()
        if employees_data:
            for employee_id, employee_data in employees_data.items():
                self.tree.insert("", "end", text="", values=(
                    employee_id, employee_data.get("name", ""), employee_data.get("position", ""),
                    employee_data.get("starting_year", ""), employee_data.get("last_attendance_time", ""),
                    employee_data.get("total_attendance", "")))

    def filter_treeview(self, *args):
        search_term = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        employees_data = self.db.get()
        if employees_data:
            for employee_id, employee_data in employees_data.items():
                if search_term in employee_data.get("name", "").lower() or search_term in employee_data.get(
                        "position", "").lower():
                    self.tree.insert("", "end", text="", values=(
                        employee_id, employee_data.get("name", ""), employee_data.get("position", ""),
                        employee_data.get("starting_year", ""), employee_data.get("last_attendance_time", ""),
                        employee_data.get("total_attendance", "")))

    def open_add_employee_window(self):
        add_employee_window = AddEmployeeWindow(self.root, self.user, self)

    def edit_employee(self):
        selected_items = self.tree.selection()
        if selected_items:
            selected_employee_id = self.tree.item(selected_items[0])["values"][0]
            print("Selected Employee ID:", selected_employee_id)  # Debugging statement
            employees_data = self.db.get()
            print("Employees Data:", employees_data)  # Debugging statement
            if employees_data:
                print("Keys in Employees Data:", employees_data.keys())  # Debugging statement
                if selected_employee_id in employees_data:
                    selected_employee_data = employees_data[selected_employee_id]
                    print("Selected Employee Data:", selected_employee_data)  # Debugging statement
                    if selected_employee_data:
                        edit_window = EditEmployeeWindow(self.root, self, selected_employee_id,
                                                         selected_employee_data)
                    else:
                        messagebox.showinfo("Error", "Employee data not found.")
                else:
                    messagebox.showinfo("Error", "Selected employee ID not found in database.")
            else:
                messagebox.showinfo("Error", "No data found in database.")
        else:
            messagebox.showinfo("Error", "Please select an employee to edit.")

    def delete_employee(self):
        selected_items = self.tree.selection()
        if selected_items:
            selected_employee_id = self.tree.item(selected_items[0])["values"][0]
            if selected_employee_id is not None and selected_employee_id != "":
                print("Selected Employee ID:", selected_employee_id)  # Debugging statement
                self.db.child(str(selected_employee_id)).delete()  # Convert to string before passing
                self.refresh_treeview()
            else:
                messagebox.showinfo("Error", "Invalid employee ID.")
        else:
            messagebox.showinfo("Error", "Please select an employee to delete.")


class AddEmployeeWindow:
    def __init__(self, parent, user, app):
        self.parent = parent
        self.user = user
        self.app = app
        self.window = Toplevel(parent)
        self.window.title("Add Employee")

        main_frame = Frame(self.window)
        main_frame.pack(padx=20, pady=10)

        self.name_label = Label(main_frame, text="Name:")
        self.name_label.grid(row=0, column=0, pady=5, sticky=W)
        self.name_entry = Entry(main_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.position_label = Label(main_frame, text="Position:")
        self.position_label.grid(row=1, column=0, pady=5, sticky=W)
        self.position_entry = Entry(main_frame, width=30)
        self.position_entry.grid(row=1, column=1, padx=5, pady=5)

        self.starting_year_label = Label(main_frame, text="Starting Year:")
        self.starting_year_label.grid(row=2, column=0, pady=5, sticky=W)
        self.starting_year_entry = Entry(main_frame, width=30)
        self.starting_year_entry.grid(row=2, column=1, padx=5, pady=5)

        self.last_attendance_label = Label(main_frame, text="Last Attendance:")
        self.last_attendance_label.grid(row=3, column=0, pady=5, sticky=W)
        self.last_attendance_entry = Entry(main_frame, width=30)
        self.last_attendance_entry.grid(row=3, column=1, padx=5, pady=5)

        self.total_attendance_label = Label(main_frame, text="Total Attendance:")
        self.total_attendance_label.grid(row=4, column=0, pady=5, sticky=W)
        self.total_attendance_entry = Entry(main_frame, width=30)
        self.total_attendance_entry.grid(row=4, column=1, padx=5, pady=5)

        self.image_label = Label(main_frame, text="Image:")
        self.image_label.grid(row=5, column=0, pady=5, sticky=W)
        self.image_entry = Entry(main_frame, width=30, state="readonly")
        self.image_entry.grid(row=5, column=1, padx=5, pady=5)
        self.browse_button = Button(main_frame, text="Browse", command=self.browse_image)
        self.browse_button.grid(row=5, column=2, padx=5, pady=5)

        self.add_button = Button(main_frame, text="Add", command=self.add_employee)
        self.add_button.grid(row=6, column=0, columnspan=2, pady=10)

    def browse_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=(("Image files", "*.png *.jpg"),))
        if file_path:
            self.image_entry.config(state="normal")
            self.image_entry.delete(0, END)
            self.image_entry.insert(0, file_path)
            self.image_entry.config(state="readonly")

    def add_employee(self):
        name = self.name_entry.get()
        position = self.position_entry.get()
        starting_year = self.starting_year_entry.get()
        # Get the current date and time
        last_attendance = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_attendance = self.total_attendance_entry.get()
        employee_id = generate_unique_id()

        # Upload image to Firebase Storage
        image_path = self.image_entry.get()
        if image_path:
            blob = bucket.blob(f"Images/{employee_id}.png")
            blob.upload_from_filename(image_path)

        self.app.db.child(employee_id).set({
            "name": name,
            "position": position,
            "starting_year": starting_year,
            "last_attendance_time": last_attendance,
            "total_attendance": total_attendance,
            "image_url": f"faceattendance-8a4e1.appspot.com{bucket.name}/Images/{employee_id}.png"
        })
        self.app.refresh_treeview()
        self.window.destroy()


class EditEmployeeWindow:
    def __init__(self, parent, app, employee_id, employee_data):
        self.parent = parent
        self.app = app
        self.employee_id = employee_id
        self.employee_data = employee_data
        self.window = Toplevel(parent)
        self.window.title("Edit Employee")

        main_frame = Frame(self.window)
        main_frame.pack(padx=20, pady=10)

        self.name_label = Label(main_frame, text="Name:")
        self.name_label.grid(row=0, column=0, pady=5, sticky=W)
        self.name_entry = Entry(main_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.insert(0, self.employee_data.get("name", ""))

        self.position_label = Label(main_frame, text="Position:")
        self.position_label.grid(row=1, column=0, pady=5, sticky=W)
        self.position_entry = Entry(main_frame, width=30)
        self.position_entry.grid(row=1, column=1, padx=5, pady=5)
        self.position_entry.insert(0, self.employee_data.get("position", ""))

        self.starting_year_label = Label(main_frame, text="Starting Year:")
        self.starting_year_label.grid(row=2, column=0, pady=5, sticky=W)
        self.starting_year_entry = Entry(main_frame, width=30)
        self.starting_year_entry.grid(row=2, column=1, padx=5, pady=5)
        self.starting_year_entry.insert(0, self.employee_data.get("starting_year", ""))

        self.last_attendance_label = Label(main_frame, text="Last Attendance:")
        self.last_attendance_label.grid(row=3, column=0, pady=5, sticky=W)
        self.last_attendance_entry = Entry(main_frame, width=30)
        self.last_attendance_entry.grid(row=3, column=1, padx=5, pady=5)
        self.last_attendance_entry.insert(0, self.employee_data.get("last_attendance_time", ""))

        self.total_attendance_label = Label(main_frame, text="Total Attendance:")
        self.total_attendance_label.grid(row=4, column=0, pady=5, sticky=W)
        self.total_attendance_entry = Entry(main_frame, width=30)
        self.total_attendance_entry.grid(row=4, column=1, padx=5, pady=5)
        self.total_attendance_entry.insert(0, self.employee_data.get("total_attendance", ""))

        self.save_button = Button(main_frame, text="Save", command=self.save_employee)
        self.save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def save_employee(self):
        new_name = self.name_entry.get()
        new_position = self.position_entry.get()
        new_starting_year = self.starting_year_entry.get()
        new_last_attendance = self.last_attendance_entry.get()
        new_total_attendance = self.total_attendance_entry.get()
        print("New Name:", new_name)
        print("New Position:", new_position)
        print("New Starting Year:", new_starting_year)
        print("New Last Attendance:", new_last_attendance)
        print("New Total Attendance:", new_total_attendance)
        self.app.db.child(self.employee_id).update({
            "name": new_name,
            "position": new_position,
            "starting_year": new_starting_year,
            "last_attendance_time": new_last_attendance,
            "total_attendance": new_total_attendance
        })
        self.app.refresh_treeview()
        self.window.destroy()


if __name__ == "__main__":
    root = Tk()
    user = "Admin"  # User who is currently logged in
    app = EmployeeManagementSystem(root, user)
    root.mainloop()
