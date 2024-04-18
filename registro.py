import sqlite3
import tkinter as tk
from tkinter import messagebox
import bcrypt
import qrcode
import customtkinter
DATABASE = 'usuarios.db'

def create_table():
    # Función para crear la tabla 'usuarios' en la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            qr_code TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    # Hashear la contraseña utilizando bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def generate_qr_code(username, password):
    # Combina el nombre de usuario y la contraseña en una cadena
    user_data = f"Username: {username}\nPassword: {password}"

    # Genera un código QR con la información del usuario
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(user_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guarda la imagen del código QR
    qr_file_path = f"{username}_qr.png"
    img.save(qr_file_path)
    return qr_file_path

def registrar_usuario():
    # Función para registrar un nuevo usuario
    username = entry_username.get()
    password = entry_password.get()

    # Validación de la entrada de usuario
    if not username or not password:
        messagebox.showerror("Error", "Por favor ingresa un nombre de usuario y una contraseña.")
        return

    # Validación de la longitud de la contraseña
    if len(password) < 8:
        messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres.")
        return

    # Hashear la contraseña antes de almacenarla en la base de datos
    hashed_password = hash_password(password)

    # Generar código QR y obtener la ruta del archivo
    qr_file_path = generate_qr_code(username, password)

    # Conectar a la base de datos y realizar la inserción
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (username, password, qr_code) VALUES (?, ?, ?)', (username, hashed_password, qr_file_path))
    conn.commit()
    conn.close()

    messagebox.showinfo("Registro", "Usuario registrado con éxito.")

# Configuración de la interfaz gráfica para el Registro de Usuario
app_registro= customtkinter.CTk()
app_registro.geometry("400x200")

app_registro.title("Registro de Usuario")

label_username = customtkinter.CTkLabel(app_registro, text="Usuario:")
label_username.pack()

entry_username = customtkinter.CTkEntry(app_registro)
entry_username.pack()

label_password = customtkinter.CTkLabel(app_registro, text="Contraseña:")
label_password.pack()

entry_password = customtkinter.CTkEntry(app_registro, show="*")
entry_password.pack()

button_register = customtkinter.CTkButton(app_registro, text="Registrar Usuario", command=registrar_usuario)
button_register.pack()

# Crea la tabla si no existe
create_table()

# Inicia la interfaz gráfica para el Registro de Usuario
app_registro.mainloop()

if __name__ == "__main__":
    print("Este mensaje se imprimirá solo cuando ejecutes archivo1.py directamente.")
