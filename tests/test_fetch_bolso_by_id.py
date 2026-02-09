"""
Test para la función fetch_bolso_by_id.
Ejecutar: pytest tests/test_fetch_bolso_by_id.py
"""
import pytest
from app.database import fetch_bolso_by_id

def test_fetch_bolso_by_id_existente():
    """Verifica que se pueda obtener un bolso existente por ID."""
    # Asumimos que existe un bolso con ID 1 (creado en init_db.sql)
    bolso = fetch_bolso_by_id(1)
    
    assert bolso is not None
    assert bolso['id'] == 1
    assert 'nombre' in bolso
    assert 'marca' in bolso
    print(f"✓ Bolso encontrado: {bolso['nombre']} - {bolso['marca']}")

def test_fetch_bolso_by_id_no_existente():
    """Verifica que devuelva None para un ID que no existe."""
    bolso = fetch_bolso_by_id(99999)
    
    assert bolso is None
    print("✓ Correctamente devuelve None para ID inexistente")

if __name__ == "__main__":
    test_fetch_bolso_by_id_existente()
    test_fetch_bolso_by_id_no_existente()
