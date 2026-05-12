from flask import Flask, render_template, request, redirect, url_for, session
from hola import * # Asegúrate de que aquí esté definida la clase Solicitud

app = Flask(__name__)
app.secret_key = 'techfix_secreto_123' 

# ==========================================
# SIMULACIÓN DE BASE DE DATOS
# ==========================================
# Inicializamos la lista de tickets. 
# Si ya la tienes en hola.py, asegúrate de que no se reinicie cada vez.
ticketsList = [
    # Agregamos un par de tickets de prueba para que veas el diseño funcionando
    Solicitud(id_solicitud=1, categoria="Celular", marca="Apple", detalles="Pantalla rota", problemas=["Pantalla"]),
    Solicitud(id_solicitud=2, categoria="Laptop / PC", marca="Dell", detalles="Mantenimiento preventivo", problemas=["Mantenimiento"])
]

# Les asignamos una fecha y estado manual a los de prueba para que luzcan reales
ticketsList[0].fecha = "07/May/2026"
ticketsList[0].estado = "Pendiente"
ticketsList[1].fecha = "05/May/2026"
ticketsList[1].estado = "En proceso"

# ==========================================
# RUTAS
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['nombre'] = "Jorge"
        session['rol'] = "cliente"
        print("¡Sesión iniciada exitosamente!")
        return redirect(url_for('index'))
    return render_template('inicioSesion.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/crearCuenta')
def crearCuenta():
    return render_template('crearCuenta.html')

@app.route('/cellphone', methods=['GET', 'POST'])
def cellphone():
    if request.method == 'POST':
        marca = request.form.get('marca')
        detalles = request.form.get('detalles')
        reparaciones = request.form.getlist('reparacion')

        nuevo_ticket = Solicitud(
            id_solicitud=len(ticketsList) + 1,
            categoria="Celular",
            marca=marca,
            detalles=detalles,
            problemas=reparaciones
        )
        # Agregamos datos que pide el HTML
        import datetime
        nuevo_ticket.fecha = datetime.date.today().strftime("%d/%b/%Y")
        nuevo_ticket.estado = "Pendiente"
        
        ticketsList.append(nuevo_ticket)
        return redirect(url_for('Tickets')) # Redirigimos directo a ver sus tickets

    return render_template('celulares.html')

@app.route('/laptops_PC', methods=['GET','POST'])
def laptops_PC():
    if request.method == 'POST':
        # Captura de datos...
        mantenimiento = request.form.get('mantenimiento')
        programas = request.form.getlist('programas')
        actualizacion = request.form.get('update')
        detalles = request.form.get('detalles')

        nuevoTicket = Solicitud(
            id_solicitud=len(ticketsList) + 1,
            categoria="Laptop / PC",
            marca="PC Genérica", # Ajusta según tu lógica
            detalles=detalles,
            problemas=programas
        )
        import datetime
        nuevoTicket.fecha = datetime.date.today().strftime("%d/%b/%Y")
        nuevoTicket.estado = "Pendiente"

        ticketsList.append(nuevoTicket)
        return redirect(url_for('Tickets'))

    return render_template('laptopsPC.html')

# ==========================================
# LA RUTA CLAVE: PASAR DATOS AL HTML
# ==========================================
@app.route('/Tickets')
def Tickets():
    # 'mis_tickets' es el nombre que usamos en el {% for ticket in mis_tickets %}
    # ticketsList es nuestra lista de objetos de Python
    return render_template('ticketsUsuarios.html', ticketsList=ticketsList)

if __name__ == '__main__':
    app.run(debug=True)