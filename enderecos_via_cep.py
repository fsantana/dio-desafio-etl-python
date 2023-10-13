import sqlite3
import requests
import re

# Conectando à base de dados SQLite
conn = sqlite3.connect("enderecos.db")

# Criando a nova tabela
conn.execute(
    """
  CREATE TABLE IF NOT EXISTS endereco (
    id INTEGER,
    endereco_completo TEXT,
    logradouro TEXT,
    numero TEXT,
    bairro TEXT,
    cidade TEXT,
    uf TEXT,
    pais TEXT,
    cep TEXT
  )
"""
)

# Inserção de dados de teste
conn.execute(" DELETE FROM endereco ")

enderecos = [
    [1, "Rua das Flores, 123, Centro, Curitiba, PR, Brasil, 80000-000"],
    [2, "Avenida Paulista, 1578, Bela Vista, São Paulo, SP, Brasil, 01310-200"],
    [3, "Praça da Sé, 21, Sé, São Paulo, SP, Brasil, 01001-000"],
    [4, "Rua XV de Novembro, 1299, Centro, Curitiba, PR, Brasil, 80020-310"],
    [5, "Avenida Atlântica, 1702, Copacabana, Rio de Janeiro, RJ, Brasil, 22021-001"],
    [6, "Rua Visconde de Pirajá, 414, Ipanema, Rio de Janeiro, RJ, Brasil, 22410-002"],
    [7, "Avenida Goethe, 200, Moinhos de Vento, Porto Alegre, RS, Brasil, 90430-100"],
    [8, "Rua dos Andradas, 1234, Centro Histórico, Porto Alegre, RS, Brasil, 90020-008"],
    [9, "Rua Augusta, 2529, Cerqueira César São Paulo SP Brasil 01413-000"],
    [10, "Avenida Sete de Setembro 2775 Rebouças Curitiba PR Brasil 80230-010"],
]

sql_insert = 'INSERT INTO endereco (id, endereco_completo) VALUES (?, ?)'

for endereco in enderecos:
    conn.execute(sql_insert, (endereco[0], endereco[1],),)

conn.commit()


def getaddress(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"

    payload = {}
    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Expressão regular para CEPs no formato 00000-000
regex_cep = r"\b(\d{5})-(\d{3})\b"
regex_numero = r"\b\d+\b"

conn.row_factory = dict_factory
cursor = conn.cursor()
# Lendo a base de dados
cursor.execute("SELECT * FROM endereco")
registros = cursor.fetchall()

# Iterando sobre cada linha do DataFrame
for row in registros:
    endereco_completo = row["endereco_completo"]
    match = re.search(regex_cep, endereco_completo)
    cep = match.group(1) + match.group(2)
    endereco = getaddress(cep)

    # extração do número
    endereco_sem_cep = re.sub(r"\b\d{5}-\d{3}\b", "", endereco_completo)
    match = re.search(regex_numero, endereco_sem_cep)
    numero = match.group()

    if "logradouro" in endereco:
        print(f"Endereço: {endereco_completo}")
        print(endereco)
        print(numero)

        sql_update = """ 
                      UPDATE endereco SET 
                      logradouro = ?, numero = ?, bairro = ?,
                      cidade = ?, uf = ?, pais = ?, cep = ? 
                      WHERE id = ? 
                    """
        # Atualizando o endereço na base de dados
        cursor.execute(sql_update, (endereco['logradouro'], numero, endereco['bairro'], 
                                    endereco['localidade'], endereco['uf'], 'BR', 
                                    endereco['cep'], row['id']))

conn.commit()
cursor.execute("SELECT * FROM endereco")
registros = cursor.fetchall()
print(registros)
conn.close()
