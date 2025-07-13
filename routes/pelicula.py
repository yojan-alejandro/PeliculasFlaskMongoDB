# from flask import request, render_template
# from models.pelicula import Pelicula
# from models.genero import Genero
# from utils.login_required import login_required
# from app import app,db

# @app.route("/pelicula/",methods=["GET"])
# @login_required
# def listPeliculas():
#     try:
#         mensaje = None
#         peliculas = Pelicula.objects()
#     except Exception as error:
#         mensaje = str(error)

#     return{"mensaje":mensaje, "peliculas":peliculas}

# @app.route("/pelicula/",methods=["POST"])
# @login_required
# def addPelicula():
#     try:
#         mensaje = None
#         estado = False

#         if request.method == "POST":
#             datos= request.get_json(force=True)
#             pelicula = Pelicula(**datos)
#             pelicula.save()
#             estado = True
#             mensaje = "Pelicula agregada correctamente"
#         else:
#             mensaje = "No permitido"

#     except Exception as error:
#         mensaje = str(error)

#     return{"estado":estado,"mensaje":mensaje}

# @app.route("/pelicula/<id>", methods=["PUT"])
# @login_required
# def updatePelicula(id):
#     try:
#         mensaje = None
#         estado = False

#         datos = request.get_json(force=True)
#         print(f"✏️ Actualizando película {id} con: {datos}")

#         pelicula = Pelicula.objects.get(id=id)
#         pelicula.update(**datos)
#         estado = True
#         mensaje = "Película actualizada correctamente"

#     except Exception as error:
#         mensaje = str(error)
#         print("❌ ERROR:", mensaje)

#     return {"estado": estado, "mensaje": mensaje}

# @app.route("/pelicula/<id>", methods=["DELETE"])
# @login_required
# def deletePelicula(id):
#     try:
#         mensaje = None
#         estado = False

#         print(f"🗑️ Eliminando película {id}")
#         pelicula = Pelicula.objects.get(id=id)
#         pelicula.delete()
#         estado = True
#         mensaje = "Película eliminada correctamente"

#     except Exception as error:
#         mensaje = str(error)
#         print("❌ ERROR:", mensaje)

#     return {"estado": estado, "mensaje": mensaje}

# @app.route("/pelicula/listar", methods=["GET"])
# @login_required
# def listar_peliculas():
#     peliculas = Pelicula.objects()
#     return render_template("listarPeliculas.html", peliculas=peliculas)

# @app.route("/pelicula/agregar", methods=["GET"])
# @login_required
# def vista_agregar_pelicula():
#     generos = Genero.objects()
#     return render_template("frmAgregarPelicula.html", generos=generos)

# routes/pelicula.py
from flask import request, render_template, Blueprint, url_for, redirect
from models.pelicula import Pelicula
from models.genero import Genero
# Importa login_required de Flask-Login
from flask_login import login_required

# Crea una instancia de Blueprint para las rutas de película
pelicula_bp = Blueprint('pelicula_bp', __name__)

@pelicula_bp.route("/pelicula/", methods=["GET"])
@login_required
def listPeliculas():
    try:
        mensaje = None
        peliculas = Pelicula.objects()
        # Convertir a JSON si es una API
        return {"mensaje": mensaje, "peliculas": [p.to_json() for p in peliculas]}
    except Exception as error:
        mensaje = str(error)
        print(f"❌ ERROR al listar películas: {mensaje}")
        return {"mensaje": mensaje, "peliculas": []}, 500

@pelicula_bp.route("/pelicula/", methods=["POST"])
@login_required
def addPelicula():
    try:
        mensaje = None
        estado = False

        if request.method == "POST":
            datos = request.get_json(force=True)
            pelicula = Pelicula(**datos)
            pelicula.save()
            estado = True
            mensaje = "Pelicula agregada correctamente"
        else:
            mensaje = "Método no permitido"

    except Exception as error:
        mensaje = str(error)
        print(f"🔴 ERROR al agregar película: {mensaje}")
        estado = False

    return {"estado": estado, "mensaje": mensaje}

@pelicula_bp.route("/pelicula/<id>", methods=["PUT"])
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
        print(f"❌ ERROR al actualizar película: {mensaje}")

    return {"estado": estado, "mensaje": mensaje}

@pelicula_bp.route("/pelicula/<id>", methods=["DELETE"])
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
        print(f"❌ ERROR al eliminar película: {mensaje}")

    return {"estado": estado, "mensaje": mensaje}

@pelicula_bp.route("/pelicula/listar", methods=["GET"])
@login_required
def listar_peliculas():
    try:
        peliculas = Pelicula.objects()
        return render_template("listarPeliculas.html", peliculas=peliculas)
    except Exception as e:
        print(f"❌ Error en listar_peliculas: {str(e)}")
        return render_template("error.html", error=str(e)), 500


@pelicula_bp.route("/pelicula/agregar", methods=["GET"])
@login_required
def vista_agregar_pelicula():
    try:
        generos = Genero.objects()
        return render_template("frmAgregarPelicula.html", generos=generos)
    except Exception as e:
        print(f"❌ Error en vista_agregar_pelicula: {str(e)}")
        return render_template("error.html", error=str(e)), 500

