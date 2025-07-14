from flask import Flask, render_template, session
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secreto123")  # Opcional pero recomendado

app.config["UPLOAD_FOLDER"] = "./static/images"
app.config["MONGODB_SETTINGS"] = {
    "db": "GestionPeliculas",
    "host": os.environ.get("URI"),
}

# Inicializar la base de datos primero
db = MongoEngine(app)

# Registrar los Blueprints
from routes.usuario import usuario_bp
from routes.genero import genero_bp
from routes.pelicula import pelicula_bp

app.register_blueprint(usuario_bp)
app.register_blueprint(genero_bp)
app.register_blueprint(pelicula_bp)

# Ruta principal
@app.route("/")
def home():
    return render_template("contenido.html")

if __name__ == "__main__":
    print("🚀 Servidor Flask cargado correctamente.")
    app.run(port=5000, host="0.0.0.0", debug=True)
