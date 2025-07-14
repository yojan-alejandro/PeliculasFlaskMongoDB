from flask import Blueprint,request, render_template
from models.genero import Genero
from utils.login_required import login_required

genero_bp = Blueprint("genero",__name__)

@genero_bp.route("/genero/", methods=["GET"])
@login_required
def listarGeneros():
    try :
        mensaje = None
        generos= Genero.objects()
    
    except Exception as error:
        mensaje = str(error)
    
    return{"mensaje":mensaje, "generos":generos}

@genero_bp.route("/genero/", methods=["POST"])
@login_required
def addGenero():
    try :
        print("🟡 Entrando a POST /genero/")
        mensaje = None
        estado = False

        if request.method == "POST":
            datos= request.get_json(force=True)
            print("🔵 Datos recibidos:", datos)
            genero = Genero(**datos)
            genero.save()
            estado = True
            mensaje = "Genero agregado correctamente"
        else:
            mensaje = "No permitido"

    except Exception as error:
        mensaje = str(error)
    print("🔴 ERROR:", mensaje)

    return{"estado":estado,"mensaje":mensaje}

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
        print("❌ ERROR:", mensaje)

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
        print("❌ ERROR:", mensaje)

    return {"estado": estado, "mensaje": mensaje}

@genero_bp.route("/genero/listar", methods=["GET"])
@login_required
def vista_listar_generos():
    try:
        generos = Genero.objects()
        return render_template("listarGeneros.html", generos=generos)
    except Exception as e:
        return f"Error: {str(e)}"
    
@genero_bp.route("/genero/agregar", methods=["GET"])
@login_required
def vista_agregar_genero():
    return render_template("frmAgregarGenero.html")
