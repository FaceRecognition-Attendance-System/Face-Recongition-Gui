import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
# from functools import partial
from face_recognition_ref.Recognition import Recognition
from pandastable import Table
import pandas as pd
from datetime import datetime


class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load = Image.open("assets/main_bg.jpg").resize((800, 600), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)


        Label(self, text="Login Here", font=("Arlian", 34, "bold"), fg="#3393FF").place(x=250, y=190)
        Label(self, text="Attendence Management System ", font=("Goudyold style", 10, "bold"),
              fg="#3393FF").place(x=250, y=260)

        Label(self, text=" Username ", font=("Goudyold style", 15, "bold"), fg="#77827D").place(
            x=250, y=300)
        txt_user = Entry(self, font=("times new roman", 15), bg="lightgray")
        txt_user.place(x=250, y=330, width=250, height=35)

        Label(self, text=" Password ", font=("Goudyold style", 15, "bold"), fg="#77827D").place(
            x=250, y=370)
        txt_pass = Entry(self, show='*', font=("times new roman", 15), bg="lightgray")
        txt_pass.place(x=250, y=400, width=250, height=35)

        txt_user.bind('<Return>', lambda event: verify())
        txt_pass.bind('<Return>', lambda event: verify())

        def verify():
            try:
                with open("DataSets/credential.txt", "r") as f:
                    info = f.readlines()
                    i = 0
                    for e in info:
                        u, p = e.split(",")
                        if u.strip() == txt_user.get() and p.strip() == txt_pass.get():
                            controller.show_frame(SecondPage)
                            txt_user.delete(0, END)
                            txt_pass.delete(0, END)
                            i = 1
                            break
                    if i == 0:
                        messagebox.showerror("Error", "Please provide correct username and password!!")
            except:
                messagebox.showerror("Error", "Please provide correct username and password!!")

        B2 = tk.Button(self, text="Login", bg="#3393FF", font=("Arial Bold", 15), fg='white', command=verify)
        B2.place(x=320, y=450)


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load = Image.open("assets/main_bg.jpg").resize((800, 600), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)
        title_lbl = Label(label, text="FACE RECOGNITION ATTENDANCE SYSTEM", font=("Arial Bold", 20),
                          bg="#2CB2FF", fg="white")
        title_lbl.place(relx=0, rely=0, width=800, height=30)
        button1 = tk.Button(self, text='Attendance Today', pady=10, padx=10, bg='#5CB8FF',
                            fg='white', font=("Arial", 15), width=15,
                            command=lambda: self.open_attendance())
        button2 = tk.Button(label, text='Attendance Log', pady=10, padx=10, bg='#5CB8FF',
                            fg='white', font=("Arial", 15), width=15,
                            command=lambda: self.employee_attendance())
        button3 = tk.Button(label, text='Live Cam', pady=10, padx=10, bg='#5CB8FF',
                            fg='white', font=("Arial", 15), width=15,
                            command=lambda: self.start_face_recognintion())
        button4 = tk.Button(label, text='Exit', pady=10, padx=10, bg='#5CB8FF',
                            fg='white', font=("Arial", 15), width=15,
                            command=lambda: quit())

        button1.place(relx=0.05, rely=0.32)
        button2.place(relx=0.38, rely=0.32)
        button3.place(relx=0.72, rely=0.32)
        button4.place(relx=0.38, rely=0.6)

        group_name = tk.Button(self, text="Remote Coders \xa9", bg='#5CB8FF', font=("Arial Bold", 15), width=20,
                               fg='white',
                               command=lambda: openweb(url='https://github.com/FaceRecognition-Attendance-System'))
        group_name.place(relx=0.71, rely=0.87)

        Buttonb = tk.Button(self, text="Log Out", bg='#5CB8FF', font=("Arial Bold", 15), width=8, fg='white',
                            command=lambda: controller.show_frame(FirstPage))
        Buttonb.place(relx=0.01, rely=0.87)

    @staticmethod
    def start_face_recognintion():
        live = Recognition()
        live.run()

    def open_attendance(self):
        new_window = tk.Tk()
        new_window.title("Today's Attendance")
        new_window.geometry("600x600")
        new_window.iconbitmap('assets/face.ico')

        df = pd.read_csv('face_recognition_ref/attendance.csv')
        now = datetime.now()
        date_string = now.strftime('%Y-%m-%d')
        today = df[df['Date'] == date_string]

        frame = tk.Frame(new_window)
        frame.pack(fill='both', expand=True)
        pt = Table(frame, dataframe=today)
        pt.show()

    def employee_attendance(self):
        def show_attendance(employee):
            def monthly_percentage():
                nonlocal names
                monthly_attendance_percentage = round((len(names.index) / 26 * 100))
                if monthly_attendance_percentage > 70:
                    label = Label(new_window, text=f'{monthly_attendance_percentage}%', bg='green', width=25)
                    label.place(relx=.63, rely=0.01)
                else:
                    label = Label(new_window, text=f'Monthly Attendance Rate is {monthly_attendance_percentage}%',
                                  bg='red', width=25)
                    label.place(relx=.63, rely=0.01)
                return monthly_attendance_percentage

            employee = value_inside.get()
            df = pd.read_csv('face_recognition_ref/attendance.csv')
            names = df[df['Name'] == employee]
            monthly_percentage()
            frame = tk.Frame(new_window)
            frame.place(relx=0, rely=0.15)
            pt = Table(frame, dataframe=names, width=600)
            pt.show()

        new_window = tk.Tk()
        new_window.title("Attendance Log")
        new_window.geometry("600x300")
        new_window.iconbitmap('assets/face.ico')
        with open('DataSets/Employees.csv', 'r') as f:
            employees_data_sets = f.readlines()
            name_list = []
            for line in employees_data_sets:
                # if name in employees csv doesn't have comma in it, it won't read it and won't put it inside the name list
                entry = line.split(',')
                name_list.append(entry[0])
        value_inside = tk.StringVar(new_window)
        value_inside.set("Select an Employee")
        question_menu = tk.OptionMenu(new_window, value_inside, *name_list, command=show_attendance)
        question_menu.place(relx=0.01, rely=0.01, width=200)


class ThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self)
        load = Image.open("assets/main_bg.jpg").resize((800, 600), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)
        Label = tk.Label(label,
                         text="For Our Future Work \n We can Add a new page.Hope you liked the work! \n Functionality over design",
                         bg="#6a8fa6", font=("Arial Bold", 25), fg='#26232e')
        Label.place(x=40, y=150)

        Buttonn = tk.Button(label, text="Next", bg='#26232e', font=("Arial Bold", 15), width=8, fg='#e6eaf5',
                            command=lambda: controller.show_frame(SecondPage))
        Buttonn.place(relx=0.87, rely=0.87)

        Buttonb = tk.Button(self, text="Log Out", bg='#26232e', font=("Arial Bold", 15), width=8, fg='#e6eaf5',
                            command=lambda: controller.show_frame(FirstPage))
        Buttonb.place(relx=0.01, rely=0.87)


class Application(tk.Tk):
    """
        In this Class the Main Frame & Specifications for the application will be configured
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        app = self
        app.title('Face Recognition Attendance System')
        app.iconbitmap("assets/face.ico")
        app.geometry('1530x790')
        menu = Menu(app)
        app.config(menu=menu)
        filemenu = Menu(menu, tearoff=False)
        menu.add_cascade(label='File', menu=filemenu)
        authorsmenu = Menu(menu, tearoff=False)
        filemenu.add_cascade(label='Authors', menu=authorsmenu)
        [authorsmenu.add_cascade(label=i) for i in
         ['Ahmad Jaara', 'Barham Farraj', 'Eman Al-shaikh', 'Faisal Al Hawajreh', 'Raneem Oqaily', 'Zaid Jarrar']]
        filemenu.add_cascade(label='Version 1.0')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=app.quit)
        helpmenu = Menu(menu, tearoff=False)
        menu.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label='About us'
                             , command=lambda: openweb(url='https://github.com/FaceRecognition-Attendance-System'))

        # creating a window
        window = tk.Frame(self)
        window.pack()
        window.grid_rowconfigure(0, minsize=600)
        window.grid_columnconfigure(0, minsize=800)

        self.frames = {}
        for F in (FirstPage, SecondPage, ThirdPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstPage)

    def show_frame(self, page):
        """
            This Method will show a specific frame as needed."switch between frames"
        """
        frame = self.frames[page]
        frame.tkraise()
        self.title("Face Recognition Attendance System")

def openweb(url):
    """
        This method give Access the code to open a URL from The WEB
    """
    webbrowser.open(url)
    return True


if __name__ == '__main__':
    app = Application()
    app.maxsize(800, 600)
    app.mainloop()
