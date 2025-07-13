from flask import request, render_template
from models.pelicula import Pelicula
from models.genero import Genero
from utils.login_required import login_required
from app import app,db

@app.route("/pelicula/",methods=["GET"])
@login_required
def listPeliculas():
    try:
        mensaje = None
        peliculas = Pelicula.objects()
    except Exception as error:
        mensaje = str(error)

    return{"mensaje":mensaje, "peliculas":peliculas}

@app.route("/pelicula/",methods=["POST"])
@login_required
def addPelicula():
    try:
        mensaje = None
        estado = False

        if request.method == "POST":
            datos= request.get_json(force=True)
            pelicula = Pelicula(**datos)
            pelicula.save()
            estado = True
            mensaje = "Pelicula agregada correctamente"
        else:
            mensaje = "No permitido"

    except Exception as error:
        mensaje = str(error)

    return{"estado":estado,"mensaje":mensaje}

@app.route("/pelicula/<id>", methods=["PUT"])
@login_required
def updatePelicula(id):
    try:
        mensaje = None
        estado = False

        datos = request.get_json(force=True)
        print(f"✏️ Actualizando película {id} con: {datos}")

        pelicula = Pelicula.objects.get(id=id)
        pelicula.update(**datos)
        estado = True
        mensaje = "Película actualizada correctamente"

    except Exception as error:
        mensaje = str(error)
        print("❌ ERROR:", mensaje)

    return {"estado": estado, "mensaje": mensaje}

@app.route("/pelicula/<id>", methods=["DELETE"])
@login_required
def deletePelicula(id):
    try:
        mensaje = None
        estado = False

        print(f"🗑️ Eliminando película {id}")
        pelicula = Pelicula.objects.get(id=id)
        pelicula.delete()
        estado = True
        mensaje = "Película eliminada correctamente"

    except Exception as error:
        mensaje = str(error)
        print("❌ ERROR:", mensaje)

    return {"estado": estado, "mensaje": mensaje}

@app.route("/pelicula/listar", methods=["GET"])
@login_required
def listar_peliculas():
    peliculas = Pelicula.objects()
    return render_template("listarPeliculas.html", peliculas=peliculas)

@app.route("/pelicula/agregar", methods=["GET"])
@login_required
def vista_agregar_pelicula():
    generos = Genero.objects()
    return render_template("frmAgregarPelicula.html", generos=generos)

