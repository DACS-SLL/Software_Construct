from datetime import datetime
from . import db

class Autor(db.Model):
    __tablename__ = 'autores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    nacionalidad = db.Column(db.String(50), nullable=True)
    biografia = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Un autor puede tener muchos libros
    libros = db.relationship('Libro', back_populates='autor', lazy='dynamic')
    
    def __repr__(self):
        return f'<Autor {self.nombre} {self.apellido}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'nacionalidad': self.nacionalidad,
            'biografia': self.biografia,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }