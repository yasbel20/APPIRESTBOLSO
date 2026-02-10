import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import fetch_all_bolsos

if __name__ == "__main__":
    try:
        bolsos = fetch_all_bolsos()
        print('✅ Total de bolsos en BD →', len(bolsos))
        for b in bolsos:
            print(f"  • {b['nombre']} - ${b['precio']} (Stock: {b['stock']})")
    except Exception as e:
        print('❌ Error al obtener bolsos →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python tests/test_fetch_all_bolsos.py
