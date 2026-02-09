"""
Test para la función fetch_all_bolsos.
Ejecutar: pytest tests/test_fetch_all_bolsos.py
"""
import pytest
from app.database import fetch_all_bolsos

def test_fetch_all_bolsos():
    """Verifica que se puedan obtener todos los bolsos."""
    bolsos = fetch_all_bolsos()
    
    assert isinstance(bolsos, list)
    print(f"✓ Se obtuvieron {len(bolsos)} bolsos de la base de datos")
    
    if len(bolsos) > 0:
        # Verificar estructura del primer bolso
        primer_bolso = bolsos[0]
        campos_esperados = ['id', 'nombre', 'marca', 'precio', 'color', 'tipo', 'stock']
        
        for campo in campos_esperados:
            assert campo in primer_bolso, f"Campo '{campo}' no encontrado"
        
        print("✓ Estructura de datos validada correctamente")

if __name__ == "__main__":
    test_fetch_all_bolsos()
