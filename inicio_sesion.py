import sqlite3
import tkinter as tk 
from customtkinter import *
from tkinter import messagebox
import bcrypt
import cv2
import subprocess
from registro import DATABASE
import customtkinter
import sys

def switch_event():
    val=switch.get()
    if val:
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")



def login(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username=?', (username,))
        usuario_encontrado = cursor.fetchone()

    if usuario_encontrado:
        if verificar_password(password, usuario_encontrado[2]):
            mostrar_mensaje_exitoso(f'Bienvenido, {username}!')
            abrir_otro_archivo(username)  # Pasar el nombre de usuario al abrir el otro archivo
            ocultar_mensaje_bienvenida()  # Oculta el mensaje de bienvenida
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

        decoded_objects = cv2.QRCodeDetector().detect(frame)

        if decoded_objects and decoded_objects[0]:
            qr_data = decoded_objects[0][0]
            entry_username.delete(0, tk.END)
            entry_username.insert(0, qr_data)

            user_data = qr_data.split('\n')
            if len(user_data) == 2:
                login(user_data[0].split(': ')[1], user_data[1].split(': ')[1])
            else:
                messagebox.showerror("Error", "Formato de código QR no válido.")

    cap.release()
    cv2.destroyAllWindows()

def abrir_otro_archivo(username):
    ruta_archivo = '/Users/elyangaelgarciarodriguez/Desktop/pytohn/proyecto_oficial/src/carga_lamina.py'
    subprocess.run(["python", ruta_archivo, username])

def exit_program():
    sys.exit()




"""
#interfaz con tkinter

# Pasar el nombre de usuario como argumento

root_login = tk.Tk()
root_login.geometry("500x400")

root_login.title("Inicio de Sesión")

label_username = tk.Label(root_login, text="Usuario:")
label_username.pack()

entry_username = tk.Entry(root_login)
entry_username.pack()

label_password = tk.Label(root_login, text="Contraseña:")
label_password.pack()

entry_password = tk.Entry(root_login, show="*")
entry_password.pack()

button_login = tk.Button(root_login, text="Iniciar Sesión", command=lambda: login(entry_username.get(), entry_password.get()))
button_login.pack()

button_scan_qr = tk.Button(root_login, text="Escanear QR", command=leer_qr_desde_camara)
button_scan_qr.pack()

button_scan_qr = tk.Button(root_login, text="Salir", command=leer_qr_desde_camara)
button_scan_qr.pack()


root_login.mainloop()


"""

app_background= customtkinter.CTk()
app_background.geometry("700x450")
#####################################


app_background.title("Inicio De Sesion")

#####################################
label_username = customtkinter.CTkLabel(app_background, text="Usuario:")
label_username.pack()

entry_username = customtkinter.CTkEntry(app_background, placeholder_text="Usuario")
entry_username.pack()

####################################

label_password = customtkinter.CTkLabel(app_background, text="Contraseña:")
label_password.pack()

entry_password = customtkinter.CTkEntry(app_background, placeholder_text="Contraseña",show="*")
entry_password.pack()
#####################################

button_login = customtkinter.CTkButton(app_background, text="Iniciar Sesión", command=lambda: login(entry_username.get(), entry_password.get()))
button_login.pack(padx=20, pady=20)

button_scan_qr = customtkinter.CTkButton(app_background, text="Escanear QR", command=leer_qr_desde_camara)
button_scan_qr.pack(padx=10,pady=10)


#necesito modificar ete codigo para que salga del programa
button_exit = customtkinter.CTkButton(app_background, text="Salir",fg_color= "red", hover_color="gray",command=exit_program)
button_exit.pack(pady=15)


#####################################



customtkinter.set_appearance_mode("ligth")
customtkinter.set_default_color_theme("dark-blue")


switch=CTkSwitch(app_background,text="Dark Mode", onvalue=1, offvalue=0, command=switch_event)
switch.pack(pady=20)
print(switch.get())
#####################################

app_background.mainloop()
