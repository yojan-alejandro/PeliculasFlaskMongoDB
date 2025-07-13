# from mongoengine import Document, StringField, EmailField

# class Usuario(Document):
#     usuario = StringField(required=True, unique=True)
#     password = StringField(required=True)
#     nombre_completo = StringField(required=True)
#     correo = EmailField(required=True)

#     def __str__(self):
#         return self.usuario

# models/usuario.py
from mongoengine import Document, StringField, EmailField
from flask_login import UserMixin # Importa UserMixin

class Usuario(Document, UserMixin): # Hereda de Document y UserMixin
    usuario = StringField(required=True, unique=True)
    password = StringField(required=True) # ¡IMPORTANTE! Cifrar esta contraseña
    nombre_completo = StringField(required=True)
    correo = EmailField(required=True)

    def __str__(self):
        return self.usuario

    # Método requerido por UserMixin para obtener el ID único del usuario
    def get_id(self):
        return str(self.id)

