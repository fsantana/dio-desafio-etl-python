from gettext import find
import sqlite3
import requests
import re
from ClassIdealPostcodes import IdealPostcodes 

# Expressão regular para CEPs no formato 00000-000
regex_cep = r"\b(\d{5})-(\d{3})\b"
regex_numero = r"\b\d+\b"

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
    [1, "Rua Visconde de Pirajá, 414, Ipanema, Rio de Janeiro, RJ, Brasil, 22410-002"],
    [2, "Avenida Goethe, 200, Moinhos de Vento, Porto Alegre, RS, Brasil, 90430-100"],
]

sql_insert = 'INSERT INTO endereco (id, endereco_completo) VALUES (?, ?)'

for endereco in enderecos:
    conn.execute(sql_insert, (endereco[0], endereco[1],),)

conn.commit()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn.row_factory = dict_factory
cursor = conn.cursor()
# Lendo a base de dados
cursor.execute("SELECT * FROM endereco")
registros = cursor.fetchall()

# Iterando sobre cada linha do DataFrame
for row in registros:
    endereco_completo = row["endereco_completo"]
    endereco = IdealPostcodes.find(endereco_completo)
    # extração do número
    endereco_sem_cep = re.sub(r"\b\d{5}-\d{3}\b", "", endereco_completo)
    match = re.search(regex_numero, endereco_sem_cep)
    numero = match.group()

    
    if endereco:
        endereco = endereco['result']
        sql_update = """ 
                      UPDATE endereco SET 
                      logradouro = ?, numero = ?, bairro = ?,
                      cidade = ?, uf = ?, pais = ?, cep = ? 
                      WHERE id = ? 
                    """
        # Atualizando o endereço na base de dados
        cursor.execute(sql_update, (endereco['native']['street_name'], numero, endereco['post_town'], 
                                    endereco['native']['order8_name'], endereco['native']['order2_name'], 'BR', 
                                    endereco['postcode'], row['id']))

conn.commit()
cursor.execute("SELECT * FROM endereco")
registros = cursor.fetchall()
print(registros)
conn.close()
