import tkinter as tk
from tkinter import *
# import webbrowser
from tkinter import messagebox
from functools import partial
# from tkinter import filedialog as fd
from Recognition import Recognition
import webbrowser
from pandastable import Table
import pandas as pd
from datetime import datetime

app = Tk()
app.title('Face Recognition Attendance System')
app.iconbitmap('assets/jordan.ico')
app.geometry('1000x800')
menu = Menu(app)
app.config(menu=menu)
filemenu = Menu(menu, tearoff=False)
menu.add_cascade(label='File', menu=filemenu)
authorsmenu = Menu(menu, tearoff=False)
filemenu.add_cascade(label='Authors', menu=authorsmenu)
# openweb(url=i[1]))
[authorsmenu.add_cascade(label=i[0], command=lambda event: openweb(url=i[1])) for i in
 [['Ahmad Jaara', 'https://github.com/ahmadjaara'], ['Barham Farraj', 'https://github.com/Farraj007'],
  ['Eman Al-shaikh', 'https://github.com/Eman-Alshaikh'], ['Faisal Al Hawajreh', 'https://github.com/Faisal-Hawajreh'],
  ['Raneem Oqaily', 'https://github.com/Raneemoqaily7'], ['Zaid Jarrar', 'https://github.com/Zaid-Jarrar']]]
# [authorsmenu.add_command(label=i) for i in['Ahmad Jaara', 'Barham Farraj', 'Eman Al-shaikh', 'Faisal Al Hawajreh', 'Raneem Oqaily', 'Zaid Jarrar']]
filemenu.add_cascade(label='Version 1.0')
filemenu.add_separator()
filemenu.add_command(label='Exit', command=app.quit)
helpmenu = Menu(menu, tearoff=False)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About')

frame = tk.Frame(app).place(relheight=400, relwidth=500)
# frame.place(relx=0.2,rely=0.2,relheight=0.6,relwidth=0.6)

def page1(frame):
    def user_credential(username, password):
        if username.get() == "admin" and password.get() == 'admin':
            print('permission granted')
            page2(frame)
        else:
            messagebox.showerror('Error', 'Incorrect Username Or Password')
            # label=Label( text="Incorrect Username Or Password", width="400",bg="red", fg="white").pack()
            print("permission denied")

    tk.Label(frame, text="Welcome To Face Recognition Attendance System", width="400", bg="blue",fg="white").pack()
    # username label and text entry box

    tk.Label(frame, text="Username: ").place(relx=.38, rely=.2)
    username = StringVar()
    tk.Entry(frame, textvariable=username).place(relx=.5, rely=.2)
    # password label and password entry box
    tk.Label(frame, text="Password: ").place(relx=.38, rely=.4)
    password = StringVar()
    tk.Entry(frame, textvariable=password, show='*').place(relx=.5, rely=.4)
    user_credential = partial(user_credential, username, password)
    login = tk.Button(frame, text="Login",
                      pady=5, padx=30, bg="blue", fg='white', command=user_credential)
    login.place(relx=.4, rely=.6)
    app.bind('<Return>', lambda event: user_credential())

def page2(frame):
    def destroy():
        quit()

    def open_attendance():
        nonlocal frame
        import tkinter.ttk as ttk
        import csv
        newWindow = tk.Tk()
        # sets the title of the
        # Toplevel widget
        newWindow.title("Today's Attendance")
        # sets the geometry of toplevel
        newWindow.geometry("600x600")
        newWindow.iconbitmap('assets/jordan.ico')

        df = pd.read_csv("Attendance.csv")
        now = datetime.now()
        dateString = now.strftime('%Y-%m-%d')
        today = df[df['Date'] == dateString]

        frame = tk.Frame(newWindow)
        frame.pack(fill='both', expand=True)
        pt = Table(frame, dataframe=today)
        pt.show()
        # TableMargin = Frame(newWindow, width=600)
        # TableMargin.pack(side=TOP)
        # scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        # scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        # tree = ttk.Treeview(TableMargin, columns=("Name", "Day",'Date',"Time",'Status'), height=400,selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        # scrollbary.config(command=tree.yview)
        # scrollbary.pack(side=RIGHT, fill=Y)
        # scrollbarx.config(command=tree.xview)
        # scrollbarx.pack(side=BOTTOM, fill=X)
        # tree.heading('Name', text="Name", anchor=W)
        # tree.heading('Day', text="Day", anchor=W)
        # tree.heading('Date', text="Date", anchor=W)
        # tree.heading('Time', text="Time", anchor=W)
        # tree.heading('Status', text="Status", anchor=W)
        # tree.column('#0', stretch=NO, minwidth=0, width=0)
        # tree.column('#1', stretch=NO, minwidth=0, width=200)
        # tree.column('#2', stretch=NO, minwidth=0, width=200)
        # tree.column('#3', stretch=NO, minwidth=0, width=300)
        # tree.column('#4', stretch=NO, minwidth=0, width=300)
        # tree.column('#5', stretch=NO, minwidth=0, width=300)
        # tree.pack()
        #
        # with open('Today_Attendance.csv') as f:
        #     reader = csv.DictReader(f, delimiter=',')
        #     for row in reader:
        #         Name = row['Name']
        #         Day =  row['Day']
        #         Date = row['Date']
        #         Time = row['Time']
        #         Status=row['Status']
        #         tree.insert("", 0, values=(Name,Day, Date, Time,Status))

    frame = tk.Frame(frame).place(relheight=500, relwidth=500)
    button1 = tk.Button(frame, text='Attendance Today', height=10, width=20, pady=10, padx=30, bg='blue', fg='white',
                        command=lambda: open_attendance())
    button2 = tk.Button(frame, text='Employees', height=10, width=20, pady=10, padx=30, bg='blue', fg='white',
                        command=lambda: page4())
    button3 = tk.Button(frame, text='Live Cam', height=10, width=20, pady=10, padx=30, bg='blue', fg='white',
                        command=lambda: page3())
    button4 = tk.Button(frame, text='Exit', height=10, width=20, pady=10, padx=30, bg='blue', fg='white',
                        command=lambda: destroy())

    button1.place(relx=0.1, rely=0.3)
    button2.place(relx=0.4, rely=0.3)
    button3.place(relx=0.7, rely=0.3)
    button4.place(relx=0.4, rely=0.6)


def page3():
    live = Recognition()
    live.run()


def page4():
    def show_attendance(employee):
        employee = value_inside.get()
        df = pd.read_csv("Attendance.csv")
        names = df[df['Name'] == employee]
        frame = tk.Frame(newWindow)
        frame.place(relx=0, rely=0.2)
        pt = Table(frame, dataframe=names)
        pt.show()

    newWindow = tk.Tk()
    newWindow.title("Employees")
    newWindow.geometry("600x600")
    newWindow.iconbitmap('assets/jordan.ico')
    with open('DataSets/Employees.csv', 'r') as f:
        employees_data_sets = f.readlines()
        name_list = []
        for line in employees_data_sets:
            # if name in employees csv doesn't have comma in it, it won't read it and won't put it inside the name list
            entry = line.split(',')
            name_list.append(entry[0])
        print(name_list)
    value_inside = tk.StringVar(newWindow)
    value_inside.set("Select an Employee")
    question_menu = tk.OptionMenu(newWindow, value_inside, *name_list, command=show_attendance)
    question_menu.pack()

def openweb(url):
    webbrowser.open(url)


page1(frame)
# bt=tk.Button(app,text='page1',command=page1)
# bt.grid(column=0,row=0)

if __name__ == '__main__':
    app.mainloop()
