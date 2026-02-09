"""
Test para verificar la conexión a la base de datos.
Ejecutar: pytest tests/test_get_connection.py
"""
import pytest
from app.database import get_connection

def test_get_connection():
    """Verifica que se pueda establecer conexión con la base de datos."""
    conn = None
    try:
        conn = get_connection()
        assert conn is not None
        assert conn.is_connected()
        print("✓ Conexión exitosa a la base de datos")
    except Exception as e:
        pytest.fail(f"Error al conectar con la base de datos: {str(e)}")
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    test_get_connection()
