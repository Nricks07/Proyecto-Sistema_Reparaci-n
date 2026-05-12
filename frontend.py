from Backend import *
import customtkinter as ctk

def cambiar_estad():
    try:
        id_sol = entry_id_solicitud.get()
        estado = entry_estado.get()
        resultado = supabase.table("Solicitudes").update({"estado": estado}).eq("id", id_sol).execute()
        if resultado.data:
            messagebox.showinfo("Estado Cambiado", "Estado cambiado exitosamente")
        else:
            messagebox.showerror("Error", "Error al cambiar estado")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def agregar_precio_solicitud():
    try:
        id_solicitud = entry_id_solicitud.get()
        precio = entry_precio_solicitud.get()
        resultado = supabase.table("Solicitudes").update({"costo": precio}).eq("id", id_solicitud).execute()
        if resultado.data:
            messagebox.showinfo("Precio Agregado", "Precio agregado exitosamente")
        else:
            messagebox.showerror("Error", "Error al agregar precio")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def mostrar_solicitudes_clientes():
    try:
        id_cliente = entry_id_cliente.get()
        resultado = supabase.table("Solicitudes").select("*").eq("id_cliente", id_cliente).execute()
        if resultado.data:
            messagebox.showinfo("Información de la Solicitud", f"ID: {resultado.data[0]['id']}\nCategoria: {resultado.data[0]['categoria']}\nTipo: {resultado.data[0]['tipo']}\nDescripción: {resultado.data[0]['descripcion']}\nEstado: {resultado.data[0]['estado']}\nCosto: {resultado.data[0]['costo']}")
        else:
            messagebox.showerror("Error", "Error al mostrar información de la solicitud")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def registro():
    try:
        nom = entry_nombre_registro.get()
        mail = entry_mail_registro.get()
        cel = entry_cel_registro.get()
        contra = entry_contra_registro.get()
        nuevo_usuario = Usuario(nom, mail, cel, contra)
        resultado = nuevo_usuario.crear_usuario(nom, mail, cel, contra)
        if resultado.data:
            messagebox.showinfo("Registro Exitoso", "Usuario registrado exitosamente")
        else:
            messagebox.showerror("Error", "Error al registrar usuario")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def login():
    try:
        mail = entry_mail_login.get()
        contra = entry_contra_login.get()
        resultado = supabase.table("Clientes").select("*").eq("email", mail).execute()
        if resultado.data:
            if resultado.data[0]["contraseña"] == contra:
                messagebox.showinfo("Login Exitoso", "Login exitoso")
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def crear_solicitud():
    try:
        categoria = entry_categoria_solicitud.get()
        tipo = entry_tipo_solicitud.get()
        descripcion = entry_descripcion_solicitud.get()
        resultado = supabase.table("Solicitudes").insert([{"categoria": categoria, "tipo": tipo, "descripcion": descripcion, "estado": "Pendiente"}]).execute()
        if resultado.data:
            messagebox.showinfo("Solicitud Creada", "Solicitud creada exitosamente")
        else:
            messagebox.showerror("Error", "Error al crear solicitud")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def agregar_stock():
    try:
        nom = entry_nombre_stock.get()
        prec_comp = entry_prec_comp_stock.get()
        prec_venta = entry_prec_venta_stock.get()
        cant_existente = entry_cant_existente_stock.get()
        resultado = supabase.table("Stock").insert([{"nombre": nom, "prec_comp": prec_comp, "prec_venta": prec_venta, "cant_existente": cant_existente}]).execute()
        if resultado.data:
            messagebox.showinfo("Stock Agregado", "Stock agregado exitosamente")
        else:
            messagebox.showerror("Error", "Error al agregar stock")
    except Exception as e:
        messagebox.showerror("Error", str(e))



        