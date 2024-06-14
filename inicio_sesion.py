import sqlite3
import tkinter as tk
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkSwitch
from tkinter import messagebox
import bcrypt
import cv2
import subprocess
import sys
import customtkinter

DATABASE = 'usuarios.db'

def switch_event():
    val = switch.get()
    customtkinter.set_appearance_mode("dark" if val else "light")

def login(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username=?', (username,))
        usuario_encontrado = cursor.fetchone()

    if usuario_encontrado:
        if verificar_password(password, usuario_encontrado[2]):
            mostrar_mensaje_exitoso(f'Bienvenido, {username}!')
            abrir_otro_archivo(username)
            ocultar_mensaje_bienvenida()
        else:
            messagebox.showerror("Error", 'Contraseña incorrecta. Intenta de nuevo.')
    else:
        messagebox.showerror("Error", 'Usuario no encontrado. Intenta de nuevo.')

def verificar_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

def mostrar_mensaje_exitoso(mensaje):
    messagebox.showinfo("Inicio de Sesión Exitoso", mensaje)

def ocultar_mensaje_bienvenida():
    app_background.withdraw()

def leer_qr_desde_camara():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow("QR Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        qr_data, points, _ = cv2.QRCodeDetector().detectAndDecode(frame)

        if qr_data:
            user_data = qr_data.split('\n')
            if len(user_data) == 2:  # Asegúrate de que el QR tenga el formato correcto
                username, password = user_data
                login(username, password)
                break
            else:
                messagebox.showerror("Error", "Formato de código QR no válido.")
    
    cap.release()
    cv2.destroyAllWindows()

def abrir_otro_archivo(username):
    # Ajusta la ruta del archivo según sea necesario
    ruta_archivo = '/Users/elyangaelgarciarodriguez/Desktop/Yahisa/APP_IND_ALM/nueva_interfaz_carga_de_laminas.py'  # Cambia esto según sea necesario
    app_background.destroy()  # Cerrar la ventana de inicio de sesión antes de ejecutar el nuevo archivo
    subprocess.run([sys.executable, ruta_archivo, username])

def exit_program():
    sys.exit()

app_background = CTk()
app_background.geometry("550x450")
app_background.title("Inicio De Sesion")

label_username = CTkLabel(app_background, text="Usuario:")
label_username.pack()

entry_username = CTkEntry(app_background, placeholder_text="Usuario")
entry_username.pack()

label_password = CTkLabel(app_background, text="Contraseña:")
label_password.pack()

entry_password = CTkEntry(app_background, placeholder_text="Contraseña", show="*")
entry_password.pack()

button_login = CTkButton(app_background, text="Iniciar Sesión", command=lambda: login(entry_username.get(), entry_password.get()))
button_login.pack(padx=20, pady=20)

button_scan_qr = CTkButton(app_background, text="Escanear QR", command=leer_qr_desde_camara)
button_scan_qr.pack(padx=10, pady=10)

button_exit = CTkButton(app_background, text="Salir", fg_color="red", hover_color="gray", command=exit_program)
button_exit.pack(pady=15)

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

switch = CTkSwitch(app_background, text="Dark Mode", onvalue=1, offvalue=0, command=switch_event)
switch.pack(pady=20)

app_background.mainloop()
