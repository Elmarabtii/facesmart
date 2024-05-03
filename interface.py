from tkinter import *
from PIL import Image, ImageTk
import os
#from student import Student
#from facesmart import Face_Recognition
from uu import EmployeeManagementSystem



class Face_recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # First Image
        img = Image.open(
            r"C:\Users\lucifer\Downloads\Facial-Recognition-Identification-master\Facial-Recognition-Identification-master\college_images\cybercheck.jpg")
        img = img.resize((500, 130))

        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=500, height=130)

        # Third Image
        img2 = Image.open(
            r"C:\Users\lucifer\Downloads\Facial-Recognition-Identification-master\Facial-Recognition-Identification-master\college_images\fig-touch.jpg")
        img2 = img2.resize((500, 130))
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=1000, y=0, width=500, height=130)

        # Bg Image
        img3 = Image.open(
            r"C:\Users\lucifer\Downloads\Facial-Recognition-Identification-master\Facial-Recognition-Identification-master\college_images\girlbg.jpg")
        img3 = img3.resize((1530, 710))
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=130, width=1530, height=710)

        title_lbl = Label(bg_img, text="Facial Recognition & Identification System",
                          font=("times new roman", 35, "bold"), bg="black", fg="white")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # Employee Details button
        img4 = Image.open(r"C:\Users\lucifer\Downloads\Facial-Recognition-Identification-master\Facial-Recognition-Identification-master\college_images\multiface-detect.jpg")
        img4 = img4.resize((220, 220))
        self.photoimg4 = ImageTk.PhotoImage(img4)

        b1 = Button(bg_img, image=self.photoimg4, command=self.employee_details, cursor="hand2")
        b1.place(x=200, y=100, width=220, height=220)

        b1_1 = Button(bg_img, text="Employee Details", command=self.employee_details, cursor="hand2",
                      font=("times new roman", 15, "bold"), bg="black", fg="white")
        b1_1.place(x=200, y=300, width=220, height=40)

        # Face Recognition button
        img5 = Image.open(r"C:\Users\lucifer\Downloads\Facial-Recognition-Identification-master\Facial-Recognition-Identification-master\college_images\gettyimages.jpg")
        img5 = img5.resize((220, 220))
        self.photoimg5 = ImageTk.PhotoImage(img5)

        b1 = Button(bg_img, image=self.photoimg5, cursor="hand2", command=self.run_facial_recognition)
        b1.place(x=630, y=100, width=220, height=220)

        b1_1 = Button(bg_img, text="Face Recognition", cursor="hand2", command=self.run_facial_recognition,
                      font=("times new roman", 15, "bold"), bg="black", fg="white")
        b1_1.place(x=630, y=300, width=220, height=40)

        # Exit button
        img10 = Image.open(
            r"C:\Users\lucifer\Downloads\Facial-Recognition-Identification-master\Facial-Recognition-Identification-master\college_images\sign-out-alt.jpg")
        img10 = img10.resize((220, 220))
        self.photoimg10 = ImageTk.PhotoImage(img10)

        b1 = Button(bg_img, image=self.photoimg10, cursor="hand2", command=self.exit_program)
        b1.place(x=1100, y=100, width=220, height=220)

        b1_1 = Button(bg_img, text="Exit Button", cursor="hand2", command=self.exit_program,
                      font=("times new roman", 15, "bold"), bg="black", fg="white")
        b1_1.place(x=1100, y=300, width=220, height=40)

    def employee_details(self):
        self.new_window = Toplevel(self.root)
        self.app = EmployeeManagementSystem(self.new_window, user="Admin")

    def run_facial_recognition(self):
        self.new_window = Toplevel(self.root)
        self.app = run_facial_recognition(self.new_window)

    def exit_program(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = Face_recognition_System(root)
    root.mainloop()

