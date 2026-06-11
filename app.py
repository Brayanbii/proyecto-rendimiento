import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Llave secreta para habilitar de manera segura las alertas flash en pantalla
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'una-llave-secreta-muy-segura')

# Configurar la conexión a PostgreSQL provista por Render
database_url = os.environ.get('DATABASE_URL')

# Reemplazo requerido debido a que SQLAlchemy exige "postgresql://" en lugar de "postgres://"
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Si no se detecta la variable en Render, usa una base de datos SQLite local para pruebas rápidas
app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para la tabla de usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    comentario = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Crear automáticamente las tablas en la base de datos al arrancar
with app.app_context():
    db.create_all()

# 1. Página de Inicio (Home Page)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Formulario de Registro y Consulta Embebida
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        comentario = request.form.get('comentario')

        # Validación básica de campos requeridos
        if not nombre or not email:
            flash('Por favor, completa los campos obligatorios.', 'error')
            return redirect(url_for('registro'))

        # Evitar errores de correos duplicados en base de datos
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"error": "El correo ya existe"}), 400
            flash('Este correo electrónico ya está registrado.', 'error')
            return redirect(url_for('registro'))

        try:
            nuevo_usuario = Usuario(nombre=nombre, email=email, comentario=comentario)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('¡Usuario registrado con éxito!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ocurrió un error al guardar los datos.', 'error')

        return redirect(url_for('registro'))

    # Para peticiones GET: Consulta todos los registros y los envía a la vista
    usuarios = Usuario.query.all()
    return render_template('registro.html', usuarios=usuarios)

# 3. Endpoint de consulta API (Formato JSON puro)
@app.route('/api/usuarios', methods=['GET'])
def api_usuarios():
    try:
        usuarios = Usuario.query.all()
        data = [
            {"id": u.id, "nombre": u.nombre, "email": u.email, "comentario": u.comentario}
            for u in usuarios
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Error al consultar la base de datos"}), 500

if __name__ == '__main__':
    app.run(debug=True)