#API PARA CREAR STUDENTS

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from decouple import config

# URL DE LA API/PUERTO DE DDONDE QUEREMOS "ESCUCHAR" / USAMOS LA RUTA CREADA PARA CREAR STUDENTS
BASE_URL = config('BASE_URL')

def create_student():
    student_data = {
        "student_names": entry_student_name.get(),#colocar correspondencia de modelo pydantic en string
        "student_username": entry_student_username.get(),
    }

    try:
        response = requests.post(BASE_URL, json=student_data)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx
        if response.status_code == 200:
            messagebox.showinfo("Success", "Student created successfully!")
        else:
            messagebox.showerror("Error", f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Request Error", f"An error occurred: {e}")

#STUDENT UI
root = tk.Tk()
root.title("Student Creation")

#CREATE STUDENT FIELDS
label_student_name = ttk.Label(root, text="Name")
label_student_name.grid(row=1, column=0, padx=10, pady=10)
entry_student_name = ttk.Entry(root)
entry_student_name.grid(row=1, column=1, padx=10, pady=10)

label_student_username = ttk.Label(root, text="Username")
label_student_username.grid(row=2, column=0, padx=10, pady=10)
entry_student_username = ttk.Entry(root)
entry_student_username.grid(row=2, column=1, padx=10, pady=10)

#CREATE STUDENT BUTTON
button_create_student = ttk.Button(root, text="Create Student", command=create_student)
button_create_student.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()