from datetime import datetime
from . import db

# Tabla de asociación entre Libro y Género (muchos a muchos)
class LibroGenero(db.Model):
    __tablename__ = 'libro_genero'
    
    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    genero_id = db.Column(db.Integer, db.ForeignKey('generos.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    libro = db.relationship('Libro', back_populates='generos')
    genero = db.relationship('Genero', back_populates='libros')
    
    __table_args__ = (
        db.UniqueConstraint('libro_id', 'genero_id', name='uq_libro_genero'),
    )
    
    def __repr__(self):
        return f'<LibroGenero {self.libro_id}-{self.genero_id}>'