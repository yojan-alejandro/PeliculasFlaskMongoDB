# from flask import request, render_template
# from models.genero import Genero
# from utils.login_required import login_required
# from app import app,db

# @app.route("/genero/", methods=["GET"])
# @login_required
# def listarGeneros():
#     try :
#         mensaje = None
#         generos= Genero.objects()
    
#     except Exception as error:
#         mensaje = str(error)
    
#     return{"mensaje":mensaje, "generos":generos}

# @app.route("/genero/", methods=["POST"])
# @login_required
# def addGenero():
#     try :
#         print("🟡 Entrando a POST /genero/")
#         mensaje = None
#         estado = False

#         if request.method == "POST":
#             datos= request.get_json(force=True)
#             print("🔵 Datos recibidos:", datos)
#             genero = Genero(**datos)
#             genero.save()
#             estado = True
#             mensaje = "Genero agregado correctamente"
#         else:
#             mensaje = "No permitido"

#     except Exception as error:
#         mensaje = str(error)
#     print("🔴 ERROR:", mensaje)

#     return{"estado":estado,"mensaje":mensaje}

# @app.route("/genero/<id>", methods=["PUT"])
# @login_required
# def actualizar_genero(id):
#     try:
#         mensaje = None
#         estado = False
#         datos = request.get_json(force=True)
#         print(f"✏️ Actualizando género {id} con: {datos}")
        
#         genero = Genero.objects.get(id=id)
#         genero.update(**datos)
#         estado = True
#         mensaje = "Género actualizado correctamente"

#     except Exception as error:
#         mensaje = str(error)
#         print("❌ ERROR:", mensaje)

#     return {"estado": estado, "mensaje": mensaje}

# @app.route("/genero/<id>", methods=["DELETE"])
# @login_required
# def eliminar_genero(id):
#     try:
#         mensaje = None
#         estado = False
#         print(f"🗑️ Eliminando género {id}")
        
#         genero = Genero.objects.get(id=id)
#         genero.delete()
#         estado = True
#         mensaje = "Género eliminado correctamente"

#     except Exception as error:
#         mensaje = str(error)
#         print("❌ ERROR:", mensaje)

#     return {"estado": estado, "mensaje": mensaje}

# @app.route("/genero/listar", methods=["GET"])
# @login_required
# def vista_listar_generos():
#     try:
#         generos = Genero.objects()
#         return render_template("listarGeneros.html", generos=generos)
#     except Exception as e:
#         return f"Error: {str(e)}"
    
# @app.route("/genero/agregar", methods=["GET"])
# @login_required
# def vista_agregar_genero():
#     return render_template("frmAgregarGenero.html")

# routes/genero.py
from flask import request, render_template, Blueprint, url_for, redirect
from models.genero import Genero
# Importa login_required de Flask-Login para asegurar la compatibilidad
from flask_login import login_required

# Crea una instancia de Blueprint para las rutas de género
genero_bp = Blueprint('genero_bp', __name__)

@genero_bp.route("/genero/", methods=["GET"])
@login_required
def listarGeneros():
    try:
        mensaje = None
        generos = Genero.objects()
        # Flask espera un JSON si la respuesta es un diccionario.
        # Si esto es para una API, está bien. Si es para renderizar una plantilla,
        # necesitarías una ruta separada que use render_template.
        return {"mensaje": mensaje, "generos": [g.to_json() for g in generos]} # Convertir a JSON si es una API
    except Exception as error:
        mensaje = str(error)
        print(f"❌ ERROR al listar géneros: {mensaje}")
        return {"mensaje": mensaje, "generos": []}, 500 # Devolver un código de error HTTP

@genero_bp.route("/genero/", methods=["POST"])
@login_required
def addGenero():
    try:
        print("🟡 Entrando a POST /genero/")
        mensaje = None
        estado = False

        if request.method == "POST":
            # Si esperas JSON, get_json(force=True) está bien, pero considera request.is_json
            datos = request.get_json(force=True)
            print("🔵 Datos recibidos:", datos)
            genero = Genero(**datos)
            genero.save()
            estado = True
            mensaje = "Genero agregado correctamente"
        else:
            mensaje = "Método no permitido" # Esto realmente no se ejecutará con methods=["POST"]

    except Exception as error:
        mensaje = str(error)
        print(f"🔴 ERROR al agregar género: {mensaje}")
        estado = False # Asegúrate de que el estado sea False en caso de error

    return {"estado": estado, "mensaje": mensaje}

@genero_bp.route("/genero/<id>", methods=["PUT"])
@login_required
def actualizar_genero(id):
    try:
        mensaje = None
        estado = False
        datos = request.get_json(force=True)
        print(f"✏️ Actualizando género {id} con: {datos}")
        
        genero = Genero.objects.get(id=id)
        genero.update(**datos)
        estado = True
        mensaje = "Género actualizado correctamente"

    except Exception as error:
        mensaje = str(error)
        print(f"❌ ERROR al actualizar género: {mensaje}")

    return {"estado": estado, "mensaje": mensaje}

@genero_bp.route("/genero/<id>", methods=["DELETE"])
@login_required
def eliminar_genero(id):
    try:
        mensaje = None
        estado = False
        print(f"🗑️ Eliminando género {id}")
        
        genero = Genero.objects.get(id=id)
        genero.delete()
        estado = True
        mensaje = "Género eliminado correctamente"

    except Exception as error:
        mensaje = str(error)
        print(f"❌ ERROR al eliminar género: {mensaje}")

    return {"estado": estado, "mensaje": mensaje}

@genero_bp.route("/genero/listar", methods=["GET"])
@login_required
def vista_listar_generos():
    try:
        generos = Genero.objects()
        return render_template("listarGeneros.html", generos=generos)
    except Exception as e:
        print(f"❌ Error en vista_listar_generos: {str(e)}")
        # Podrías renderizar una plantilla de error o redirigir
        return render_template("error.html", error=str(e)), 500
    
@genero_bp.route("/genero/agregar", methods=["GET"])
@login_required
def vista_agregar_genero():
    return render_template("frmAgregarGenero.html")

