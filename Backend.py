import random
#Complemente un poco las clases de usuario y de administrador
class Persona:
    def _init_(self, name, apellido, mail, cel):
        self.nombre = name
        self.apellido = apellido
        self.correo = mail
        self.num_cel = cel

class Administrador(Persona):
    def _init_(self, nom, apellido, mail, cel, id_admin, contra):
        super()._init_(nom, apellido, mail, cel)
        self.contraseña = contra
        self.id_admin = id_admin

    def cambiar_estados_soli(self, soli, new_estado):
        soli.estado = new_estado

    def gest_stock():
        pass

    def contactar_distribuidores():
        pass

    def gen_info():
        pass

    def gest_clientes():
        pass

    def gest_soli():
        pass

class Usuario(Persona):
    def _init_(self, nom, apellido, mail, cel, id_usu, usu, contra):
        super()._init_(nom, apellido, mail, cel)
        self.soli_activas = []
        self.id_usuario = id_usu
        self.usuario = usu
        self.contraseña = contra

class Aparato:
    def _init_(self, id_prod, marca, mod):
        self.id_producto = id_prod
        self.marca = marca
        self.modelo = mod

class Celular(Aparato):
    def _init_(self, id_prod, marca, mod, falla_especifica_cel):
        super()._init_(id_prod, marca, mod)
        self.falla_especifica = falla_especifica_cel

# class Celular(Aparato):
#     def _init_(self, id_prod, marca, mod, cam, bat, carcasa, con_car, pantalla):
#         super()._init_(id_prod, marca, mod)
#         self.camara = cam
#         self.bateria = bat
#         self.carcasa = carcasa
#         self.control_carga = con_car
#         self.pantalla = pantalla

class Consola(Aparato):
    def _init_(self, id_prod, marca, mod, falla_especifica_consola):
        super()._init_(id_prod, marca, mod)
        self.falla_especifica = falla_especifica_consola

# class Consola(Aparato):
#     def _init_(self, id_prod, marca, mod, alm, cont):
#         super()._init_(id_prod, marca, mod)
#         self.almacenamiento = alm
#         self.control = cont

class Laptop(Aparato):
    def _init_(self, id_prod, marca, mod, falla_especifica_laptop):
        super()._init_(id_prod, marca, mod)
        self.falla_especifica = falla_especifica_laptop

# class Laptop(Aparato):
#     def _init_(self, id_prod, marca, mod, sis_ope, mem, alm, bat):
#         super()._init_(id_prod, marca, mod)
#         self.sistema_ope = sis_ope
#         self.memoria = mem
#         self.almacenamiento = alm
#         self.bateria = bat

class Solicitudes:
    def _init_(self, id_sol, cat, id_client, tipo, desc):
        tipo = ["Mantenimiento", "Reparacion"]
        cat = ["Celular", "Consola", "Laptop"]
        self.categoria = cat
        self.id_solicitud = id_sol
        self.tipo = tipo
        self.categoria = cat
        self.id_cliente = id_client
        self.descripcion = desc
    
    def calcular_precio():
        pass

class Stock:
    def _init_(self):
        self.stock: dict[str, int] = {}
    
    def agregar_nuevo(self, nombre):
        self.stock = {nombre: 0}

    def agregar_cant(self, nombre, cantidad):
        self.stock[nombre] += cantidad