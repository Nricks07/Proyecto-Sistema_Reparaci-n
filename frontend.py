from Backend import *
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

sist_admin = Administrador()
sist_stock = Stock()
sist_solicitud = Solicitudes()
sist_usuario = Persona()

def limpiar_pantalla(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

def ventana_login(sist_usuario):
    ventana_login = ctk.CTk()
    ventana_login.title("Login")
    ventana_login.geometry("400x300")

    correo = ctk.CTkLabel(ventana_login, text="Correo")
    correo.pack(pady=10)
    entrada_correo = ctk.CTkEntry(ventana_login, placeholder_text="Correo")
    entrada_correo.pack(pady=10)

    contra = ctk.CTkLabel(ventana_login, text="Contraseña")
    contra.pack(pady=10)
    entrada_contra = ctk.CTkEntry(ventana_login, placeholder_text="Contraseña", show="*")
    entrada_contra.pack(pady=10)

    btn_login = ctk.CTkButton(ventana_login, text="Login", command=lambda: sist_usuario.login(entrada_correo.get(), entrada_contra.get()))
    btn_login.pack(pady=10)
    limpiar_pantalla(ventana_login)
    ventana_login.mainloop()

def ventana_administrador(sist_admin):
    ventana_administrador = ctk.CTk()
    ventana_administrador.title("Administrador")
    ventana_administrador.geometry("400x350")

    btn_gest_soli = ctk.CTkButton(ventana_administrador, text="Solicitudes", command=lambda: ventana_solicitudes(sist_admin))
    btn_gest_soli.pack(pady=10)

    btn_gest_stock = ctk.CTkButton(ventana_administrador, text="Stock", command=lambda: sist_admin.gest_stock())
    btn_gest_stock.pack(pady=10)

    btn_gest_clientes = ctk.CTkButton(ventana_administrador, text="Clientes", command=lambda: sist_admin.gest_clientes())
    btn_gest_clientes.pack(pady=10)

    btn_ingresos = ctk.CTkButton(ventana_administrador, text="Ingresos", command=lambda: sist_admin.ingresos())
    btn_ingresos.pack(pady=10)

    btn_gastos = ctk.CTkButton(ventana_administrador, text="Gastos", command=lambda: sist_admin.gastos())
    btn_gastos.pack(pady=10)

    btn_contactar_distribuidores = ctk.CTkButton(ventana_administrador, text="Distribuidores", command=lambda: sist_admin.contactar_distribuidores())
    btn_contactar_distribuidores.pack(pady=10)

    btn_salir = ctk.CTkButton(ventana_administrador, text="Salir", command=ventana_login)
    limpiar_pantalla(ventana_administrador)
    btn_salir.pack(pady=10)
    
    ventana_administrador.mainloop()

def ventana_solicitudes(sist_admin):
    ventana_soli = ctk.CTkToplevel()
    ventana_soli.title("Solicitudes")
    ventana_soli.geometry("900x400")

    try:
        respuesta = sist_admin.gest_soli()
        datos = respuesta.data
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener solicitudes: {e}")
        return

    # Estilo para la tabla (Treeview)
    style = ttk.Style(ventana_soli)
    style.theme_use("default")
    style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#343638")
    style.map('Treeview', background=[('selected', '#22559b')])
    style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
    style.map("Treeview.Heading", background=[('active', '#3484F0')])

    columnas = ("id", "id_cliente", "tipo", "categoria", "descripcion", "estado", "costo", "fecha_recibo")
    tabla = ttk.Treeview(ventana_soli, columns=columnas, show="headings")
    
    tabla.heading("id", text="ID")
    tabla.heading("id_cliente", text="ID Cliente")
    tabla.heading("tipo", text="Tipo")
    tabla.heading("categoria", text="Categoría")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("estado", text="Estado")
    tabla.heading("costo", text="Costo")
    tabla.heading("fecha_recibo", text="Fecha Recibo")

    tabla.column("id", width=50, anchor="center")
    tabla.column("id_cliente", width=80, anchor="center")
    tabla.column("tipo", width=100)
    tabla.column("categoria", width=100)
    tabla.column("descripcion", width=200)
    tabla.column("estado", width=100, anchor="center")
    tabla.column("costo", width=80, anchor="center")
    tabla.column("fecha_recibo", width=150, anchor="center")

    scrollbar = ttk.Scrollbar(ventana_soli, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)

    crear_controles_estado(ventana_soli)
    btn_salir = ctk.CTkButton(ventana_soli, text="Salir", command=ventana_administrador)
    btn_salir.pack(pady=10)
    limpiar_pantalla(ventana_soli)

    ventana_soli.mainloop()

# Insertar los datos en la tabla
    if datos:
        for fila in datos:
            tabla.insert("", "end", values=(
                fila.get("id", ""),
                fila.get("id_cliente", ""),
                fila.get("tipo", ""),
                fila.get("categoria", ""),
                fila.get("descripcion", ""),
                fila.get("estado", ""),
                fila.get("costo", ""),
                fila.get("created_at", "")
            ))

def crear_controles_estado(ventana):
    # 1. Crear un Frame para los controles
    self.frame_controles = ctk.CTkFrame(ventana)
    self.frame_controles.pack(pady=10, padx=20, fill="x")

    self.label = ctk.CTkLabel(self.frame_controles, text="Cambiar estado del pedido seleccionado:")
    self.label.pack(side="left", padx=10)

    # 2. El Menú de opciones
    self.opciones_estado = ["Cancelar", "Listo"]
    self.menu_estado = ctk.CTkOptionMenu(self.frame_controles, values=self.opciones_estado)
    self.menu_estado.pack(side="left", padx=10)
    self.menu_estado.set("Pendiente") # Valor por defecto

    # 3. Botón para aplicar el cambio
    self.btn_actualizar = ctk.CTkButton(self.frame_controles, 
                                        text="Actualizar Estado", 
                                        command=self.actualizar_estado_logica)
    self.btn_actualizar.pack(side="left", padx=10)

    self.btn_eliminar = ctk.CTkButton(self.frame_controles, 
                                  text="Eliminar Pedido", 
                                  fg_color="#922B21",  # Color rojo para advertir peligro
                                  hover_color="#7B241C",
                                  command=self.eliminar_pedido_logica)
    self.btn_eliminar.pack(side="left", padx=10)

def eliminar_pedido_logica(self):
    seleccion = self.tree.selection()
        
    if not seleccion:
        messagebox.showwarning("Atención", "Debes seleccionar un pedido para eliminar.")
        return

    # ID del item en el Treeview
    item_id = seleccion[0]
    valores = self.tree.item(item_id, "values")
    
    #columna 0 es el ID que necesitas para Supabase
    id_db_pedido = valores[0]

    # Pregunta de seguridad
    confirmacion = messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Estás seguro de que quieres eliminar el pedido con ID {id_db_pedido}?"
    )

    if confirmacion:
        try:
            sist_solicitud.eliminar_soli(id_db_pedido)
            messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el pedido: {e}")

def actualizar_estado_logica(self):
    seleccion = self.tree.selection()
        
    if not seleccion:
        messagebox.showwarning("Atención", "Por favor, selecciona un pedido de la tabla")
        return

    nuevo_estado = self.menu_estado.get()
        
    item_id = seleccion[0]
    valores_actuales = list(self.tree.item(item_id, "values"))
        
    # El índice 6 corresponde a la columna "estado"
    valores_actuales[6] = nuevo_estado
    sist_admin.cambiar_estados_soli(item_id, nuevo_estado)

    # Actualizar visualmente la tabla
    self.tree.item(item_id, values=valores_actuales)
    messagebox.showinfo("Éxito", f"Pedido actualizado a: {nuevo_estado}")

def ventana_stock():
    ventana_stock = ctk.CTk()
    ventana_stock.title("Stock")
    ventana_stock.geometry("400x350")
    btn_salir = ctk.CTkButton(ventana_stock, text="Salir", command=ventana_administrador)
    limpiar_pantalla(ventana_stock)
    btn_salir.pack(pady=10)
    ventana_stock.mainloop()

def ventana_gest_clientes():
    ventana_gest_clientes = ctk.CTk()
    ventana_gest_clientes.title("Gestión de Clientes")
    ventana_gest_clientes.geometry("400x350")
    btn_salir = ctk.CTkButton(ventana_gest_clientes, text="Salir", command=ventana_administrador)
    limpiar_pantalla(ventana_gest_clientes)
    btn_salir.pack(pady=10)
    ventana_gest_clientes.mainloop()

def ventana_ingresos():
    ventana_ingresos = ctk.CTk()
    ventana_ingresos.title("Ingresos")
    ventana_ingresos.geometry("400x350")
    btn_salir = ctk.CTkButton(ventana_ingresos, text="Salir", command=ventana_administrador)
    limpiar_pantalla(ventana_ingresos)
    btn_salir.pack(pady=10)
    ventana_ingresos.mainloop()

def ventana_gastos():
    ventana_gastos = ctk.CTk()
    ventana_gastos.title("Gastos")
    ventana_gastos.geometry("400x350")
    btn_salir = ctk.CTkButton(ventana_gastos, text="Salir", command=ventana_administrador)
    limpiar_pantalla(ventana_gastos)
    btn_salir.pack(pady=10)
    ventana_gastos.mainloop()

def ventana_distribuidores():
    ventana_distribuidores = ctk.CTk()
    ventana_distribuidores.title("Distribuidores")
    ventana_distribuidores.geometry("400x350")
    btn_salir = ctk.CTkButton(ventana_distribuidores, text="Salir", command=ventana_administrador)
    limpiar_pantalla(ventana_distribuidores)
    btn_salir.pack(pady=10)
    ventana_distribuidores.mainloop()