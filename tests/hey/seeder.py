from faker import Faker
import psycopg2  # or import mysql.connector / sqlite3 depending on your DB

# --- CONFIGURATION ---
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "tabd"
DB_USER = "postgres"
DB_PASS = "test"

NUM_ROWS = 10000
# ---------------------

fake = Faker()

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# CREATE TABLE clientes (
#     id SERIAL PRIMARY KEY, -- auto-incrementing ID
#     nome VARCHAR(100) NOT NULL, 
#     email VARCHAR(100) UNIQUE NOT NULL,
#     senha VARCHAR(100) NOT NULL,
#     telefone VARCHAR(15),
#     endereco TEXT
# );

# CREATE TABLE restaurantes (
#     id SERIAL PRIMARY KEY,
#     nome VARCHAR(100) NOT NULL,
#     endereco TEXT NOT NULL,
#     telefone VARCHAR(15)
# );

# CREATE TABLE produtos (
#     id SERIAL PRIMARY KEY,
#     nome VARCHAR(100) NOT NULL,
#     descricao TEXT,
#     preco DECIMAL(10, 2) NOT NULL,
#     restaurante_id INT REFERENCES restaurantes(id)
# );

# CREATE TABLE pedidos (
#     id SERIAL PRIMARY KEY,
#     cliente_id INT REFERENCES clientes(id),
#     restaurante_id INT REFERENCES restaurantes(id),
#     data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     status VARCHAR(50) DEFAULT 'Pendente',
#     total DECIMAL(10, 2) NOT NULL
# );

# CREATE TABLE itens_pedido (
#     id SERIAL PRIMARY KEY,
#     pedido_id INT REFERENCES pedidos(id),
#     produto_id INT REFERENCES produtos(id),
#     quantidade INT NOT NULL,
#     preco_unitario DECIMAL(10, 2) NOT NULL
# );

# CREATE TABLE entregadores (
#     id SERIAL PRIMARY KEY,
#     nome VARCHAR(100) NOT NULL,
#     telefone VARCHAR(15),
#     veiculo VARCHAR(50)
# );

# CREATE TABLE entregas (
#     id SERIAL PRIMARY KEY,
#     pedido_id INT REFERENCES pedidos(id),
#     entregador_id INT REFERENCES entregadores(id),
#     data_entrega TIMESTAMP,
#     status VARCHAR(50) DEFAULT 'A Caminho'
# );
DATA = {
    'clientes': {
        'nome': 'fake.name()',
        'email': 'fake.unique.email()',
        'senha': '"password123"',
        'telefone': 'fake.msisdn()',
        'endereco': 'fake.address()'
    },
    'restaurantes': {
        'nome': 'fake.company()',
        'endereco': 'fake.address()',
        'telefone': 'fake.msisdn()'
    },
    'produtos': {
        'nome': 'fake.word().title()',
        'descricao': 'fake.sentence()',
        'preco': 'round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)',
        'restaurante_id': 'fake.random_int(min=1, max=1000)'
    },
    'pedidos': {
        'cliente_id': 'fake.random_int(min=1, max=10000)',
        'restaurante_id': 'fake.random_int(min=1, max=1000)',
        'data': 'fake.date_time_this_year()',
        'total': 'round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)'
    },
    'itens_pedido': {
        'pedido_id': 'fake.random_int(min=1, max=50000)',
        'produto_id': 'fake.random_int(min=1, max=20000)',
        'quantidade': 'fake.random_int(min=1, max=5)',
        'preco_unitario': 'round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)'
    },
}
ROWS = {
    'clientes': 0000,
    'restaurantes': 000,
    'produtos': 0000,
    'pedidos': 10000,
    'itens_pedido': 30000,
}

for table, fields in DATA.items():
    num_rows = ROWS[table]
    field_names = ', '.join(fields.keys())
    for i in range(num_rows):
        values = ', '.join(f"'{eval(v)}'" for v in fields.values())
        cur.execute(
            f"INSERT INTO {table} ({field_names}) VALUES ({values})"
        )
        if (i + 1) % 1000 == 0:
            conn.commit()
            print(f"{i+1} rows inserted into {table}...")
# TABLE_NAME = "clientes"

# for i in range(NUM_ROWS):
#     name = fake.name()
#     email = fake.unique.email()
#     cur.execute(
#         f"INSERT INTO {TABLE_NAME} (nome, email, senha, telefone, endereco) VALUES (%s, %s, %s, %s, %s)",
#         (name, email, "password123", fake.msisdn(), fake.address())
#     )
#     if (i + 1) % 1000 == 0:
#         conn.commit()
#         print(f"{i+1} rows inserted...")

conn.commit()
cur.close()
conn.close()
print("Done.")