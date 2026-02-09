"""
Test para la función insert_bolso.
Ejecutar: pytest tests/test_insert_bolso.py
"""
import pytest
from app.database import insert_bolso, fetch_bolso_by_id, delete_bolso

def test_insert_bolso():
    """Verifica que se pueda insertar un nuevo bolso."""
    # Datos de prueba
    datos_bolso = {
        "nombre": "Bolso Test",
        "marca": "Test Brand",
        "precio": 99.99,
        "color": "Azul",
        "tipo": "bandolera",
        "stock": 10
    }
    
    # Insertar bolso
    nuevo_id = insert_bolso(**datos_bolso)
    
    assert nuevo_id > 0
    print(f" Bolso insertado con ID: {nuevo_id}")
    
    # Verificar que se insertó correctamente
    bolso_insertado = fetch_bolso_by_id(nuevo_id)
    assert bolso_insertado is not None
    assert bolso_insertado['nombre'] == datos_bolso['nombre']
    assert bolso_insertado['marca'] == datos_bolso['marca']
    assert float(bolso_insertado['precio']) == datos_bolso['precio']
    print("✓ Datos insertados correctamente verificados")
    
    # Limpiar: eliminar el bolso de prueba
    delete_bolso(nuevo_id)
    print(" Bolso de prueba eliminado")

if __name__ == "__main__":
    test_insert_bolso()
