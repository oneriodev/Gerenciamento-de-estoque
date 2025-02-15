from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/produtos/*": {"origins": "*"}})  # Altere conforme necessário

def init_db():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            descricao TEXT,
            largura REAL,
            profundidade REAL,
            altura REAL,
            area_m2 REAL,
            volume_m3 REAL,
            vlr_m2 REAL,
            tipo TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('estoque.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Inicializa o banco de dados
init_db()

@app.route('/produtos', methods=['GET'])
def get_produtos():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    
    produtos_list = [dict(produto) for produto in produtos]
    return jsonify(produtos_list)

@app.route('/produtos', methods=['POST'])
def add_produto():
    data = request.json

    if not data.get('nome') or not isinstance(data['quantidade'], int) or data['quantidade'] <= 0:
        return jsonify({'error': 'Dados inválidos'}), 400
    
    preco = float(data.get('preco', 0))
    largura = float(data.get('largura', 0))
    profundidade = float(data.get('profundidade', 0))
    altura = float(data.get('altura', 0))
    area_m2 = largura * profundidade
    volume_m3 = largura * profundidade * altura
    vlr_m2 = float(data.get('vlr_m2', 0))
    tipo = data.get('tipo', '')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO produtos (nome, quantidade, preco, descricao, largura, profundidade, altura, area_m2, volume_m3, vlr_m2, tipo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['nome'], data['quantidade'], preco, data.get('descricao', ''), largura, profundidade, altura, area_m2, volume_m3, vlr_m2, tipo))
    conn.commit()
    id_produto = c.lastrowid
    conn.close()
    
    return jsonify({'id': id_produto, 'message': 'Produto adicionado com sucesso'}), 201

@app.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    data = request.json

    if not data.get('nome') or not isinstance(data['quantidade'], int) or data['quantidade'] <= 0:
        return jsonify({'error': 'Dados inválidos'}), 400

    preco = float(data.get('preco', 0))
    largura = float(data.get('largura', 0))
    profundidade = float(data.get('profundidade', 0))
    altura = float(data.get('altura', 0))
    area_m2 = largura * profundidade
    volume_m3 = largura * profundidade * altura
    vlr_m2 = float(data.get('vlr_m2', 0))
    tipo = data.get('tipo', '')

    conn = get_db_connection()
    c = conn.cursor()
    
    # Verifica se o produto existe antes de atualizar
    produto_existente = conn.execute('SELECT id FROM produtos WHERE id=?', (id,)).fetchone()
    if not produto_existente:
        conn.close()
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    c.execute('''
        UPDATE produtos
        SET nome=?, quantidade=?, preco=?, descricao=?, largura=?, profundidade=?, altura=?, area_m2=?, volume_m3=?, vlr_m2=?, tipo=?
        WHERE id=?
    ''', (data['nome'], data['quantidade'], preco, data.get('descricao', ''), largura, profundidade, altura, area_m2, volume_m3, vlr_m2, tipo, id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Produto atualizado com sucesso'})

@app.route('/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    conn = get_db_connection()
    c = conn.cursor()

    # Verifica se o produto existe antes de excluir
    produto_existente = conn.execute('SELECT id FROM produtos WHERE id=?', (id,)).fetchone()
    if not produto_existente:
        conn.close()
        return jsonify({'error': 'Produto não encontrado'}), 404

    c.execute('DELETE FROM produtos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Produto excluído com sucesso'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
