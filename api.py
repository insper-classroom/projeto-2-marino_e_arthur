from flask import Flask, request, jsonify  # Adicionei jsonify
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv  # Corrigido: de django para dotenv

# Carregar as variáveis de ambiente do arquivo .env (mudei de .cred para .env)
load_dotenv('.env')

# Configurações para conexão com o banco de dados usando variáveis de ambiente
config = {
    'host': os.getenv('DB_HOST'),  # Remove 'localhost' como padrão
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),  
    'port': int(os.getenv('DB_PORT', 22795)),
    'ssl_ca': os.getenv('SSL_CA_PATH'),
    'ssl_verify_cert': True  # Importante para Aiven
}

# Função para conectar ao banco de dados
def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print("✅ Conectado ao Aiven!")
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"❌ Erro: {err}")
        return None

app = Flask(__name__)

@app.route('/api/imoveis', methods=['GET'])  # Corrigido: moveis -> imoveis
def get_imoveis():  # Corrigido: get_moves -> get_imoveis
    """Lista todos os imóveis"""
    conn = connect_db()
    
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis")
    results = cursor.fetchall()
    
    if not results:
        return {"erro": "Nenhum imóvel encontrado"}, 404
    
    imoveis = []
    for imovel in results:
        imovel_dict = {
            "id": imovel[0],
            "logradouro": imovel[1],
            "tipo_logradouro": imovel[2],
            "bairro": imovel[3],
            "cidade": imovel[4],
            "cep": imovel[5],
            "tipo": imovel[6],
            "valor": float(imovel[7]) if imovel[7] else None,
            "data_aquisicao": str(imovel[8]) if imovel[8] else None
        }
        imoveis.append(imovel_dict)
    
    cursor.close()
    conn.close()
    
    return jsonify({"imoveis": imoveis}), 200

if __name__ == '__main__':
    app.run(debug=True)