import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import pandas as pd
import sys
import customtkinter as ctk
import os

# Obtener el nombre de usuario del argumento de línea de comandos
try:
    username = sys.argv[1]
except IndexError:
    messagebox.showerror("Error", "Nombre de usuario no proporcionado.")
    sys.exit(1)

BD_LAMINAS = 'laminas.db'
BD_LAMINAS_XLSX = 'laminas.xlsx'

def crear_tabla():
    with sqlite3.connect(BD_LAMINAS) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                material TEXT,
                calibre TEXT,
                cantidad INTEGER,
                cliente TEXT,
                proveedor TEXT,
                fecha_registro TEXT,
                usuario_registro TEXT
            )
        ''')

def guardar_datos(material, calibre, cantidad, cliente, proveedor, usuario_registro):
    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with sqlite3.connect(BD_LAMINAS) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO registros (material, calibre, cantidad, cliente, proveedor, fecha_registro, usuario_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (material, calibre, cantidad, cliente, proveedor, fecha_registro, usuario_registro))
        conn.commit()

    guardar_en_excel(material, calibre, cantidad, cliente, proveedor, fecha_registro)

def guardar_en_excel(material, calibre, cantidad, cliente, proveedor, fecha_registro):
    new_data = pd.DataFrame({
        'Material': [material],
        'Calibre': [calibre],
        'Cantidad': [cantidad],
        'Cliente': [cliente],
        'Proveedor': [proveedor],
        'Fecha de Registro': [fecha_registro],
    })

    if not os.path.isfile(BD_LAMINAS_XLSX):
        with pd.ExcelWriter(BD_LAMINAS_XLSX, engine='xlsxwriter') as writer:
            new_data.to_excel(writer, sheet_name='Registros', index=False)
    else:
        existing_data = pd.read_excel(BD_LAMINAS_XLSX)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        with pd.ExcelWriter(BD_LAMINAS_XLSX, engine='xlsxwriter') as writer:
            updated_data.to_excel(writer, sheet_name='Registros', index=False)

    messagebox.showinfo("Éxito", "Datos guardados en la base de datos y en el archivo Excel.")

def guardar_y_cerrar():
    material = entry_material.get()
    calibre = entry_calibre.get()
    cantidad = entry_cantidad.get()
    cliente = entry_cliente.get()
    proveedor = entry_proveedor.get()

    if material and calibre and cantidad and cliente and proveedor:
        guardar_datos(material, calibre, cantidad, cliente, proveedor, '''username''')
        app_laminas_almacenamiento.destroy()
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

def exit_program():
    sys.exit()

crear_tabla()

app_laminas_almacenamiento = ctk.CTk()
app_laminas_almacenamiento.geometry('650x450')
app_laminas_almacenamiento.title("Formulario de Registro")


label_material = ctk.CTkLabel(app_laminas_almacenamiento, text="Material:")
label_material.pack()

entry_material = ctk.CTkEntry(app_laminas_almacenamiento)
entry_material.pack()

label_calibre = ctk.CTkLabel(app_laminas_almacenamiento, text="Calibre:")
label_calibre.pack()

entry_calibre = ctk.CTkEntry(app_laminas_almacenamiento)
entry_calibre.pack()

label_cantidad = ctk.CTkLabel(app_laminas_almacenamiento, text="Cantidad:")
label_cantidad.pack()

entry_cantidad = ctk.CTkEntry(app_laminas_almacenamiento)
entry_cantidad.pack()

label_cliente = ctk.CTkLabel(app_laminas_almacenamiento, text="Cliente:")
label_cliente.pack()

entry_cliente = ctk.CTkEntry(app_laminas_almacenamiento)
entry_cliente.pack()

label_proveedor = ctk.CTkLabel(app_laminas_almacenamiento, text="Proveedor:")
label_proveedor.pack()

entry_proveedor = ctk.CTkEntry(app_laminas_almacenamiento)
entry_proveedor.pack()

button_guardar = ctk.CTkButton(app_laminas_almacenamiento, text="Guardar", command=guardar_y_cerrar)
button_guardar.pack(padx=20, pady=20)

button_exit = ctk.CTkButton(app_laminas_almacenamiento, text="Salir", fg_color="red", hover_color="gray", command=exit_program)
button_exit.pack(padx=20, pady=20)

app_laminas_almacenamiento.mainloop()
