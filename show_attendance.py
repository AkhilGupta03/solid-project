import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import csv

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get().strip()
        if not Subject:
            text_to_speech("Please select a department.")
            return
        
        subject_folder = f"Attendance/{Subject}"
        if not os.path.exists(subject_folder):
            text_to_speech(f"No attendance files found for {Subject}. Please check the folder.")
            return
        
        filenames = glob(os.path.join(subject_folder, "*.csv"))
        if not filenames:
            text_to_speech(f"No attendance files found for {Subject}. Please check the folder.")
            return
        
        # Read all CSV files and combine them
        df_list = []
        for f in filenames:
            df = pd.read_csv(f)
            # Ensure required columns exist
            if 'In-Time' not in df.columns:
                df['In-Time'] = ''
            if 'Out-Time' not in df.columns:
                df['Out-Time'] = ''
            if 'Date' not in df.columns:
                df['Date'] = pd.to_datetime('today').strftime('%Y-%m-%d')
            df_list.append(df)
        
        # Merge all dataframes
        newdf = pd.concat(df_list)
        
        # Calculate attendance percentage
        newdf['Attendance'] = newdf.apply(
            lambda x: '100%' if x['In-Time'] and x['Out-Time'] else '50%' if x['In-Time'] or x['Out-Time'] else '0%',
            axis=1
        )
        
        # Save combined attendance
        attendance_file = os.path.join(subject_folder, "attendance.csv")
        newdf.to_csv(attendance_file, index=False)
        
        # Create new window to display attendance
        att_window = Toplevel()
        att_window.title(f"Attendance of {Subject}")
        att_window.geometry("800x400")
        att_window.configure(background="white")
        
        # Create Treeview with scrollbars
        tree = ttk.Treeview(att_window)
        tree["columns"] = list(newdf.columns)
        tree["show"] = "headings"
        
        for col in newdf.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        for _, row in newdf.iterrows():
            tree.insert("", "end", values=list(row))
        
        vsb = ttk.Scrollbar(att_window, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(att_window, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        tree.grid(column=0, row=0, sticky="nsew")
        vsb.grid(column=1, row=0, sticky="ns")
        hsb.grid(column=0, row=1, sticky="ew")
        
        att_window.grid_columnconfigure(0, weight=1)
        att_window.grid_rowconfigure(0, weight=1)

    subject = Tk()
    subject.title("Subject Selection")
    subject.geometry("580x320")
    subject.configure(background="white")
    
    Label(subject, text="Select Department", bg="white", fg="red", font=("arial", 25)).place(x=130, y=12)

    def Attf():
        sub = tx.get().strip()
        if not sub:
            text_to_speech("Please select a department!")
        else:
            subject_path = f"Attendance/{sub}"
            if os.path.exists(subject_path):
                os.startfile(subject_path)
            else:
                text_to_speech(f"No attendance files found for {sub}. Please check the folder.")

    Button(subject, text="Check Sheets", command=Attf, bd=7, font=("times new roman", 15),
           bg="white", fg="black", height=2, width=10, relief=RIDGE).place(x=360, y=170)
    
    Label(subject, text="Department", width=10, height=2, bg="white", fg="black", bd=5, relief=RIDGE,
          font=("times new roman", 15)).place(x=50, y=100)
    
    departments = ["Sales", "IT", "Bid", "Pre Sales"]
    tx = ttk.Combobox(subject, values=departments, font=("times", 20), state="readonly", width=15)
    tx.current(0)
    tx.place(x=190, y=110)

    Button(subject, text="View Attendance", command=calculate_attendance, bd=7, font=("times new roman", 15),
           bg="white", fg="black", height=2, width=12, relief=RIDGE).place(x=195, y=170)
    
    subject.mainloop()
