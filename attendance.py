import tkinter as tk
from tkinter import messagebox
import os
import cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import pyttsx3 

# Project modules
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# Initialize the text-to-speech engine
engine = pyttsx3.init()
 
def text_to_speech(user_text):
    engine.say(user_text)
    engine.runAndWait()

# File paths 

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# Custom button style
def create_button(parent, text, command, x, y, width=17, height=2):
    btn = tk.Button(parent, 
                   text=text, 
                   command=command,
                   bd=0,
                   font=("Arial", 14, "bold"),
                   bg="#333333",
                   fg="white",
                   activebackground="#555555",
                   activeforeground="white",
                   width=width,
                   height=height,
                   relief=tk.RIDGE)
    btn.place(x=x, y=y)
    # Add hover effects
    def on_enter(e):
        btn['background'] = '#444444'
    def on_leave(e):
        btn['background'] = '#333333'
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# Main window setup
window = tk.Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
window.configure(background="white")

# Custom fonts
title_font = ("Arial", 35, "bold")
subtitle_font = ("Arial", 24)
button_font = ("Arial", 14, "bold")

def del_sc1(sc1):
    sc1.destroy()

def err_screen():
    sc1 = tk.Toplevel(window)
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="white")
    sc1.resizable(0, 0)
    tk.Label(sc1, text="Enrollment & Name required!!!", fg="yellow", bg="black", font=("Arial", 16, "bold")).pack()
    btn = create_button(sc1, "OK", lambda: del_sc1(sc1), 150, 50, 9, 1)
 
def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

# Load logo
"""try:
    logo = Image.open("UI_Image/0001.jpg")
    logo = logo.resize((50, 47), Image.LANCZOS)
    logo1 = ImageTk.PhotoImage(logo)
except FileNotFoundError:
    print("Warning: UI_Image/0001.jpg not found. Please ensure the image file exists.")
    """
logo1 = None

# Header frame
header_frame = tk.Frame(window, bg="white", height=100)
header_frame.pack(fill=tk.X, pady=10)

if logo1:
    l1 = tk.Label(header_frame, image=logo1, bg="white")
    l1.pack(side=tk.LEFT, padx=20)
    l1.image = logo1  # Keep a reference to prevent garbage collection

# Main title
main_title = tk.Label(header_frame, 
                     text="Akhil Gupta", 
                     bg="white", 
                     fg="red", 
                     font=("Arial", 24, "bold"))
main_title.pack(side=tk.LEFT, padx=10)

# Subtitle
subtitle = tk.Label(window, 
                   text="Attendance using \nFace Recognition", 
                   bg="white",  
                   fg="black", 
                   font=title_font)
subtitle.pack(pady=20)

# Load images for buttons
def load_image(path, x, y):
    try:
        img = Image.open(path)
        img_tk = ImageTk.PhotoImage(img)
        label = tk.Label(window, image=img_tk)
        label.image = img_tk  # Keep a reference to prevent garbage collection
        label.place(x=x, y=y)
    except FileNotFoundError:
        print(f"Warning: {path} not found.")

load_image("UI_Image/register.png", 101, 270)
load_image("UI_Image/attendance.png", 960, 270)
load_image("UI_Image/verifyy.png", 600, 270)

def TakeImageUI():
    ImageUI = tk.Toplevel(window)
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="white")
    ImageUI.resizable(0, 0)

    # Title
    tk.Label(ImageUI, bg="white", relief=tk.RIDGE, bd=10, font=("arial", 35)).pack(fill=tk.X)
    tk.Label(ImageUI, text="Register Your Face", bg="white", fg="red", font=("arial", 30)).place(x=235, y=12)
    tk.Label(ImageUI, text="Enter the details", bg="white", fg="black", bd=10, font=("arial", 24)).place(x=280, y=75)

    # Enrollment No
    tk.Label(ImageUI, text="Employee ID", width=10, height=2, bg="white", fg="black", bd=5, relief=tk.RIDGE, font=("times new roman", 12)).place(x=120, y=130)
    txt1 = tk.Entry(ImageUI, width=17, bd=5, validate="key", bg="white", fg="red", relief=tk.RIDGE, font=("times", 25, "bold"))
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Name
    tk.Label(ImageUI, text="Name", width=10, height=2, bg="white", fg="black", bd=5, relief=tk.RIDGE, font=("times new roman", 12)).place(x=120, y=200)
    txt2 = tk.Entry(ImageUI, width=17, bd=5, bg="white", fg="black", relief=tk.RIDGE, font=("times", 25, "bold"))
    txt2.place(x=250, y=200)

    # Notification
    tk.Label(ImageUI, text="Notification", width=10, height=2, bg="white", fg="black", bd=5, relief=tk.RIDGE, font=("times new roman", 12)).place(x=120, y=270)
    message = tk.Label(ImageUI, text="", width=32, height=2, bd=5, bg="white", fg="yellow", relief=tk.RIDGE, font=("times", 12, "bold"))
    message.place(x=250, y=270)

    def take_image():
        enrollment = txt1.get()
        name = txt2.get()
        if not enrollment or not name:
            messagebox.showerror("Error", "Enrollment No and Name are required!")
            return
        takeImage.TakeImage(enrollment, name, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech)
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # Take Image button
    tk.Button(ImageUI, text="Take Image", command=take_image, bd=10, font=("times new roman", 18), bg="white", fg="black", height=2, width=12, relief=tk.RIDGE).place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech)

    # Train Image button
    tk.Button(ImageUI, text="Train Image", command=train_image, bd=10, font=("times new roman", 18), bg="white", fg="black", height=2, width=12, relief=tk.RIDGE).place(x=360, y=350)

# Main action buttons - placed below corresponding images
# Register a new student button (below register.png at 100,270)
create_button(window, "Register new Employee", TakeImageUI, 100, 500,19)

def automatic_attendance():
    automaticAttedance.subjectChoose(text_to_speech)

# Take Attendance button (below verifyy.png at 600,270)
create_button(window, "Mark Attendance", automatic_attendance, 600, 500,18)

def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

# View Attendance button (below attendance.png at 980,270)
create_button(window, "View Attendance", view_attendance, 980, 500, 21)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

# Exit button
exit_btn = create_button(window, "EXIT", on_closing, 600, 620)
exit_btn.configure(fg="red", activeforeground="red")

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()