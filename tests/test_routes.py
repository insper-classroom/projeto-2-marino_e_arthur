import pytest
from unittest.mock import patch, MagicMock
from api import app  # Importamos a aplicação Flask e a função de conexão

@pytest.fixture
def client():
    """Cria um cliente de teste para a API."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("api.connect_db")  # Substituímos a função que conecta ao banco por um Mock
def test_buscar_imoveis(mock_connect_db, client):
    """Testa a rota /imoveis sem acessar o banco de dados real."""

    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos o retorno do banco de dados
    mock_cursor.fetchall.return_value = [
        (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29'),
        (2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', 260069.89, '2021-11-30')]

    # Substituímos a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn

    # Fazemos a requisição para a API
    response = client.get('/api/imoveis')

    # Verificamos se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificamos se os dados retornados estão corretos
    expected_response = {
        "imoveis": [
        {"id": 1, "logradouro": 'Nicole Common', "tipo_logradouro":'Travessa', "bairro":'Lake Danielle',"cidade":'Judymouth','cep':'85184',"tipo":'casa em condominio', "valor": 488423.52,"data_aquisicao":'2017-07-29'},
        {"id": 2, "logradouro": 'Price Prairie', "tipo_logradouro":'Travessa', "bairro":'Colonton',"cidade":'North Garyville','cep':'93354',"tipo":'casa em condominio', "valor":260069.89,"data_aquisicao":'2021-11-30'},
        ]
    }
    assert response.get_json() == expected_response

    # Verificamos se a consulta SQL foi executada corretamente
    mock_cursor.execute.assert_called_once_with("SELECT * FROM imoveis")
@patch("api.connect_db")
def test_buscar_imovel_id(mock_connect_db, client):
    
    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

    # Simulamos o retorno do banco de dados
    mock_cursor.fetchone.return_value = (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29')

    # Substituímos a função `connect_db` para retornar nosso Mock em vez de uma conexão real
    mock_connect_db.return_value = mock_conn

    # Fazemos a requisição para a API
    response = client.get('/api/imoveis/1')

    # Verificamos se o código de status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificamos se os dados retornados estão corretos
    expected_response = {"id": 1, "logradouro": 'Nicole Common', "tipo_logradouro":'Travessa', "bairro":'Lake Danielle',"cidade":'Judymouth','cep':'85184',"tipo":'casa em condominio', "valor": 488423.52,"data_aquisicao":'2017-07-29'}


    assert response.get_json() == expected_response

    # Verificamos se a consulta SQL foi executada corretamente
    mock_cursor.execute.assert_called_once_with("SELECT * FROM imoveis WHERE id = %s", (1,))
@patch("api.connect_db")
def test_adicionar_novo_imovel(mock_connect_db, client):
    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    # crio um id 
    mock_cursor.lastrowid = 3
    #novo imovel
    novo_imovel = {
        "logradouro": "Rua Street",
        "tipo_logradouro": "Travessa",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "cep": "01234-567",
        "tipo": "apartamento",
        "valor": 350000.00,
        "data_aquisicao": "2024-01-15"
    }
    # Fazemos a requisição para a API
    response = client.post('/api/imoveis',json=novo_imovel)
    # Verificamos se o código de status da resposta é 201(OK)
    assert response.status_code == 201
    #verificar se a resposta da api esta correta 
    expected_response = {
        "mensagem": "Imóvel Criado",
        "id": 3
    }

    # Verificamos se os dados retornados estão corretos
    assert response.get_json() == expected_response


    # Verificar se a query SQL foi executada corretamente
    mock_cursor.execute.assert_called_once()
    # Opcional: verificar os parâmetros da query
    args = mock_cursor.execute.call_args[0]
    assert "INSERT INTO imoveis" in args[0]  # Verifica se é um INSERT
@patch("api.connect_db")
def test_atualizar_imovel_existente(mock_connect_db, client):
    # Criamos um Mock para a conexão e o cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configuramos o Mock para retornar o cursor quando chamarmos conn.cursor()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
 
    # Simulamos o retorno do banco de dados
    mock_cursor.fetchone.return_value = (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29')
    #novo imovel
    imovel_atualizado = {
        "logradouro": "Rua Nova Atualizada",
        "tipo_logradouro": "Travessa",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "cep": "01234-567",
        "tipo": "apartamento",
        "valor": 350000.00,
        "data_aquisicao": "2024-01-15"
    }
    # Fazemos a requisição para a API
    response = client.put('/api/imoveis/1',json=imovel_atualizado)
    # Verificamos se o código de status da resposta é 201(OK)
    assert response.status_code == 200
    #verificar se a resposta da api esta correta 
    # Verificamos a mensagem de sucesso
    expected_response = {
        "mensagem": "Imóvel Atualizado",
    }

    # Verificamos se os dados retornados estão corretos
    assert response.get_json() == expected_response

 # Verificamos se a query SQL de UPDATE foi executada
    mock_cursor.execute.assert_called()
    
    # Pega todas as chamadas do execute
    calls = mock_cursor.execute.call_args_list
    
    # Verifica se a primeira chamada foi SELECT (verificar se existe)
    assert "SELECT * FROM imoveis WHERE id = %s" in calls[0][0][0]
    assert calls[0][0][1] == (1,)
    
    # Verifica se a segunda chamada foi UPDATE
    assert "UPDATE imoveis set" in calls[1][0][0]
    # Verifica se os parâmetros do UPDATE incluem os dados e o ID
    params = calls[1][0][1]
    assert params[0] == "Rua Nova Atualizada"  # logradouro
    assert params[6] == 350000.00  # valor
    assert params[8] == 1  # ID no final




