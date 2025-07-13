from flask import request, render_template, session, redirect
from app import app
from utils.login_required import login_required
from models.usuario import Usuario

# Mostrar formulario login
@app.route("/login", methods=["GET"])
def login_form():
    return render_template("login.html")

@app.route("/usuario/crear_demo", methods=["GET"])
def crear_usuarios_demo():
    Usuario(usuario="admin", password="admin123", nombre_completo="Administrador", correo="admin@gmail.com").save()
    Usuario(usuario="user", password="user123", nombre_completo="Usuario", correo="user@gmail.com").save()
    return "✅ Usuarios de prueba creados"


# Procesar login
@app.route("/login", methods=["POST"])
def login_post():
    datos = request.get_json(force=True)
    print("🔎 Datos recibidos:", datos)
    user = Usuario.objects(usuario=datos["usuario"], password=datos["password"]).first()
    
    if user:
        print("✅ Usuario encontrado:", user)
        session["usuario"] = user.usuario
        return {"estado": True, "mensaje": "Login exitoso"}
    else:
        print("❌ Usuario no encontrado")
        return {"estado": False, "mensaje": "Usuario o contraseña incorrectos"}

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")

# Mostrar formulario registro
# Mostrar formulario de registro
@app.route("/registro", methods=["GET"])
def registro_form():
    return render_template("registro.html")

# Procesar el registro
@app.route("/registro", methods=["POST"])
def registro_post():
    datos = request.get_json(force=True)
    print("📩 Datos recibidos en registro:", datos)

    if Usuario.objects(usuario=datos["usuario"]).first():
        print("⚠️ Usuario ya existe")
        return {"estado": False, "mensaje": "⚠️ El usuario ya existe."}

    try:
        nuevo = Usuario(
            usuario=datos["usuario"],
            password=datos["password"],
            nombre_completo=datos["nombre_completo"],
            correo=datos["correo"]
        )
        nuevo.save()
        print("✅ Usuario guardado en DB")
        return {"estado": True, "mensaje": "✅ Usuario registrado correctamente."}
    except Exception as e:
        print("❌ Error al guardar:", e)
        return {"estado": False, "mensaje": "❌ Error al registrar."}
