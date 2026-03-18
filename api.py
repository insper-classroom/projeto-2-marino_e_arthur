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
def buscar_imoveis():  # Corrigido: get_moves -> get_imoveis
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
@app.route('/api/imoveis/<int:id>', methods=['GET']) 
def buscar_imoveis_id(id):  # Corrigido: get_moves -> get_imoveis
    """Lista todos os imóveis"""
    conn = connect_db()
    
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
    imovel = cursor.fetchone()
    
    if not imovel:
        cursor.close()
        conn.close()
        return {"erro": "Nenhum imóvel encontrado"}, 404
    
   
   
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
     
    
    cursor.close()
    conn.close()
    
    return jsonify(imovel_dict), 200
@app.route('/api/imoveis', methods=['POST'])
def adicionar_novo_imovel():
    
    # 1. Verificar se recebeu JSON
    if not request.is_json:
        return {"erro": "Content-Type deve ser application/json"}, 400
    
    #2 pegar os dados do post
    dados = request.get_json()
    # 3. Validar campos obrigatórios
    campos_obrigatorios = ['logradouro', 'tipo_logradouro', 'bairro', 'cidade', 'cep', 'tipo', 'valor']
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {"erro": f"Campo '{campo}' é obrigatório"}, 400
    # 4. Conectar ao banco de dados
    conn = connect_db()
   
    cursor = conn.cursor()
        
        
      
    cursor.execute("""
            INSERT INTO imoveis 
            (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,(
            dados['logradouro'],
            dados['tipo_logradouro'],
            dados['bairro'],
            dados['cidade'],
            dados['cep'],
            dados['tipo'],
            dados['valor'],
            dados.get('data_aquisicao')  # Opcional
        ))
    # 8. Confirmar transação
    conn.commit()
    # 9. Pegar ID do novo registro
    novo_id = cursor.lastrowid
    cursor.close()
    conn.close()
     

    
    return {
            "mensagem": "Imóvel Criado",
            "id": novo_id
        }, 201
    
@app.route('/api/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    
    # 1. Verificar se recebeu JSON
    if not request.is_json:
        return {"erro": "Content-Type deve ser application/json"}, 400
    
    #2 pegar os dados do post
    dados = request.get_json()
      # 4. Conectar ao banco de dados
    conn = connect_db()
    if not conn:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id,))
    imovel = cursor.fetchone()
    
    if not imovel:
        cursor.close()
        conn.close()
        return {"erro": "Nenhum imóvel encontrado"}, 404
    
   
   
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
    
    # 3. Validar campos existentes
    campos_existentes = ['logradouro', 'tipo_logradouro', 'bairro', 'cidade', 'cep', 'tipo', 'valor','data_aquisicao']
    for campo in dados:
        if campo not in campos_existentes:
            return {"erro": f"Campo '{campo}' é invalido"}, 400
        imovel_dict[campo] = dados[campo] 
  
    
    cursor = conn.cursor()
    #5 atualizar banco de dados 
    
    cursor.execute("""
            UPDATE imoveis set       
            logradouro =%s , tipo_logradouro =%s, bairro=%s, cidade=%s, cep=%s, tipo=%s, valor=%s, data_aquisicao=%s)
            where id =%d
        """,(
            imovel_dict['logradouro'],
            imovel_dict['tipo_logradouro'],
            imovel_dict['bairro'],
            imovel_dict['cidade'],
            imovel_dict['cep'],
            imovel_dict['tipo'],
            imovel_dict['valor'],
            imovel_dict.get('data_aquisicao'),
            id
        ))
    conn.commit()
  
    novo_id = cursor.lastrowid
    cursor.close()
    conn.close()
     

    
    return {
            "mensagem": "Imóvel Atualizado",
        }, 200 

if __name__ == '__main__':
    app.run(debug=True)