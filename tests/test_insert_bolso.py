import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import insert_bolso

if __name__ == "__main__":
    try:
        nuevo_id = insert_bolso(
            nombre='Bolso Test Insertion',
            descripcion='Bolso de prueba para test de inserción',
            precio=99.99,
            stock=15,
            categoria='Bandolera',
            codigo_sku='TEST-BAND-001'
        )

        print('🆔 ID bolso insertado →', nuevo_id)
    except Exception as e:
        print('❌ Error al insertar bolso →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python tests/test_insert_bolso.py
