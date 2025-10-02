from faker import Faker
import psycopg2  # or import mysql.connector / sqlite3 depending on your DB

# --- CONFIGURATION ---
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "tabd"
DB_USER = "postgres"
DB_PASS = "test"

TABLE_NAME = "users"
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

for i in range(NUM_ROWS):
    name = fake.name()
    email = fake.unique.email()
    city = fake.city()
    cur.execute(
        f"INSERT INTO {TABLE_NAME} (name, email, city) VALUES (%s, %s, %s)",
        (name, email, city)
    )
    if (i + 1) % 1000 == 0:
        conn.commit()
        print(f"{i+1} rows inserted...")

conn.commit()
cur.close()
conn.close()
print("Done.")