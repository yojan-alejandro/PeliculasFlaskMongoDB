from flask import Flask,render_template,session
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
from routes.usuario import *
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = "clave_secreta"

app.config["UPLOAD_FOLDER"] = "./static/images"
app.config["MONGODB_SETTINGS"] = {
    "db": "GestionPeliculas",
    "host": os.environ.get("URI"),
}

print("🔍 URI encontrada:", os.environ.get("URI"))

@app.route("/")
def home():
    return render_template("contenido.html")

db = MongoEngine(app)

if __name__ == "__main__":
    print("🚀 Servidor Flask cargado correctamente.")
    from routes.genero import *
    from routes.pelicula import *
    
    app.run(port=5000, host="0.0.0.0", debug=True)
