from pathlib import Path
import os
import mysql.connector
from dotenv import load_dotenv, find_dotenv
import pytest

# Cargar variables de entorno
load_dotenv(find_dotenv())

# Nombre de la base de datos de pruebas
TEST_DB = os.getenv("TEST_DB_NAME", "test_yasbel")

# Configurar para usar BD de pruebas
os.environ["DB_NAME"] = TEST_DB

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "2DAW")
DB_PASSWORD = os.getenv("DB_PASSWORD", "2DAW_pass")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

SQL_PATH = Path(__file__).resolve().parent.parent / "docs" / "init_db.sql"


def _execute_sql_without_db(sql_text: str, conn: mysql.connector.MySQLConnection) -> None:
    """Ejecuta SQL sin seleccionar una base de datos."""
    cur = conn.cursor()
    try:
        for stmt in sql_text.split(";"):
            stmt = stmt.strip()
            if not stmt:
                continue
            cur.execute(stmt)
        conn.commit()
    finally:
        cur.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Crea y puebla la BD de pruebas antes de la sesión y la elimina al final."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        charset="utf8mb4",
    )
    try:
        sql = SQL_PATH.read_text(encoding="utf-8")
        # Reemplazar el nombre de la DB por la de pruebas
        sql = sql.replace("yasbel", TEST_DB)
        _execute_sql_without_db(sql, conn)

        yield
    finally:
        # Limpiar: eliminar la base de datos de prueba
        cur = conn.cursor()
        try:
            cur.execute(f"DROP DATABASE IF EXISTS `{TEST_DB}`;")
            conn.commit()
        finally:
            cur.close()
            conn.close()
