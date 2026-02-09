"""
Test para la función delete_bolso.
Ejecutar: pytest tests/test_delete_bolso.py
"""
import pytest
from app.database import insert_bolso, delete_bolso, fetch_bolso_by_id

def test_delete_bolso():
    """Verifica que se pueda eliminar un bolso existente."""
    # 1. Crear un bolso de prueba
    datos_bolso = {
        "nombre": "Bolso a Eliminar",
        "marca": "Delete Test",
        "precio": 25.00,
        "color": "Gris",
        "tipo": "bandolera",
        "stock": 3
    }
    
    bolso_id = insert_bolso(**datos_bolso)
    assert bolso_id > 0
    print(f"✓ Bolso de prueba creado con ID: {bolso_id}")
    
    # 2. Verificar que existe
    bolso = fetch_bolso_by_id(bolso_id)
    assert bolso is not None
    print(" Bolso existe antes de eliminar")
    
    # 3. Eliminar el bolso
    exito = delete_bolso(bolso_id)
    assert exito is True
    print(" Bolso eliminado exitosamente")
    
    # 4. Verificar que ya no existe
    bolso_eliminado = fetch_bolso_by_id(bolso_id)
    assert bolso_eliminado is None
    print(" Confirmado que el bolso ya no existe")

def test_delete_bolso_no_existente():
    """Verifica que devuelva False al eliminar un bolso inexistente."""
    exito = delete_bolso(99999)
    assert exito is False
    print(" Correctamente devuelve False para ID inexistente")

if __name__ == "__main__":
    test_delete_bolso()
    test_delete_bolso_no_existente()
