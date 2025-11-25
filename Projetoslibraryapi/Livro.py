# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    estoque = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Livro {self.titulo}>'

    def serialize(self):
        """Método para retornar o objeto em formato JSON."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'isbn': self.isbn,
            'estoque': self.estoque
        }
