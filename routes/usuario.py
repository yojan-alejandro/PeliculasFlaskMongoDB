# from flask import request, render_template, session, redirect
# from app import app
# from utils.login_required import login_required
# from models.usuario import Usuario

# # Mostrar formulario login
# @app.route("/login", methods=["GET"])
# def login_form():
#     return render_template("login.html")

# @app.route("/usuario/crear_demo", methods=["GET"])
# def crear_usuarios_demo():
#     Usuario(usuario="admin", password="admin123", nombre_completo="Administrador", correo="admin@gmail.com").save()
#     Usuario(usuario="user", password="user123", nombre_completo="Usuario", correo="user@gmail.com").save()
#     return "✅ Usuarios de prueba creados"


# # Procesar login
# @app.route("/login", methods=["POST"])
# def login_post():
#     datos = request.get_json(force=True)
#     print("🔎 Datos recibidos:", datos)
#     user = Usuario.objects(usuario=datos["usuario"], password=datos["password"]).first()
    
#     if user:
#         print("✅ Usuario encontrado:", user)
#         session["usuario"] = user.usuario
#         return {"estado": True, "mensaje": "Login exitoso"}
#     else:
#         print("❌ Usuario no encontrado")
#         return {"estado": False, "mensaje": "Usuario o contraseña incorrectos"}

# # Logout
# @app.route("/logout")
# def logout():
#     session.pop("usuario", None)
#     return redirect("/login")

# # Mostrar formulario registro
# # Mostrar formulario de registro
# @app.route("/registro", methods=["GET"])
# def registro_form():
#     return render_template("registro.html")

# # Procesar el registro
# @app.route("/registro", methods=["POST"])
# def registro_post():
#     datos = request.get_json(force=True)
#     print("📩 Datos recibidos en registro:", datos)

#     if Usuario.objects(usuario=datos["usuario"]).first():
#         print("⚠️ Usuario ya existe")
#         return {"estado": False, "mensaje": "⚠️ El usuario ya existe."}

#     try:
#         nuevo = Usuario(
#             usuario=datos["usuario"],
#             password=datos["password"],
#             nombre_completo=datos["nombre_completo"],
#             correo=datos["correo"]
#         )
#         nuevo.save()
#         print("✅ Usuario guardado en DB")
#         return {"estado": True, "mensaje": "✅ Usuario registrado correctamente."}
#     except Exception as e:
#         print("❌ Error al guardar:", e)
#         return {"estado": False, "mensaje": "❌ Error al registrar."}

# routes/usuario.py
from flask import request, render_template, session, redirect, url_for, Blueprint, flash
# Importa los decoradores de Flask-Login
from flask_login import login_user, logout_user, login_required, current_user
from models.usuario import Usuario

# NO necesitas importar 'app' directamente aquí.
# from app import app # <-- ELIMINAR ESTA LÍNEA

# Crea una instancia de Blueprint para las rutas de usuario
# El primer argumento es el nombre del blueprint, el segundo es el nombre del módulo.
usuario_bp = Blueprint('usuario_bp', __name__)

# Mostrar formulario login
@usuario_bp.route("/login", methods=["GET"])
def login_form():
    # Si el usuario ya está autenticado, redirige a la página de inicio
    if current_user.is_authenticated:
        return redirect(url_for('home')) # 'home' es la ruta global en app.py
    return render_template("login.html")

@usuario_bp.route("/usuario/crear_demo", methods=["GET"])
def crear_usuarios_demo():
    # Considera cifrar las contraseñas incluso para usuarios demo
    Usuario(usuario="admin", password="admin123", nombre_completo="Administrador", correo="admin@gmail.com").save()
    Usuario(usuario="user", password="user123", nombre_completo="Usuario", correo="user@gmail.com").save()
    return "✅ Usuarios de prueba creados"

# Procesar login
@usuario_bp.route("/login", methods=["POST"])
def login_post():
    datos = request.get_json(force=True)
    print("🔎 Datos recibidos:", datos)
    # ¡IMPORTANTE! Aquí deberías verificar la contraseña cifrada, no en texto plano
    user = Usuario.objects(usuario=datos["usuario"], password=datos["password"]).first()
    
    if user:
        print("✅ Usuario encontrado:", user)
        # Usa login_user de Flask-Login para manejar la sesión
        login_user(user)
        # flash("Login exitoso", "success") # Puedes usar flash para mensajes al usuario
        return {"estado": True, "mensaje": "Login exitoso"}
    else:
        print("❌ Usuario no encontrado")
        # flash("Usuario o contraseña incorrectos", "danger")
        return {"estado": False, "mensaje": "Usuario o contraseña incorrectos"}

# Logout
@usuario_bp.route("/logout")
@login_required # Asegura que solo usuarios logueados puedan cerrar sesión
def logout():
    logout_user() # Usa logout_user de Flask-Login
    # Redirige a la ruta de login del blueprint
    return redirect(url_for('usuario_bp.login_form'))

# Mostrar formulario de registro
@usuario_bp.route("/registro", methods=["GET"])
def registro_form():
    return render_template("registro.html")

# Procesar el registro
@usuario_bp.route("/registro", methods=["POST"])
def registro_post():
    datos = request.get_json(force=True)
    print("📩 Datos recibidos en registro:", datos)

    if Usuario.objects(usuario=datos["usuario"]).first():
        print("⚠️ Usuario ya existe")
        return {"estado": False, "mensaje": "⚠️ El usuario ya existe."}

    try:
        nuevo = Usuario(
            usuario=datos["usuario"],
            # ¡IMPORTANTE! Cifra la contraseña antes de guardarla
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

