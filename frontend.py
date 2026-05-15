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

    # Insertar los datos en la tabla primero
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

    # --- Lógica de botones anidada ---
    def actualizar_estado_logica():
        seleccion = tabla.selection()
            
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, selecciona un pedido de la tabla")
            return

        nuevo_estado = menu_estado.get()
        item_id = seleccion[0]
        valores_actuales = list(tabla.item(item_id, "values"))
        
        # columna 0 es el ID real de la base de datos
        id_db_pedido = valores_actuales[0]
            
        # El índice 5 corresponde a la columna "estado"
        valores_actuales[5] = nuevo_estado
        
        try:
            sist_admin.cambiar_estado_soli(id_db_pedido, nuevo_estado)
            tabla.item(item_id, values=valores_actuales) # Actualizar visualmente la tabla
            messagebox.showinfo("Éxito", f"Pedido actualizado a: {nuevo_estado}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el pedido: {e}")

    def eliminar_pedido_logica():
        seleccion = tabla.selection()
            
        if not seleccion:
            messagebox.showwarning("Atención", "Debes seleccionar un pedido para eliminar.")
            return

        item_id = seleccion[0]
        valores = tabla.item(item_id, "values")
        id_db_pedido = valores[0]

        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar el pedido con ID {id_db_pedido}?"
        )

        if confirmacion:
            try:
                sist_solicitud.eliminar_soli(id_db_pedido)
                tabla.delete(item_id) # Remover de la tabla visualmente
                messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el pedido: {e}")

    # --- Controles Visuales ---
    frame_controles = ctk.CTkFrame(ventana_soli)
    frame_controles.pack(pady=10, padx=20, fill="x")

    label = ctk.CTkLabel(frame_controles, text="Cambiar estado del pedido seleccionado:")
    label.pack(side="left", padx=10)

    # Opciones de estado ampliadas
    opciones_estado = ["En progreso", "Listo", "Cancelado"]
    menu_estado = ctk.CTkOptionMenu(frame_controles, values=opciones_estado)
    menu_estado.pack(side="left", padx=10)
    menu_estado.set("En progreso") # Valor por defecto

    btn_actualizar = ctk.CTkButton(frame_controles, text="Actualizar Estado", command=actualizar_estado_logica)
    btn_actualizar.pack(side="left", padx=10)

    btn_eliminar = ctk.CTkButton(frame_controles, 
                                  text="Eliminar Pedido", 
                                  fg_color="#922B21",
                                  hover_color="#7B241C",
                                  command=eliminar_pedido_logica)
    btn_eliminar.pack(side="left", padx=10)

    btn_salir = ctk.CTkButton(ventana_soli, text="Salir", command=ventana_soli.destroy)
    btn_salir.pack(pady=10)
    limpiar_pantalla(ventana_soli)
    ventana_soli.mainloop()

def ventana_stock(sist_admin):
    ventana_stock = ctk.CTk()
    ventana_stock.title("Stock")
    ventana_stock.geometry("400x350")

    try:
        respuesta = sist_admin.gest_stock()
        datos = respuesta.data
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener stock: {e}")
        return

    # Estilo para la tabla (Treeview)
    style = ttk.Style(ventana_stock)
    style.theme_use("default")
    style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#343638")
    style.map('Treeview', background=[('selected', '#22559b')])
    style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
    style.map("Treeview.Heading", background=[('active', '#3484F0')])

    columnas = ("Id", "Nombre", "Precio-Compra", "Precio-Venta", "Cantidad", "Cantidad-Minima")
    tabla = ttk.Treeview(ventana_stock, columns=columnas, show="headings")
    
    tabla.heading("Id", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Precio-Compra", text="Precio-Compra")
    tabla.heading("Precio-Venta", text="Precio-Venta")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Cant-minima", text="Cantidad Minima")

    tabla.column("Id", width=50, anchor="center")
    tabla.column("Nombre", width=80, anchor="center")
    tabla.column("Precio-Compra", width=100)
    tabla.column("Precio-Venta", width=100)
    tabla.column("Cantidad", width=200)
    tabla.column("Cant-minima", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(ventana_stock, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)
    
    if datos:
        for fila in datos:
            tabla.insert("", "end", values=(
                fila.get("id", ""),
                fila.get("nombre", ""),
                fila.get("precio_compra", ""),
                fila.get("precio_venta", ""),
                fila.get("cantidad", ""),
                fila.get("cant_minima", "")
            ))

    frame_controles = ctk.CTkFrame(ventana_stock)
    frame_controles.pack(pady=10, padx=20, fill="x")

    label = ctk.CTkLabel(frame_controles, text="Cantidad a añadir:")
    label.pack(side="left", padx=10)

    cantidad = ctk.CTkEntry(frame_controles)
    cantidad.pack(side="left", padx=10)

    menu_estado = ctk.CTkOptionMenu(frame_controles, values=cantidad.get())
    menu_estado.pack(side="left", padx=10)

    def cantidad_agregar():
        seleccion = tabla.selection()
            
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, selecciona un producto de la tabla")
            return

        cantidad_agregar = cantidad.get()
        if not cantidad_agregar or not cantidad_agregar.isdigit():
            messagebox.showwarning("Atención", "Por favor, ingresa una cantidad válida")
            
        item_id = seleccion[0]
        valores = tabla.item(item_id, "values")
        id_producto = valores[0]
        cantidad_actual = valores[4]
        
        cantidad_nueva = int(cantidad_actual) + int(cantidad_agregar)
        
        try:
            sist_stock.agregar_cant(id_producto, cantidad_nueva)
            tabla.item(item_id, values=cantidad_nueva) # Actualizar visualmente la tabla
            messagebox.showinfo("Éxito", f"Producto actualizado a: {cantidad_nueva}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")

    def eliminar_producto():
        seleccion = tabla.selection()
            
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, selecciona un producto de la tabla")
            return

        item_id = seleccion[0]
        valores = tabla.item(item_id, "values")
        id_producto = valores[0]
        
        try:
            sist_stock.eliminar_stock(id_producto)
            tabla.delete(item_id) # Remover de la tabla visualmente
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")
        

    btn_actualizar = ctk.CTkButton(frame_controles, text="Agregar Cantidad", command=cantidad_agregar)
    btn_actualizar.pack(side="left", padx=10)

    btn_salir = ctk.CTkButton(ventana_stock, text="Salir", command=ventana_administrador)
    limpiar_pantalla(ventana_stock)
    btn_salir.pack(pady=10)
    ventana_stock.mainloop()
#falta tabla y botones
def ventana_gest_clientes(sist_admin):
    ventana_gest_clientes = ctk.CTk()
    ventana_gest_clientes.title("Gestión de Clientes")
    ventana_gest_clientes.geometry("400x350")
    btn_salir = ctk.CTkButton(ventana_gest_clientes, text="Salir", command=ventana_administrador)
    limpiar_pantalla(ventana_gest_clientes)
    btn_salir.pack(pady=10)
    ventana_gest_clientes.mainloop()
#faltan botones
def ventana_ingresos(sist_admin):
    ventana_ingresos = ctk.CTk()
    ventana_ingresos.title("Ingresos")
    ventana_ingresos.geometry("400x350")

    try:
        respuesta = sist_admin.ingresos()
        datos = respuesta.data
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener ingresos: {e}")
        return

    # Estilo para la tabla (Treeview)
    style = ttk.Style(ventana_ingresos)
    style.theme_use("default")
    style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#343638")
    style.map('Treeview', background=[('selected', '#22559b')])
    style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
    style.map("Treeview.Heading", background=[('active', '#3484F0')])

    columnas = ("Id", "Descripción", "Monto", "Fecha")
    tabla = ttk.Treeview(ventana_ingresos, columns=columnas, show="headings")
    
    tabla.heading("Id", text="ID")
    tabla.heading("Descripción", text="Descripción")
    tabla.heading("Monto", text="Monto")
    tabla.heading("Fecha", text="Fecha")

    tabla.column("Id", width=50, anchor="center")
    tabla.column("Descripción", width=200)
    tabla.column("Monto", width=100, anchor="center")
    tabla.column("Fecha", width=150, anchor="center")

    scrollbar = ttk.Scrollbar(ventana_ingresos, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)
    
    if datos:
        for fila in datos:
            tabla.insert("", "end", values=(
                fila.get("id", ""),
                fila.get("descripcion", ""),
                fila.get("monto", ""),
                fila.get("fecha", "")
            ))



    btn_salir = ctk.CTkButton(ventana_ingresos, text="Salir", command=ventana_administrador)
    limpiar_pantalla(ventana_ingresos)
    btn_salir.pack(pady=10)
    ventana_ingresos.mainloop()
#faltan botones
def ventana_gastos(sist_admin):
    ventana_gastos = ctk.CTk()
    ventana_gastos.title("Gastos")
    ventana_gastos.geometry("400x350")

    try:
        respuesta = sist_admin.gastos()
        datos = respuesta.data
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener gastos: {e}")
        return

    # Estilo para la tabla (Treeview)
    style = ttk.Style(ventana_gastos)
    style.theme_use("default")
    style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#343638")
    style.map('Treeview', background=[('selected', '#22559b')])
    style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
    style.map("Treeview.Heading", background=[('active', '#3484F0')])

    columnas = ("Id", "Descripción", "Monto", "Fecha")
    tabla = ttk.Treeview(ventana_gastos, columns=columnas, show="headings")
    
    tabla.heading("Id", text="ID")
    tabla.heading("Descripción", text="Descripción")
    tabla.heading("Monto", text="Monto")
    tabla.heading("Fecha", text="Fecha")

    tabla.column("Id", width=50, anchor="center")
    tabla.column("Descripción", width=200)
    tabla.column("Monto", width=100, anchor="center")
    tabla.column("Fecha", width=150, anchor="center")

    scrollbar = ttk.Scrollbar(ventana_gastos, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)
    
    if datos:
        for fila in datos:
            tabla.insert("", "end", values=(
                fila.get("id", ""),
                fila.get("descripcion", ""),
                fila.get("monto", ""),
                fila.get("fecha", "")
            ))

    btn_salir = ctk.CTkButton(ventana_gastos, text="Salir", command=ventana_administrador)
    limpiar_pantalla(ventana_gastos)
    btn_salir.pack(pady=10)
    ventana_gastos.mainloop()
#faltan botones
def ventana_distribuidores(sist_admin):
    ventana_distribuidores = ctk.CTk()
    ventana_distribuidores.title("Distribuidores")
    ventana_distribuidores.geometry("400x350")
    
    try:
        respuesta = sist_admin.contactar_distribuidores()
        datos = respuesta.data
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener distribuidores: {e}")
        return

    # Estilo para la tabla (Treeview)
    style = ttk.Style(ventana_distribuidores)
    style.theme_use("default")
    style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#343638")
    style.map('Treeview', background=[('selected', '#22559b')])
    style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
    style.map("Treeview.Heading", background=[('active', '#3484F0')])

    columnas = ("Id", "Nombre", "Email", "Celular")
    tabla = ttk.Treeview(ventana_distribuidores, columns=columnas, show="headings")
    
    tabla.heading("Id", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Email", text="Email")
    tabla.heading("Celular", text="Celular")

    tabla.column("Id", width=50, anchor="center")
    tabla.column("Nombre", width=150)
    tabla.column("Email", width=200)
    tabla.column("Celular", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(ventana_distribuidores, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)
    
    if datos:
        for fila in datos:
            tabla.insert("", "end", values=(
                fila.get("id", ""),
                fila.get("nombre", ""),
                fila.get("email", ""),
                fila.get("celular", "")
            ))


    btn_salir = ctk.CTkButton(ventana_distribuidores, text="Salir", command=ventana_administrador)
    limpiar_pantalla(ventana_distribuidores)
    btn_salir.pack(pady=10)
    ventana_distribuidores.mainloop()