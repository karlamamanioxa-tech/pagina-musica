import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = "database/landing_page.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

    # 1. Obtener la configuración general
    configuracion = conn.execute(
        "SELECT * FROM configuracion_sitio LIMIT 1"
    ).fetchone()

    # 2. Obtener los datos del HERO
    hero = conn.execute("SELECT * FROM hero LIMIT 1").fetchone()

    # 3. Obtener las estadísticas
    estadisticas = conn.execute("SELECT * FROM estadisticas ORDER BY orden").fetchall()

    # 4. Obtener los CURSOS y sus CARACTERÍSTICAS
    cursos = conn.execute("SELECT * FROM cursos WHERE estado = 1 ORDER BY orden").fetchall()
    cursos_con_caracts = []
    for curso in cursos:
        caracteristicas = conn.execute(
            "SELECT caracteristica FROM curso_caracteristicas WHERE curso_id = ? ORDER BY orden",
            (curso['id'],)
        ).fetchall()
        # Convertir la lista de filas en una lista simple de strings
        lista_caracts = [c['caracteristica'] for c in caracteristicas]
        cursos_con_caracts.append({
            'id': curso['id'],
            'titulo': curso['titulo'],
            'descripcion': curso['descripcion'],
            'imagen': curso['imagen'],
            'caracteristicas': lista_caracts
        })

    # 5. Obtener los datos de la sección NOSOTROS
    nosotros = conn.execute("SELECT * FROM nosotros LIMIT 1").fetchone()

    # 6. Obtener los VALORES (tags)
    valores = conn.execute("SELECT * FROM valores ORDER BY orden").fetchall()

    conn.close()

    # Pasar todo al template
    return render_template('index.html',
                           configuracion=configuracion,
                           hero=hero,
                           estadisticas=estadisticas,
                           cursos=cursos_con_caracts,
                           nosotros=nosotros,
                           valores=valores)

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')
    
    conn = get_db_connection()
    # Usamos 'mensajes_contacto' que es el nombre en tu DB
    conn.execute("INSERT INTO mensajes_contacto (nombre, email, mensaje) VALUES (?, ?, ?)",
                 (nombre, email, mensaje))
    conn.commit()
    conn.close()
    
    # Redirigir a la vista de la tabla
    return redirect(url_for('ver_mensajes'))

@app.route('/mensajes')
def ver_mensajes():
    conn = get_db_connection()
    # 'fecha_envio' es el nombre que aparece en tu captura de DBeaver
    mensajes = conn.execute("SELECT id, nombre, email, mensaje, fecha_envio FROM mensajes_contacto ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('mensajes.html', mensajes=mensajes)


@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM mensajes_contacto WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('ver_mensajes'))

if __name__ == '__main__':
    app.run(debug=True)