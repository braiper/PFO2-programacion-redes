from flask import Flask, request, jsonify, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
# Clave secreta necesaria para manejar sesiones en Flask
app.secret_key = 'clave_secreta_super_segura'

DB_NAME = 'usuarios.db'

# Inicializar la base de datos SQLite
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL
            )
        ''')
        conn.commit()

# 1. Registro de Usuarios
@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    
    # Validamos que lleguen los datos requeridos
    if not datos or 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({"error": "Faltan datos (usuario o contraseña)"}), 400

    usuario = datos['usuario']
    contraseña_plana = datos['contraseña']

    # Hashear la contraseña antes de guardarla
    contraseña_hash = generate_password_hash(contraseña_plana)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)',
                (usuario, contraseña_hash)
            )
            conn.commit()
        return jsonify({"mensaje": f"Usuario '{usuario}' registrado con éxito"}), 201
    
    except sqlite3.IntegrityError:
        return jsonify({"error": "El nombre de usuario ya existe"}), 409

# 2. Inicio de Sesión
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    
    if not datos or 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({"error": "Faltan credenciales"}), 400

    usuario = datos['usuario']
    contraseña_plana = datos['contraseña']

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT contraseña FROM usuarios WHERE usuario = ?', (usuario,))
        fila = cursor.fetchone()

    # Verificar si el usuario existe y si el hash coincide con la contraseña ingresada
    if fila and check_password_hash(fila[0], contraseña_plana):
        session['usuario'] = usuario  # Guardamos al usuario en la sesión para darle acceso
        return jsonify({"mensaje": "Inicio de sesión exitoso. Ya puedes acceder a /tareas"}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# 3. Gestión de Tareas
@app.route('/tareas', methods=['GET'])
def tareas():
    # Verificamos que el usuario haya iniciado sesión
    if 'usuario' not in session:
        return jsonify({"error": "No autorizado. Por favor, inicia sesión en /login primero."}), 401

    usuario_actual = session['usuario']
    
    # HTML de bienvenida
    html_bienvenida = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Gestión de Tareas</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>¡Bienvenido/a, {usuario_actual}!</h1>
            <p>Has iniciado sesión correctamente y tienes acceso al panel de tareas.</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_bienvenida), 200

if __name__ == '__main__':
    init_db()  # Crea la base de datos y la tabla al arrancar si no existen
    app.run(debug=True, port=5000)