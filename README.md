# ⚙️ 🔹 SETUP INICIAL

## Instalar dependências

```bash
pip install flask pytest requests
```

---

## Rodar banco (ex2)

```bash
python ex2_tabelas.py
```

---

## Rodar API

```bash
python app.py
```

---

## Rodar testes

```bash
pytest -v
```

---

# 🧠 FLUXO DA PROVA

```text
1. olhar teste (se tiver)
2. criar rota igual
3. conectar banco
4. fazer SQL
5. return jsonify + status
```

---

# 🔥 PADRÃO DE ROTA (SEMPRE USAR)

```python
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("SQL", valores)

conn.commit()
conn.close()

return jsonify(...), 200
```

---

# 📦 CRUD PADRÃO

## CREATE (POST)

```python
data = request.json

cursor.execute(
    "INSERT INTO tabela (campo1, campo2) VALUES (?, ?)",
    (data["campo1"], data["campo2"])
)
```

---

## READ (GET)

```python
cursor.execute("SELECT * FROM tabela")
dados = cursor.fetchall()
```

---

## READ ID

```python
cursor.execute("SELECT * FROM tabela WHERE id=?", (id,))
dado = cursor.fetchone()
```

---

## UPDATE

```python
cursor.execute(
    "UPDATE tabela SET campo=? WHERE id=?",
    (valor, id)
)
```

---

## DELETE

```python
cursor.execute("DELETE FROM tabela WHERE id=?", (id,))
```

---

# 🌐 VIACEP (FORNECEDOR)

```python
import requests

r = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
dados = r.json()

if "erro" in dados:
    return jsonify({"erro": "CEP inválido"}), 400
```

Campos:

```text
uf → estado
localidade → cidade
bairro
logradouro → rua
```

---

# 🔗 JOIN (ESTOQUE)

```sql
SELECT e.estoque_id, p.nome, e.quantidade
FROM tbl_estoque e
JOIN tbl_produtos p ON e.produto_id = p.produto_id
WHERE e.fornecedor_id = ?
```

---

# 🧪 TESTES (PYTEST)

## client

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
```

---

## teste básico

```python
def test_algo(client):
    response = client.get("/rota")
    assert response.status_code == 200
```

---

## POST teste

```python
response = client.post("/rota", json={
    "campo": "valor"
})
```

---

# ⚠️ STATUS CODES

```text
200 → OK
201 → criado
400 → erro (dados)
404 → não encontrado
```

---

# ⚠️ ERROS QUE REPROVAM

* esquecer commit()
* rota errada
* não usar jsonify
* SQL sem ?
* não usar request.json
* nome errado da tabela

---

# 🧠 DICAS DE PROVA

```text
teste manda → você segue
não inventa rota
faz simples primeiro
se travar → faz básico funcionar
```

---

# 🚀 RESUMO FINAL

```text
rota → banco → SQL → commit → return
```

---
