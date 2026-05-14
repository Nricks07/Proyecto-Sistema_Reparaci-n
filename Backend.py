from supabase import create_client

url = "https://wuxeivshsbbarvwazogy.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1eGVpdnNoc2JiYXJ2d2F6b2d5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc5MDUxNTUsImV4cCI6MjA5MzQ4MTE1NX0.AomXNEB35nQ-00PCM1x8gQuPx43qFQ9jfardt0J6TWg" # Reemplaza con la clave de tu imagen_8.png

try:
    supabase = create_client(url, key)
    print("--- Sistema de Gestión de Reparaciones ---")
    print("¡Conexión exitosa al sistema de la tienda!")
except Exception as e:
    print(f"Error al conectar: {e}")

class Persona:
    def __init__(self, name, mail, cel):
        self.nombre = name
        self.correo = mail
        self.num_cel = cel

    def login(correo, contra):
        try:
            usuario = Usuario()
            sesion = supabase.auth.sign_in_with_password({
                "email": correo,
                "password": contra,
            })
            messagebox.showinfo("Login", "Login exitoso")
        except Exception as e:
            messagebox.showerror("Login", f"Error al iniciar sesión: {e}")

class Administrador(Persona):
    def __init__(self, nom, mail, cel, id_admin, contra):
        super().__init__(nom, mail, cel)
        self.contraseña = contra
        self.id_admin = id_admin

    def cambiar_estados_soli(self, id_solicitud, new_estado):
        actualizar = supabase.table("Solicitudes").update({"estado": new_estado}).eq("id", id_solicitud).execute()
        return actualizar

    def gest_stock(self):
        stock = Stock()
        stock.mostrar_stock()

    def contactar_distribuidores(self):
        mostrar = supabase.table("Distribuidor").select("*").execute()
        return mostrar

    def ingresos(self):
        mostrar = supabase.table("Finanzas").select("*").eq("tipo", "Ingreso").execute()
        return mostrar

    def gastos(self):
        mostrar = supabase.table("Finanzas").select("*").eq("tipo", "Gasto").execute()
        return mostrar

    def gest_clientes(self):
        mostrar = supabase.table("Clientes").select("*").execute()
        return mostrar

    def gest_soli(self):
        mostrar = supabase.table("Solicitudes").select("*").execute()
        return mostrar

class Distruidor(Persona):
    def __init__(self, name, mail, cel):
        super().__init__(name, mail, cel)

class Usuario(Persona):
    def __init__(self, id_cliente, nom, mail, cel, contra):
        super().__init__(nom, mail, cel)
        self.id_cliente = id_cliente 
        self.contraseña = contra


    def crear_usuario(self, nom, mail, cel, contra):
        nuevo_usuario = {
            "Nombre" : nom,
            "Email" : mail,
            "Celular" : cel,
            "Contraseña" : contra,
        }
        insertar = supabase.table("Clientes").insert([nuevo_usuario]).execute()

        if insertar.data:
            self.id_cliente = insertar.data[0]['id'] 
            return insertar

    def crear_soli(self, cat, id_client, tipo):
        solicitud = Solicitudes(cat, id_client, tipo)
        return solicitud

    def eliminar_soli(self, id_sol):
        eliminar = supabase.table("Solicitudes").delete().eq("id", id_sol).execute()
        return eliminar

    def ver_mis_solicitudes(self):
        mostrar = supabase.table("Solicitudes").select("*").eq("id_cliente", self.id_cliente).execute()
        return mostrar

class Aparato:
    def __init__(self, id_prod, marca, mod):
        self.id_producto = id_prod
        self.marca = marca
        self.modelo = mod

class Celular(Aparato):
    def __init__(self, id_prod, marca, mod, falla_especifica_cel):
        super().__init__(id_prod, marca, mod)
        self.falla_especifica = falla_especifica_cel

class Consola(Aparato):
    def __init__(self, id_prod, marca, mod, falla_especifica_consola):
        super().__init__(id_prod, marca, mod)
        self.falla_especifica = falla_especifica_consola

class Laptop(Aparato):
    def __init__(self, id_prod, marca, mod, falla_especifica_laptop):
        super().__init__(id_prod, marca, mod)
        self.falla_especifica = falla_especifica_laptop

class Solicitudes:
    def __init__(self, cat, id_client, tipo):
        self.categoria = cat
        self.tipo = tipo
        self.id_cliente = id_client
        
    def agregar_soli(self, descripcion):
        nueva_solicitud = {
            "categoria" : self.categoria,
            "id_cliente" : self.id_cliente,
            "tipo" : self.tipo,
            "estado" : "Pendiente",
            "descripcion" : descripcion,
            "costo": 0.0,
        }

        insertar = supabase.table("Solicitudes").insert([nueva_solicitud]).execute()

        if insertar.data:
            self.id_solicitud = insertar.data[0]['id'] 
            
        return insertar
         
    def agregar_precio(self, costo_sol):
        actualizar = supabase.table("Solicitudes").update({"costo": costo_sol}).eq("id", self.id_solicitud).execute()
        return actualizar

    def mostrar_solicitudes(self):
        mostrar = supabase.table("Solicitudes").select("*").execute()
        return mostrar

    def mostrar_solicitudes_pendientes(self):
        mostrar = supabase.table("Solicitudes").select("*").eq("estado", "Pendiente").execute()
        return mostrar

    def mostrar_solicitudes_en_proceso(self):
        mostrar = supabase.table("Solicitudes").select("*").eq("estado", "En Proceso").execute()
        return mostrar

    def mostrar_solicitudes_finalizadas(self):
        mostrar = supabase.table("Solicitudes").select("*").eq("estado", "Finalizado").execute()
        descripcion = supabase.table("Solicitudes").select("descripcion").eq("estado", "Finalizado").execute()
        monto = supabase.table("Solicitudes").select("costo").eq("estado", "Finalizado").execute()
        mostrar2 = supabase.table("Finanzas").insert([{"descripcion": descripcion, "monto" : monto, "tipo" : "Ingreso"}]).execute()
        return mostrar, mostrar2

    def cambiar_estado_soli(self, id_sol, estado):
        actualizar = supabase.table("Solicitudes").update({"estado": estado}).eq("id", id_sol).execute()
        return actualizar

    def eliminar_soli(self, id_sol):
        eliminar = supabase.table("Solicitudes").delete().eq("id", id_sol).execute()
        return eliminar

class Stock:
    def __init__(self):
        pass

    def agregar_nuevo(self, nombre, prec_comp, prec_venta, cant_existente):
        nuevo_producto ={
            "Nombre" : nombre,
            "Precio-Compra" : prec_comp,
            "Precio-Venta" : prec_venta,
            "Cantidad" : cant_existente,
        }

        insertar = supabase.table("Productos").insert([nuevo_producto]).execute()
        return insertar

    def agregar_cant(self, nombre, cantidad):
        agregar = supabase.table("Productos").update({"Cantidad": cantidad}).eq("Nombre", nombre).execute()
        monto = supabase.table("Productos").select("Precio-Compra").eq("Nombre", nombre).execute()
        monto_final = monto * cantidad
        gasto = supabase.table("Finanzas").insert([{"descripcion" : "Compra de Repuestos", "monto" : monto_final, "tipo" : "Gasto"}]).execute()
        return agregar, gasto

    def mostrar_stock(self):
        mostrar = supabase.table("Productos").select("*").execute()
        return mostrar

    def eliminar_stock(self, nombre):
        eliminar = supabase.table("Productos").delete().eq("Nombre", nombre).execute()
        return eliminar