# app.py

from flask import Flask, request, jsonify
from models import db, Livro  # Importa o objeto db e a classe Livro do arquivo models.py
import json
import os

# --- Configuração Inicial do Aplicativo ---
app = Flask(__name__)

# Configuração do banco de dados SQLite local
# O arquivo do banco de dados (biblioteca.db) será criado na raiz do seu projeto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com o aplicativo Flask
db.init_app(app)

# Função auxiliar para criar as tabelas no banco de dados
def create_database():
    """Cria o arquivo do banco de dados e as tabelas se não existirem."""
    with app.app_context():
        db.create_all()
        print("Banco de dados 'biblioteca.db' criado/verificado!")

# --- Endpoints da API (Rotas) ---

@app.route('/api/livros', methods=['GET'])
def get_livros():
    """Endpoint para listar todos os livros."""
    livros = Livro.query.all()
    # Converte a lista de objetos Livro em uma lista de dicionários JSON
    return jsonify([livro.serialize() for livro in livros])

@app.route('/api/livros/<int:id>', methods=['GET'])
def get_livro(id):
    """Endpoint para buscar um livro por ID."""
    # get_or_404 retorna o livro ou um erro 404 Not Found se não existir
    livro = Livro.query.get_or_404(id)
    return jsonify(livro.serialize())

@app.route('/api/livros', methods=['POST'])
def add_livro():
    """Endpoint para adicionar um novo livro."""
    data = request.get_json()

    # Validação básica de entrada
    if not data or not 'titulo' in data or not 'autor' in data or not 'isbn' in data:
        return jsonify({'erro': 'Dados incompletos. Título, autor e ISBN são obrigatórios.'}), 400

    novo_livro = Livro(
        titulo=data['titulo'],
        autor=data['autor'],
        isbn=data['isbn'],
        estoque=data.get('estoque', 1) # Define 1 como padrão se 'estoque' não for fornecido
    )
    db.session.add(novo_livro)
    db.session.commit()
    # Retorna o livro recém-criado e o status code 201 Created
    return jsonify(novo_livro.serialize()), 201

@app.route('/api/livros/<int:id>', methods=['PUT'])
def update_livro(id):
    """Endpoint para atualizar um livro existente."""
    livro = Livro.query.get_or_404(id)
    data = request.get_json()

    # Atualiza apenas os campos que foram fornecidos no corpo da requisição
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
    return jsonify({'mensagem': f'Livro com ID {id} deletado com sucesso'}), 200

# --- Execução do Aplicativo ---

if __name__ == '__main__':
    # Garante que o banco de dados e as tabelas existam antes de rodar o app
    create_database() 
    # Inicia o servidor Flask. O modo debug permite recarregamento automático.
    app.run(debug=True)
