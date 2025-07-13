from mongoengine import Document, StringField, EmailField

class Usuario(Document):
    usuario = StringField(required=True, unique=True)
    password = StringField(required=True)
    nombre_completo = StringField(required=True)
    correo = EmailField(required=True)

    def __str__(self):
        return self.usuario
