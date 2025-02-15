import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("estoque.db")
c = conn.cursor()

# Tenta adicionar as colunas se não existirem
try:
    c.execute("ALTER TABLE produtos ADD COLUMN area_m2 REAL;")
except sqlite3.OperationalError:
    print("Coluna 'area_m2' já existe.")

try:
    c.execute("ALTER TABLE produtos ADD COLUMN volume_m3 REAL;")
except sqlite3.OperationalError:
    print("Coluna 'volume_m3' já existe.")

try:
    c.execute("ALTER TABLE produtos ADD COLUMN vlr_m2 REAL;")
except sqlite3.OperationalError:
    print("Coluna 'vlr_m2' já existe.")

try:
    c.execute("ALTER TABLE produtos ADD COLUMN tipo TEXT;")
except sqlite3.OperationalError:
    print("Coluna 'tipo' já existe.")

# Salvar e fechar conexão
conn.commit()
conn.close()

print("Banco corrigido com sucesso!")
