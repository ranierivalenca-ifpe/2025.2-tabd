from os import path, getenv
from dotenv import load_dotenv

load_dotenv()

PROJECTS_PATH = path.join(path.abspath(path.dirname(__file__)), "../", "projects")
SCAFFOLD_PATH = path.join(
    path.abspath(path.dirname(__file__)), "../", "scaffold-template"
)

EXPOSED_PORT = 5432
DB_USER = "postgres"
DB_PASS = "root"
