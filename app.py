# from flask import Flask,render_template,session
# from flask_mongoengine import MongoEngine
# from dotenv import load_dotenv
# from routes.usuario import *
# import os

# load_dotenv()

# app = Flask(__name__)

# app.secret_key = "clave_secreta"

# app.config["UPLOAD_FOLDER"] = "./static/images"
# app.config["MONGODB_SETTINGS"] = {
#     "db": "GestionPeliculas",
#     "host": os.environ.get("URI"),
# }

# @app.route("/")
# def home():
#     return render_template("contenido.html")

# db = MongoEngine(app)

# if __name__ == "__main__":
#     print("🚀 Servidor Flask cargado correctamente.")
#     from routes.genero import *
#     from routes.pelicula import *
    
#     app.run(port=5000, host="0.0.0.0", debug=True)

# app.py
import os
from flask import Flask, render_template, session
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user
from dotenv import load_dotenv

# Importa los Blueprints que has definido en tus archivos de rutas
from routes.usuario import usuario_bp
from routes.genero import genero_bp
from routes.pelicula import pelicula_bp

# Carga las variables de entorno del archivo .env
load_dotenv()

# --- Configuración de la aplicación Flask ---
app = Flask(__name__)

# Configura la clave secreta desde las variables de entorno
# ¡IMPORTANTE! Asegúrate de establecer una SECRET_KEY segura en tus variables de entorno de Render
app.secret_key = os.environ.get("SECRET_KEY", "una_clave_secreta_muy_segura_por_defecto_NO_USAR_EN_PRODUCCION")

# Configuración para la carga de archivos (si la usas)
app.config["UPLOAD_FOLDER"] = "./static/images"

# Configuración de MongoDB usando la URI de las variables de entorno
app.config["MONGODB_SETTINGS"] = {
    "db": "GestionPeliculas",
    "host": os.environ.get("MONGO_URI"), # Asegúrate de que esta variable exista en Render
}

# Inicializa la base de datos con la aplicación Flask
db = MongoEngine(app)

# --- Configuración de Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
# Define la vista a la que se redirigirá si un usuario no está autenticado
login_manager.login_view = 'usuario_bp.login_form'

# Importa el modelo Usuario después de inicializar 'db' para evitar problemas
from models.usuario import Usuario

# Función user_loader para Flask-Login
# Carga un usuario dado su ID
@login_manager.user_loader
def load_user(user_id):
    # Busca el usuario por su ID en MongoDB
    return Usuario.objects(id=user_id).first()

# --- Rutas globales (si las hay, como la página de inicio) ---
@app.route("/")
def home():
    # Puedes pasar la sesión o el usuario actual a la plantilla si es necesario
    return render_template("contenido.html", current_user=current_user)

# --- Registro de Blueprints ---
# Registra cada Blueprint con la instancia de la aplicación
# Puedes añadir un url_prefix si quieres que todas las rutas de un blueprint
# empiecen con un prefijo específico (ej. /usuarios, /generos, /peliculas)
app.register_blueprint(usuario_bp)
app.register_blueprint(genero_bp) # Asumiendo que genero_bp está definido en routes/genero.py
app.register_blueprint(pelicula_bp) # Asumiendo que pelicula_bp está definido en routes/pelicula.py

# --- Punto de entrada para desarrollo local (no usado por Gunicorn en Render) ---
if __name__ == "__main__":
    print("🚀 Servidor Flask cargado correctamente (Modo Desarrollo).")
    # Gunicorn se encargará de ejecutar la aplicación en Render
    # No necesitas importar las rutas aquí, ya se registran los blueprints arriba.
    port = int(os.environ.get('PORT', 5000)) # Render usará su propia variable PORT
    app.run(host="0.0.0.0", port=port, debug=True)
