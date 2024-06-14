import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import pandas as pd
import sys
import customtkinter as ctk
import qrcode

BD_LAMINAS = 'laminas.db'
BD_LAMINAS_XLSX = 'laminas.xlsx'

# Obtener el nombre de usuario del argumento de línea de comandos
try:
    username = sys.argv[1]
except IndexError:
    messagebox.showerror("Error", "Nombre de usuario no proporcionado.")
    sys.exit(1)

def generate_qr_code(data, filename):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        img.save(filename)
        return filename
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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
                oc TEXT,
                ubicacion TEXT,
                fecha_registro TEXT,
                usuario_registro TEXT
            )
        ''')

def guardar_datos(material, calibre, cantidad, cliente, proveedor, oc, ubicacion, usuario_registro):
    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with sqlite3.connect(BD_LAMINAS) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO registros (material, calibre, cantidad, cliente, proveedor, oc, ubicacion, fecha_registro, usuario_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (material, calibre, cantidad, cliente, proveedor, oc, ubicacion, fecha_registro, usuario_registro))
        conn.commit()

    # También guardamos en un archivo Excel
    df = pd.read_sql_query("SELECT * FROM registros", conn)
    df.to_excel(BD_LAMINAS_XLSX, sheet_name='Registros', index=False)

def guardar_y_cerrar():
    material = entry_material.get()
    calibre = entry_calibre.get()
    cantidad = entry_cantidad.get()
    cliente = entry_cliente.get()
    proveedor = entry_proveedor.get()
    oc = entry_oc.get()
    ubicacion = entry_ubicacion.get()

    if material and calibre and cantidad and cliente and proveedor and oc and ubicacion:
        guardar_datos(material, calibre, cantidad, cliente, proveedor, oc, ubicacion, username)
        app_laminas_almacenamiento.destroy()
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

def exit_program():
    sys.exit()

crear_tabla()

app_laminas_almacenamiento = ctk.CTk()
app_laminas_almacenamiento.geometry('650x550')
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

label_oc = ctk.CTkLabel(app_laminas_almacenamiento, text="OC:")
label_oc.pack()

entry_oc = ctk.CTkEntry(app_laminas_almacenamiento)
entry_oc.pack()

label_ubicacion = ctk.CTkLabel(app_laminas_almacenamiento, text="Ubicación:")
label_ubicacion.pack()

entry_ubicacion = ctk.CTkEntry(app_laminas_almacenamiento)
entry_ubicacion.pack()

button_guardar = ctk.CTkButton(app_laminas_almacenamiento, text="Guardar", command=guardar_y_cerrar)
button_guardar.pack(padx=20, pady=20)

button_exit = ctk.CTkButton(app_laminas_almacenamiento, text="Salir", fg_color="red", hover_color="gray", command=exit_program)
button_exit.pack(padx=20, pady=20)

app_laminas_almacenamiento.mainloop()
