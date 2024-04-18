#!/usr/bin/env python
import sqlite3
import qrcode
import tkinter as tk
from tkinter import messagebox, ttk
import cv2



class EmpleadosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro de Empleados")

        # Inicializar la conexión a la base de datos
        self.conn = sqlite3.connect("empleados.db")
        self.cursor = self.conn.cursor()

        # Crear la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS empleados (
                                id INTEGER PRIMARY KEY,
                                nombre TEXT,
                                apellidos TEXT,
                                id_empleado TEXT,
                                puesto TEXT,
                                codigo_qr TEXT,
                                categoria TEXT
                            )''')
        self.conn.commit()

        # Crear una barra de desplazamiento
        self.scrollbar = tk.Scrollbar(root)
        self.scrollbar.pack(side="right", fill="y")

        # Crear un árbol para mostrar la lista de empleados
        self.tree = ttk.Treeview(root, columns=("Nombre", "Apellidos", "ID Empleado", "Puesto", "Código QR", "Categoría", "Maquina Asignada, "),
                                 show="headings", yscrollcommand=self.scrollbar.set)
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("ID Empleado", text="ID Empleado")
        self.tree.heading("Puesto", text="Puesto")
        self.tree.heading("Código QR", text="Código QR")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.pack()
        self.scrollbar.config(command=self.tree.yview)

        # Labels y Entry para ingresar datos del empleado
        self.nombre_label = tk.Label(root, text="Nombre:")
        self.nombre_label.pack()
        self.nombre_entry = tk.Entry(root)
        self.nombre_entry.pack()

        self.apellidos_label = tk.Label(root, text="Apellidos:")
        self.apellidos_label.pack()
        self.apellidos_entry = tk.Entry(root)
        self.apellidos_entry.pack()

        self.id_empleado_label = tk.Label(root, text="ID del Empleado:")
        self.id_empleado_label.pack()
        self.id_empleado_entry = tk.Entry(root)
        self.id_empleado_entry.pack()

        self.puesto_label = tk.Label(root, text="Puesto:")
        self.puesto_label.pack()
        self.puesto_entry = tk.Entry(root)
        self.puesto_entry.pack()

        self.categoria_label = tk.Label(root, text="Categoría:")
        self.categoria_label.pack()
        self.categoria_entry = ttk.Combobox(root, values=("admin", "usuario"))
        self.categoria_entry.pack()

        # Botones para realizar acciones
        self.agregar_button = tk.Button(root, text="Agregar Empleado", command=self.agregar_empleado)
        self.agregar_button.pack()

        self.editar_button = tk.Button(root, text="Editar Empleado", command=self.editar_empleado)
        self.editar_button.pack()

        self.eliminar_button = tk.Button(root, text="Eliminar Empleado", command=self.eliminar_empleado)
        self.eliminar_button.pack()

        self.listar_button = tk.Button(root, text="Listar Empleados", command=self.listar_empleados)
        self.listar_button.pack()

        self.escanear_button = tk.Button(root, text="Escanear Código QR", command=self.escanear_codigo_qr)
        self.escanear_button.pack()

        # Actualizar la lista de empleados al inicio
        self.actualizar_lista_empleados()

        # Cerrar la conexión de la base de datos cuando se cierra la aplicación
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.conn.close()
        self.root.destroy()

    def agregar_empleado(self):
        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        id_empleado = self.id_empleado_entry.get()
        puesto = self.puesto_entry.get()
        categoria = self.categoria_entry.get()

        if not (nombre and apellidos and id_empleado and puesto and categoria):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        codigo_qr_texto = f"Nombre: {nombre}\nApellidos: {apellidos}\nID del Empleado: {id_empleado}\nPuesto: {puesto}\nCategoría: {categoria}"

        try:
            self.cursor.execute("INSERT INTO empleados (nombre, apellidos, id_empleado, puesto, codigo_qr, categoria) VALUES (?, ?, ?, ?, ?, ?)",
                                (nombre, apellidos, id_empleado, puesto, codigo_qr_texto, categoria))
            self.conn.commit()

            self.generar_codigo_qr(codigo_qr_texto, nombre)

            messagebox.showinfo("Éxito", "Empleado registrado con éxito.")
            self.limpiar_campos()
            self.actualizar_lista_empleados()
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"Error al agregar empleado: {e}")

    def editar_empleado(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un empleado para editar.")
            return

        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        id_empleado = self.id_empleado_entry.get()
        puesto = self.puesto_entry.get()
        categoria = self.categoria_entry.get()

        if not (nombre and apellidos and id_empleado and puesto and categoria):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        codigo_qr_texto = f"Nombre: {nombre}\nApellidos: {apellidos}\nID del Empleado: {id_empleado}\nPuesto: {puesto}\nCategoría: {categoria}"

        try:
            id_seleccionado = selected_item[0]
            self.cursor.execute("UPDATE empleados SET nombre=?, apellidos=?, id_empleado=?, puesto=?, codigo_qr=?, categoria=? WHERE id=?",
                                (nombre, apellidos, id_empleado, puesto, codigo_qr_texto, categoria, id_seleccionado))
            self.conn.commit()

            self.generar_codigo_qr(codigo_qr_texto, nombre)

            messagebox.showinfo("Éxito", "Empleado editado con éxito.")
            self.limpiar_campos()
            self.actualizar_lista_empleados()
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"Error al editar empleado: {e}")

    def eliminar_empleado(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un empleado para eliminar.")
            return

        try:
            id_seleccionado = selected_item[0]
            self.cursor.execute("DELETE FROM empleados WHERE id=?", (id_seleccionado,))
            self.conn.commit()

            messagebox.showinfo("Éxito", "Empleado eliminado con éxito.")
            self.actualizar_listaempleado()
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"Error al eliminar empleado: {e}")

    def listar_empleados(self):
        self.actualizar_lista_empleados()

    def actualizar_lista_empleados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute("SELECT * FROM empleados")
        empleados = self.cursor.fetchall()
        for empleado in empleados:
            self.tree.insert("", "end", values=(empleado[1], empleado[2], empleado[3], empleado[4], empleado[5], empleado[6]))

    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.apellidos_entry.delete(0, tk.END)
        self.id_empleado_entry.delete(0, tk.END)
        self.puesto_entry.delete(0, tk.END)
        self.categoria_entry.set("")

    def generar_codigo_qr(self, texto, nombre_empleado):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(texto)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Guardar el código QR como una imagen PNG
        qr_img.save(f"{nombre_empleado}_qr.png")

    def escanear_codigo_qr(self):
        cap = cv2.VideoCapture(0)

        cv2.namedWindow("Escanear Código QR", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Escanear Código QR", 800, 600)

        while True:
            ret, frame = cap.read()

            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(gray)

            if data:
                self.buscar_empleado(data)

            cv2.imshow("Escanear Código QR", frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def buscar_empleado(self, codigo_qr_texto):
        self.cursor.execute("SELECT * FROM empleados WHERE codigo_qr=?", (codigo_qr_texto,))
        empleado = self.cursor.fetchone()
        if empleado:
            messagebox.showinfo("Empleado Encontrado", f"Nombre: {empleado[1]}\nApellidos: {empleado[2]}\nID del Empleado: {empleado[3]}\nPuesto: {empleado[4]}")
        else:
            messagebox.showerror("Empleado no Encontrado", "No se encontró ningún empleado con este código QR.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmpleadosApp(root)
    root.mainloop()

