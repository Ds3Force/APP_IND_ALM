import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import qrcode
import cv2
import hashlib
import bcrypt

# Genera una clave de cifrado

# Supongamos que esta es la contraseña que deseas cifrar
contrasena = "mi_contrasena_secreta"

# Cifra la contraseña antes de almacenarla en la base de datos

# Imprime la contraseña descifrada (solo con fines de demostración)



# Función para generar un código QR
def generar_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

# Función para registrar un trabajador en la base de datos
def registrar_trabajador():
    nombre = nombre_entry.get()
    codigo_qr_data = codigo_qr_entry.get()
    contrasena = contrasena_entry.get()

    # Validar que los campos no estén vacíos
    if not nombre or not codigo_qr_data or not contrasena:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    try:
        # Generar un hash seguro para la contraseña
        hashed_contrasena = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()

        # Insertar el trabajador en la base de datos
        conn = sqlite3.connect('registro_de_material.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO trabajadores (nombre, codigo_qr, contrasena) VALUES (?, ?, ?)", (nombre, codigo_qr_data, hashed_contrasena))
        conn.commit()
        conn.close()

        # Generar y mostrar el código QR
        qr_image = generar_qr(codigo_qr_data)
        qr_image.show()

        # Limpiar los campos de entrada
        nombre_entry.delete(0, tk.END)
        codigo_qr_entry.delete(0, tk.END)
        contrasena_entry.delete(0, tk.END)

        messagebox.showinfo("Registro Exitoso", "El trabajador ha sido registrado con éxito.")

    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"Error al registrar al trabajador: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")



# Función para leer códigos QR desde una cámara
def leer_codigo_qr():
    cap = cv2.VideoCapture(0)  # Inicializar la cámara predeterminada

    while True:
        ret, frame = cap.read()

        # Aquí puedes procesar la imagen del frame para detectar y decodificar códigos QR si lo deseas
        
        cv2.imshow('Lector de Códigos QR', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Función para registrar una entrada de material en la base de datos
def registrar_entrada_material():
    material_nombre = material_nombre_entry.get()
    cantidad = cantidad_entry.get()
    cliente = cliente_entry.get()
    codigo_qr_data = codigo_qr_material_entry.get()  # Usar el campo correcto

    if material_nombre and cantidad and cliente and codigo_qr_data:
        # Insertar la entrada de material en la base de datos
        conn = sqlite3.connect('registro_de_material.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entradas_material (material_nombre, cantidad, cliente, codigo_qr) VALUES (?, ?, ?, ?)",
                       (material_nombre, cantidad, cliente, codigo_qr_data))
        conn.commit()
        conn.close()
        
        # Generar y mostrar el código QR
        qr_image = generar_qr(codigo_qr_data)
        qr_image.show()
        
        # Limpiar los campos de entrada
        material_nombre_entry.delete(0, tk.END)
        cantidad_entry.delete(0, tk.END)
        cliente_entry.delete(0, tk.END)
        codigo_qr_material_entry.delete(0, tk.END)
        
        messagebox.showinfo("Registro Exitoso", "La entrada de material ha sido registrada con éxito.")
    else:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")

# Función para verificar las credenciales del trabajador
def verificar_credenciales():
    codigo_qr_data = codigo_qr_entry.get()
    contrasena = contrasena_entry.get()
    
    conn = sqlite3.connect('registro_de_material.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nombre, codigo_qr, contrasena FROM trabajadores WHERE codigo_qr=?", (codigo_qr_data,))
    trabajador = cursor.fetchone()
    
    conn.close()
    
    if trabajador:
        trabajador_id, trabajador_nombre, trabajador_codigo_qr, trabajador_contrasena = trabajador
        
        hashed_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()
        if hashed_contrasena == trabajador_contrasena:
            messagebox.showinfo("Acceso Autorizado", f"Bienvenido, {trabajador_nombre}!")
        else:
            messagebox.showerror("Error de Autenticación", "Contraseña incorrecta. Inténtalo de nuevo.")
    else:
        messagebox.showerror("Error de Autenticación", "No se encontró ningún trabajador con este código QR.")

# Crear una ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Registro y Seguimiento de Trabajadores y Material")

# Configurar el estilo de la interfaz de usuario
style = ttk.Style()
style.configure("TButton", padding=5, font=("Helvetica", 12))

# Crear pestañas en la interfaz
pestañas = ttk.Notebook(ventana)

# Pestaña de Registro de Trabajadores
pestaña_trabajadores = ttk.Frame(pestañas)
pestañas.add(pestaña_trabajadores, text="Registro de Trabajadores")

# Etiquetas y campos de entrada para el registro de trabajadores
nombre_label = tk.Label(pestaña_trabajadores, text="Nombre del Trabajador:")
nombre_label.pack()
nombre_entry = tk.Entry(pestaña_trabajadores)
nombre_entry.pack()

codigo_qr_label = tk.Label(pestaña_trabajadores, text="Código QR:")
codigo_qr_label.pack()
codigo_qr_entry = tk.Entry(pestaña_trabajadores)
codigo_qr_entry.pack()

contrasena_label = tk.Label(pestaña_trabajadores, text="Contraseña:")
contrasena_label.pack()
contrasena_entry = tk.Entry(pestaña_trabajadores, show="*")  # Campo de contraseña
contrasena_entry.pack()

# Botón para registrar trabajador
registrar_trabajador_button = ttk.Button(pestaña_trabajadores, text="Registrar Trabajador", command=registrar_trabajador)
registrar_trabajador_button.pack()


# Pestaña de Registro de Material
pestaña_material = ttk.Frame(pestañas)
pestañas.add(pestaña_material, text="Registro de Material")

# Etiquetas y campos de entrada para el registro de material
material_nombre_label = tk.Label(pestaña_material, text="Nombre del Material:")
material_nombre_label.pack()
material_nombre_entry = tk.Entry(pestaña_material)
material_nombre_entry.pack()

cantidad_label = tk.Label(pestaña_material, text="Cantidad:")
cantidad_label.pack()
cantidad_entry = tk.Entry(pestaña_material)
cantidad_entry.pack()

cliente_label = tk.Label(pestaña_material, text="Cliente:")
cliente_label.pack()
cliente_entry = tk.Entry(pestaña_material)
cliente_entry.pack()

codigo_qr_material_label = tk.Label(pestaña_material, text="Código QR:")
codigo_qr_material_label.pack()
codigo_qr_material_entry = tk.Entry(pestaña_material)
codigo_qr_material_entry.pack()

# Botón para registrar entrada de material
registrar_material_button = ttk.Button(pestaña_material, text="Registrar Entrada de Material", command=registrar_entrada_material)
registrar_material_button.pack()

# Pestaña de Autenticación de Trabajadores
pestaña_autenticacion = ttk.Frame(pestañas)
pestañas.add(pestaña_autenticacion, text="Autenticación de Trabajadores")

# Etiquetas y campos de entrada para la autenticación de trabajadores
codigo_qr_autenticacion_label = tk.Label(pestaña_autenticacion, text="Código QR del Trabajador:")
codigo_qr_autenticacion_label.pack()
codigo_qr_autenticacion_entry = tk.Entry(pestaña_autenticacion)  # Cambiado el nombre a codigo_qr_autenticacion_entry
codigo_qr_autenticacion_entry.pack()

contrasena_label = tk.Label(pestaña_autenticacion, text="Contraseña:")
contrasena_label.pack()
contrasena_entry = tk.Entry(pestaña_autenticacion, show="*")
contrasena_entry.pack()


# Botón para verificar las credenciales
verificar_credenciales_button = ttk.Button(pestaña_autenticacion, text="Verificar Credenciales", command=verificar_credenciales)
verificar_credenciales_button.pack()

# Agregar pestañas a la ventana principal
pestañas.pack(expand=1, fill="both")

# Crear una conexión a la base de datos (o crearla si no existe)
conn = sqlite3.connect('registro_de_material.db')
cursor = conn.cursor()

# Crear la tabla de trabajadores si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS trabajadores (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        codigo_qr TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL
    )
''')

# Crear la tabla de entradas de material si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entradas_material (
        id INTEGER PRIMARY KEY,
        material_nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        cliente TEXT NOT NULL,
        codigo_qr TEXT UNIQUE NOT NULL,
        trabajador_id INTEGER NOT NULL,
        fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (trabajador_id) REFERENCES trabajadores (id)
    )
''')

# Guardar cambios y cerrar la conexión a la base de datos
conn.commit()
conn.close()

# Función para abrir el lector de códigos QR desde la cámara
def abrir_lector_qr():
    leer_codigo_qr()

# Botón para abrir el lector de códigos QR
abrir_lector_qr_button = ttk.Button(pestaña_autenticacion, text="Abrir Lector de Códigos QR", command=abrir_lector_qr)
abrir_lector_qr_button.pack()

# Función principal para ejecutar la aplicación
def main():
    ventana.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    main()
