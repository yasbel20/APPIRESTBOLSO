import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import delete_bolso

if __name__ == "__main__":
    try:
        # Cambia este ID por uno que quieras eliminar
        bolso_id = 99
        
        eliminado = delete_bolso(bolso_id)

        if eliminado:
            print(f'✅ Bolso ID {bolso_id} eliminado correctamente')
        else:
            print(f'❌ No se pudo eliminar (¿existe el ID {bolso_id}?)')
    except Exception as e:
        print('❌ Error al eliminar bolso →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python tests/test_delete_bolso.py
