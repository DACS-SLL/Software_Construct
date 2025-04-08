from datetime import datetime
from . import db

# Tabla de asociación entre Libro y Autor (muchos a muchos)
class LibroAutor(db.Model):
    __tablename__ = 'libro_autor'
    
    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'), nullable=False)
    rol = db.Column(db.String(50), nullable=True)  # Por ejemplo: autor principal, co-autor, editor, etc.
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    libro = db.relationship('Libro', back_populates='autores')
    autor = db.relationship('Autor', back_populates='libros')
    
    __table_args__ = (
        db.UniqueConstraint('libro_id', 'autor_id', name='uq_libro_autor'),
    )
    
    def __repr__(self):
        return f'<LibroAutor {self.libro_id}-{self.autor_id}>'