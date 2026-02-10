import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import fetch_bolso_by_id

if __name__ == "__main__":
    try:
        # Cambia este ID por uno que exista en tu BD
        bolso_id = 1
        bolso = fetch_bolso_by_id(bolso_id)
        
        if bolso:
            print(f'✅ Bolso encontrado (ID {bolso_id}) →')
            print(f"  • Nombre: {bolso['nombre']}")
            print(f"  • Precio: ${bolso['precio']}")
            print(f"  • Stock: {bolso['stock']}")
            print(f"  • Categoría: {bolso['categoria']}")
            print(f"  • SKU: {bolso['codigo_sku']}")
        else:
            print(f'❌ No se encontró bolso con ID {bolso_id}')
    except Exception as e:
        print('❌ Error al buscar bolso →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python tests/test_fetch_bolso_by_id.py
