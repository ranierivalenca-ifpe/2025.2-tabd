# !/usr/bin/env python3

# Example seeder script

# ----------------------------------------------------------------------------------------------
# This script uses the Seeder class to populate a PostgreSQL database with
# sample data.
# ----------------------------------------------------------------------------------------------

# DO NOT CHANGE THE IMPORTS BELOW
import os
import site

site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from lib import fake, Seeder
# DO NOT CHANGE THE IMPORTS ABOVE

# ----------------------------------------------------------------------------------------------
# CHANGE THE PARAMETERS AND VARIABLES BELOW TO MATCH YOUR DATABASE SCHEMA
# ----------------------------------------------------------------------------------------------

db_host = "localhost"
db_port = 5432
db_name = "tabd"

# ----------------------------------------------------------------------------------------------
# Seeder must be initialized with the correct DB connection info before you can use it on seeding
# ----------------------------------------------------------------------------------------------
seeder = Seeder(db_host, db_port, db_name)

schema = {
    "users": {
        "name": lambda: fake.name(),
        "email": lambda: fake.unique_except(
            seeder.select("email", "email", cache=False)
        ).email(),
        "password": '"password123"',
        "address": lambda: fake.address(),
    },
    "books": {
        "title": lambda: fake.sentence(nb_words=4),
        "author": lambda: fake.name(),
        "published_date": lambda: fake.date(),
        "isbn": lambda: fake.unique_except(
            seeder.select("isbn", "isbn", cache=False)
        ).isbn13(),
        "pages": lambda: fake.random_int(min=50, max=1000),
        "cover": lambda: fake.image_url(),
        "language": lambda: fake.language_code(),
    },
    "book_reviews": {
        "book_id": lambda: fake.from_list(
            [int(id) for id in seeder.select("books", "id")]
        ),
        "user_id": lambda: fake.from_list(
            [int(id) for id in seeder.select("users", "id")]
        ),
        "rating": lambda: fake.random_int(min=1, max=5),
        "comment": lambda: fake.sentence(),
    },
}

rows = {
    "users": 1000,
    "books": 2000,
    "book_reviews": 5000,
}

seeder.seed(schema, rows)

print("Done.")
