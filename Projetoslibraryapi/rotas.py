# app.py
from flask import Flask, request, jsonify
from models import db, Livro
import json
import os

app = Flask(__name__)
# Configuração do banco de dados SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com o aplicativo Flask
db.init_app(app)

# Cria as tabelas no banco de dados se elas não existirem
def create_database():
    with app.app_context():
        db.create_all()
        print("Banco de dados criado!")

# --- Endpoints da API ---

@app.route('/api/livros', methods=['GET'])
def get_livros():
    """Endpoint para listar todos os livros."""
    livros = Livro.query.all()
    # Serializa a lista de objetos para JSON
    return jsonify([livro.serialize() for livro in livros])

@app.route('/api/livros/<int:id>', methods=['GET'])
def get_livro(id):
    """Endpoint para buscar um livro por ID."""
    livro = Livro.query.get_or_404(id)
    return jsonify(livro.serialize())

@app.route('/api/livros', methods=['POST'])
def add_livro():
    """Endpoint para adicionar um novo livro."""
    data = request.get_json()
    if not data or not 'titulo' in data or not 'autor' in data or not 'isbn' in data:
        return jsonify({'erro': 'Dados incompletos'}), 400

    novo_livro = Livro(
        titulo=data['titulo'],
        autor=data['autor'],
        isbn=data['isbn'],
        estoque=data.get('estoque', 1)
    )
    db.session.add(novo_livro)
    db.session.commit()
    return jsonify(novo_livro.serialize()), 201

@app.route('/api/livros/<int:id>', methods=['PUT'])
def update_livro(id):
    """Endpoint para atualizar um livro existente."""
    livro = Livro.query.get_or_404(id)
    data = request.get_json()

    livro.titulo = data.get('titulo', livro.titulo)
    livro.autor = data.get('autor', livro.autor)
    livro.isbn = data.get('isbn', livro.isbn)
    livro.estoque = data.get('estoque', livro.estoque)

    db.session.commit()
    return jsonify(livro.serialize())

@app.route('/api/livros/<int:id>', methods=['DELETE'])
def delete_livro(id):
    """Endpoint para deletar um livro."""
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    return jsonify({'mensagem': 'Livro deletado com sucesso'}), 200

# --- Execução do Aplicativo ---

if __name__ == '__main__':
    # Cria o banco de dados antes de iniciar o servidor
    create_database() 
    # Roda o servidor Flask em modo debug
    app.run(debug=True)
