class Solicitud:
    def __init__(self, id_solicitud, categoria, marca, detalles, problemas):
        self.id_solicitud = id_solicitud
        self.categoria = categoria
        self.marca = marca
        self.detalles = detalles
        self.problemas = problemas
        self.estado = "Pendiente"

# Nuestra base de datos simulada
tickets_guardados = []