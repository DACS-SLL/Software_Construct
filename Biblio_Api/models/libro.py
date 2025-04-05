
from datetime import datetime
from . import db

class Libro(db.Model):
    __tablename__ = 'libros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    anio_publicacion = db.Column(db.Integer, nullable=True)
    genero = db.Column(db.String(50), nullable=True)
    sinopsis = db.Column(db.Text, nullable=True)
    paginas = db.Column(db.Integer, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Un libro pertenece a un autor
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'), nullable=False)
    autor = db.relationship('Autor', back_populates='libros')
    
    def __repr__(self):
        return f'<Libro {self.titulo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'isbn': self.isbn,
            'anio_publicacion': self.anio_publicacion,
            'genero': self.genero,
            'sinopsis': self.sinopsis,
            'paginas': self.paginas,
            'autor_id': self.autor_id,
            'autor_nombre': f"{self.autor.nombre} {self.autor.apellido}" if self.autor else None,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }