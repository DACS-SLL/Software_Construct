from datetime import datetime
from . import db

class Libro(db.Model):
    __tablename__ = 'libros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    anio_publicacion = db.Column(db.Integer, nullable=True)
    sinopsis = db.Column(db.Text, nullable=True)
    paginas = db.Column(db.Integer, nullable=True)
    activo = db.Column(db.Boolean, default=True)  # Para borrado lógico
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación muchos a muchos con Autor a través de LibroAutor
    autores = db.relationship('LibroAutor', back_populates='libro', cascade="all, delete-orphan")
    
    # Relación muchos a muchos con Género a través de LibroGenero
    generos = db.relationship('LibroGenero', back_populates='libro', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Libro {self.titulo}>'
    
    def to_dict(self, include_autores=False, include_generos=False):
        result = {
            'id': self.id,
            'titulo': self.titulo,
            'isbn': self.isbn,
            'anio_publicacion': self.anio_publicacion,
            'sinopsis': self.sinopsis,
            'paginas': self.paginas,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        }
        
        if include_autores:
            result['autores'] = [
                {
                    'id': la.autor.id,
                    'nombre': la.autor.nombre,
                    'apellido': la.autor.apellido,
                    'rol': la.rol
                }
                for la in self.autores if la.autor.activo
            ]
            
        if include_generos:
            result['generos'] = [
                {
                    'id': lg.genero.id,
                    'nombre': lg.genero.nombre
                }
                for lg in self.generos if lg.genero.activo
            ]
            
        return result