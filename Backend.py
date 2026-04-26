import random
class Persona:
    def __init__(self, nom, cel):
        self.nombre = nom
        self.num_cel = cel
#me gusta enrique

#Ya sabiamos

class Administrador(Persona):
    def __init__(self, nom, cel,id_admin, contra):
        super().__init__(nom, cel)
        self.contraseña = contra
        self.id_admin = id_admin

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
    def __init__(self, nom, cel, id_usu, usu, contra):
        super().__init__(nom, cel)
        self.soli_activas = []
        self.id_usuario = id_usu
        self.usuario = usu
        self.contraseña = contra
    
    #Metodo para que cree una solicitud


#quitamos y dejamos para celular y consola
class Aparato:
    def __init__(self, id_prod, marca, mod):
        self.id_producto = id_prod
        self.marca = marca
        self.modelo = mod

class Celular(Aparato):
    def __init__(self, id_prod, marca, mod, cam, bat, carcasa, con_car, pantalla):
        super().__init__(id_prod, marca, mod)
        self.camara = cam
        self.bateria = bat
        self.carcasa = carcasa
        self.control_carga = con_car
        self.pantalla = pantalla

class Consola(Aparato):
    def __init__(self, id_prod, marca, mod, alm, cont):
        super().__init__(id_prod, marca, mod)
        self.almacenamiento = alm
        self.control = cont

class Laptop(Aparato):
    def __init__(self, id_prod, marca, mod, sis_ope, mem, alm, bat):
        super().__init__(id_prod, marca, mod)
        self.sistema_ope = sis_ope
        self.memoria = mem
        self.almacenamiento = alm
        self.bateria = bat

class Solicitudes:
    def __init__(self, id_sol, cat, id_client, tipo, desc):
        tipo = ["Mantenimiento", "Reparacion"]
        cat = ["Celular", "Consola", "Laptop"]
        self.categoria = cat
        self.id_solicitud = id_sol
        self.tipo = tipo
        self.categoria = cat
        self.id_cliente = id_client
        self.descripcion = desc

class Stock:
    def __init__(self):
        self.stock = dict[str, int] = {}
    
    def agregar_nuevo(self, nombre):
        self.stock = {nombre: 0}

    def agregar_cant(self, nombre, cantidad):
        self.stock[nombre] += cantidad

class Provedor:
    def __init__(self):
        pass