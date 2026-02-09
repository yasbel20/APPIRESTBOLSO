"""
Test para la función update_bolso.
Ejecutar: pytest tests/test_update_bolso.py
"""
import pytest
from app.database import insert_bolso, update_bolso, fetch_bolso_by_id, delete_bolso

def test_update_bolso():
    """Verifica que se pueda actualizar un bolso existente."""
    # 1. Crear un bolso de prueba
    datos_iniciales = {
        "nombre": "Bolso Original",
        "marca": "Original Brand",
        "precio": 50.00,
        "color": "Rojo",
        "tipo": "tote",
        "stock": 5
    }
    
    bolso_id = insert_bolso(**datos_iniciales)
    assert bolso_id > 0
    print(f"✓ Bolso de prueba creado con ID: {bolso_id}")
    
    # 2. Actualizar el bolso
    datos_actualizados = {
        "nombre": "Bolso Actualizado",
        "marca": "Updated Brand",
        "precio": 75.50,
        "color": "Verde",
        "tipo": "bandolera",
        "stock": 15
    }
    
    exito = update_bolso(bolso_id=bolso_id, **datos_actualizados)
    assert exito is True
    print("✓ Bolso actualizado exitosamente")
    
    # 3. Verificar los cambios
    bolso_actualizado = fetch_bolso_by_id(bolso_id)
    assert bolso_actualizado['nombre'] == "Bolso Actualizado"
    assert bolso_actualizado['marca'] == "Updated Brand"
    assert float(bolso_actualizado['precio']) == 75.50
    assert bolso_actualizado['stock'] == 15
    print("✓ Cambios verificados correctamente")
    
    # 4. Limpiar
    delete_bolso(bolso_id)
    print("✓ Bolso de prueba eliminado")

def test_update_bolso_no_existente():
    """Verifica que devuelva False al actualizar un bolso inexistente."""
    datos = {
        "nombre": "No existe",
        "marca": "Test",
        "precio": 10.00,
        "color": "Negro",
        "tipo": "tote",
        "stock": 0
    }
    
    exito = update_bolso(bolso_id=99999, **datos)
    assert exito is False
    print("✓ Correctamente devuelve False para ID inexistente")

if __name__ == "__main__":
    test_update_bolso()
    test_update_bolso_no_existente()
