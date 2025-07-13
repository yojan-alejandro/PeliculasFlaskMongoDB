from mongoengine import *
from models.genero import Genero    

class Pelicula(Document):
    codigo = StringField(max_length=10, unique=True, required=True)
    titulo = StringField(max_length=80, required=True)
    descripcion = StringField(required=True)
    duracion = IntField(min_value=30, max_value=200,required=True)
    protagonista = StringField(max_length=50, required=True)
    genero = ReferenceField(Genero)

    def __repr__(self):
        
        return self.titulo