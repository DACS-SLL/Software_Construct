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
    activo = db.Column(db.Boolean, default=True)  # Para borrado lógico
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación muchos a muchos con Libro a través de LibroAutor
    libros = db.relationship('LibroAutor', back_populates='autor', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Autor {self.nombre} {self.apellido}>'
    
    def to_dict(self, include_libros=False):
        result = {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'nacionalidad': self.nacionalidad,
            'biografia': self.biografia,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        }
        
        if include_libros:
            result['libros'] = [
                {
                    'id': la.libro.id,
                    'titulo': la.libro.titulo,
                    'isbn': la.libro.isbn,
                    'rol': la.rol
                }
                for la in self.libros if la.libro.activo
            ]
            
        return result