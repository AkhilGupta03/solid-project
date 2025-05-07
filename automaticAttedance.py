import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font
import pyttsx3

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "TrainingImageLabel\\Trainner.yml"
)
trainimage_path = "TrainingImage"
studentdetail_path = (
    "StudentDetails\\studentdetails.csv"
)  
attendance_path = "Attendance"
 

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def text_to_speech(user_text):
    engine.say(user_text)
    engine.runAndWait()

# for choose subject and fill attendance
def subjectChoose(text_to_speech):
    subject = tk.Toplevel()
    subject.title("Subject...")
    subject.geometry("580x400")
    subject.resizable(0, 0)
    subject.configure(background="white")

    titl = tk.Label(subject, bg="white", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    titl = tk.Label(
        subject,
        text="Select the Department",
        bg="white",
        fg="red",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="white",
        fg="yellow",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )
    Notifica.place(x=20, y=300)
    Notifica.config(text="")

    # Dropdown for departments
    from tkinter import ttk
    departments = ["Sales", "IT", "Bid", "Pre Sales"]
    tx = ttk.Combobox(
        subject,
        values=departments,
        font=("times", 20),
        state="readonly",
        width=15,
    )
    tx.current(0)
    tx.place(x=190, y=110)

    def FillInTimeAttendance():
        FillAttendance("In-Time")

    def FillOutTimeAttendance():
        FillAttendance("Out-Time")

    def FillAttendance(attendance_type):
        sub = tx.get().strip()
        if not sub:
            t = "Please select a department!"
            text_to_speech(t)
            Notifica.config(text=t, fg="black", bg="white")
            Notifica.place(x=20, y=300)
            return

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            try:
                recognizer.read(trainimagelabel_path)
            except Exception as e:
                error_msg = "Model not found, please train the model first!"
                Notifica.config(text=error_msg, bg="white", fg="black", width=33, font=("times", 15, "bold"))
                Notifica.place(x=20, y=250)
                text_to_speech(error_msg)
                return

            facecasCade = cv2.CascadeClassifier(haarcasecade_path)
            df = pd.read_csv(studentdetail_path)
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ["Enrollment", "Name", "Date", "In-Time", "Out-Time"]
            attendance = pd.DataFrame(columns=col_names)
            start_time = time.time()
            capture_duration = 20

            while True:
                ret, im = cam.read()
                if not ret:
                    messagebox.showerror("Error", "Could not open camera.")
                    break
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = facecasCade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    cv2.putText(im, f"Conf: {int(conf)}", (x, y-10), font, 0.8, (0, 255, 255), 2)

                    if conf < 50:
                        global Subject
                        global aa
                        global date
                        global timeStamp
                        Subject = sub
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                        aa = df.loc[df["Enrollment"] == Id]["Name"].values
                        tt = str(Id) + "-" + aa[0]
                        attendance.loc[len(attendance)] = [Id, aa[0], date, timeStamp if attendance_type == "In-Time" else "", "" if attendance_type == "In-Time" else timeStamp]
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)
                    else:
                        Id = "Unknown"
                        tt = str(Id)
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

                cv2.imshow("Filling Attendance...", im)
                if cv2.waitKey(30) & 0xFF == 27 or (time.time() - start_time) > capture_duration:
                    break

            cam.release()
            cv2.destroyAllWindows()

            if not attendance.empty:
                attendance = attendance.drop_duplicates(subset=['Enrollment'], keep='first')
                path = os.path.join(attendance_path, Subject)
                os.makedirs(path, exist_ok=True)
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                existing_files = [f for f in os.listdir(path) if f.startswith(f"{Subject}_{today}")]

                if existing_files and attendance_type == "Out-Time":
                    existing_file = os.path.join(path, existing_files[0])
                    existing_df = pd.read_csv(existing_file)
                    for idx, row in attendance.iterrows():
                        mask = existing_df['Enrollment'] == row['Enrollment']
                        existing_df['In-Time'] = existing_df['In-Time'].astype(str)
                        existing_df['Out-Time'] = existing_df['Out-Time'].astype(str)
                        existing_df.loc[mask, 'Out-Time'] = str(row['Out-Time'])
                    existing_df.to_csv(existing_file, index=False)
                else:
                    ts = time.time()
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                    Hour, Minute, Second = timeStamp.split(":")
                    fileName = f"{path}/{Subject}_{today}_{Hour}-{Minute}-{Second}.csv"
                    attendance.to_csv(fileName, index=False)

                m = f"Attendance Filled Successfully for {Subject}"
                Notifica.config(text=m, bg="white", fg="black", width=33, relief=RIDGE, bd=5, font=("times", 15, "bold"))
                Notifica.place(x=50, y=250)
                text_to_speech(m)
                if existing_files and attendance_type == "Out-Time":
                    show_attendance_table(existing_file, Subject)
                else:
                    show_attendance_table(fileName, Subject)
            else:
                f = "No Face found for attendance"
                Notifica.config(text=f, bg="white", fg="black", width=33, font=("times", 15, "bold"))
                Notifica.place(x=20, y=250)
                text_to_speech(f)

        except Exception as e:
            error_msg = f"An error occurred: {e}"
            Notifica.config(text=error_msg, bg="white", fg="black", width=33, font=("times", 15, "bold"))
            Notifica.place(x=20, y=250)
            text_to_speech(error_msg)
            cv2.destroyAllWindows()

    def show_attendance_table(file_path, subject_name):
        root = tk.Toplevel(subject)
        root.title(f"Attendance of {subject_name}")
        root.configure(background="white")
        root.geometry("800x400")

        try:
            df = pd.read_csv(file_path)
            if df.empty:
                messagebox.showinfo("Info", f"No attendance data found for {subject_name}.")
                root.destroy()
                return

            tree = tkk.Treeview(root)
            tree["columns"] = list(df.columns)
            tree["show"] = "headings"

            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor="center")

            for i, row in df.iterrows():
                tree.insert("", "end", values=list(row))

            vsb = tkk.Scrollbar(root, orient="vertical", command=tree.yview)
            hsb = tkk.Scrollbar(root, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            tree.grid(column=0, row=0, sticky="nsew")
            vsb.grid(column=1, row=0, sticky="ns")
            hsb.grid(column=0, row=1, sticky="ew")

            root.grid_columnconfigure(0, weight=1)
            root.grid_rowconfigure(0, weight=1)
            root.mainloop()
        except FileNotFoundError:
            messagebox.showerror("Error", f"Attendance file not found: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while displaying attendance: {e}")

    def Attf():
        sub = tx.get().strip()
        if not sub:
            t = "Please select a department!"
            text_to_speech(t)
            Notifica.config(text=t, fg="black", bg="white")
            Notifica.place(x=20, y=250)
            return
        folder_path = os.path.join(attendance_path, sub)
        os.makedirs(folder_path, exist_ok=True)
        try:
            os.startfile(folder_path)
        except OSError:
            messagebox.showerror("Error", f"Could not open folder: {folder_path}. Please check your default file explorer.")

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="white",
        fg="black",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub_label = tk.Label(
        subject,
        text="Department",
        width=10,
        height=2,
        bg="white",
        fg="black",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub_label.place(x=50, y=100)

    fill_in = tk.Button(
        subject,
        text="In-Time Attendance",
        command=FillInTimeAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="white",
        fg="green",
        height=2,
        width=15,
        relief=RIDGE,
    )
    fill_in.place(x=100, y=170)

    fill_out = tk.Button(
        subject,
        text="Out-Time Attendance",
        command=FillOutTimeAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="white",
        fg="red",
        height=2,
        width=15,
        relief=RIDGE,
    )
    fill_out.place(x=300, y=170)

    subject.mainloop()
