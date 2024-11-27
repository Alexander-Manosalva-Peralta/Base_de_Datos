from werkzeug.utils import secure_filename
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Necesario para usar sesiones

# Simulación de usuarios registrados
users = {}

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Datos simulados de ejemplo para las conversaciones
conversations = [
    {"id": 1, "name": "Usuario 1", "last_message": "Hola, ¿cómo estás?"},
    {"id": 2, "name": "Usuario 2", "last_message": "¿Listo para la reunión?"}
]
# Ruta para cargar la página de mensajería
@app.route('/messages')
def messages():
    return render_template('messages.html')

# Ruta para obtener una conversación específica (simulada)
@app.route('/get_conversation/<int:id>', methods=['GET'])
def get_conversation(id):
    # Aquí puedes conectar con una base de datos real y recuperar mensajes
    if id <= len(conversations):
        conversation = {
            "id": id,
            "messages": [
                {"sender": "Usuario 1", "text": "¡Hola! ¿Cómo estás?", "type": "received"},
                {"sender": "Usuario 2", "text": "¡Hola! Estoy bien, ¿y tú?", "type": "sent"}
            ]
        }
        return jsonify(conversation)
    else:
        return jsonify({"error": "Conversación no encontrada"}), 404

@app.route('/crear-publicacion', methods=['POST'])
def crear_publicacion():
    texto = request.form.get('texto')
    archivo = request.files.get('archivo')

    if archivo:
        filename = secure_filename(archivo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        archivo.save(filepath)

        # Aquí deberías guardar la publicación en la base de datos y obtener los datos necesarios
        # Simularemos los datos que se devolverán
        response_data = {
            'success': True,
            'perfilImagen': '/static/images/profile1.jpg',  # Cambia esto por la imagen del usuario
            'nombreUsuario': 'Usuario 1',  # Cambia esto por el nombre de usuario del perfil
            'contenido': f'<img src="{filepath}" alt="Contenido de la publicación">'
        }
        return jsonify(response_data)

    return jsonify({'success': False})
@app.route('/')
def index():
    # Página principal (login)
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']  # Usaremos el teléfono como "contraseña"

        # Verificar si el correo ya existe
        if email in users:
            flash('El correo ya está registrado. Por favor, utiliza otro.')
            return redirect(url_for('register'))

        # Guardar el usuario
        users[email] = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'city': '',  # Datos opcionales inicializados vacíos
            'bio': '',
            'birthdate': ''
        }

        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('index'))

    return render_template('registro.html')


@app.route('/login', methods=['POST'])
def login():
    # Verificar credenciales
    email = request.form['email']
    phone = request.form['phone']  # El número de teléfono actúa como contraseña

    if email in users and users[email]['phone'] == phone:
        # Guardar la sesión del usuario autenticado
        session['email'] = email
        flash('Inicio de sesión exitoso.')
        return redirect(url_for('feed'))

    flash('Correo o número de teléfono incorrecto.')
    return redirect(url_for('index'))


@app.route('/feed')
def feed():
    # Verificar si el usuario está autenticado
    if 'email' not in session:
        flash('Por favor, inicia sesión para acceder al feed.')
        return redirect(url_for('index'))

    # Datos del usuario
    user = users[session['email']]
    return render_template('feed.html', user=user)


@app.route('/profile')
def profile():
    # Verificar si el usuario está autenticado
    if 'email' not in session:
        flash('Por favor, inicia sesión para acceder al perfil.')
        return redirect(url_for('index'))

    # Obtener datos del usuario autenticado
    user = users[session['email']]

    # Pasar el nombre al template
    return render_template('profile.html', username=user['first_name'])


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    # Verificar si el usuario está autenticado
    if 'email' not in session:
        flash('Por favor, inicia sesión para editar tu perfil.')
        return redirect(url_for('index'))

    email = session['email']
    user = users[email]

    if request.method == 'POST':
        # Actualizar los datos del perfil del usuario
        user['first_name'] = request.form['first_name']
        user['last_name'] = request.form['last_name']
        user['city'] = request.form['city']
        user['bio'] = request.form['bio']
        user['birthdate'] = request.form['birthdate']
        flash('Tu perfil ha sido actualizado exitosamente.')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=user)


@app.route('/logout')
def logout():
    # Cerrar sesión
    session.pop('email', None)
    flash('Has cerrado sesión exitosamente.')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('query', '')
    # Aquí, implementa la lógica para buscar en tu base de datos o lista de publicaciones
    results = []  # Esto debería llenarse con los resultados de la búsqueda
    return render_template('search_results.html', query=query, results=results)

@app.route('/explorer')
def explorer():
    return render_template('explorer.html')
@app.route('/reels')
def reels():
    return render_template('reels.html')

if __name__ == '__main__':
    app.run(debug=True)
