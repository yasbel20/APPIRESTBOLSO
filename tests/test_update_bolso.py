import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import update_bolso

if __name__ == "__main__":
    try:
        # Cambia este ID por uno que exista en tu BD
        bolso_id = 1
        
        actualizado = update_bolso(
            bolso_id=bolso_id,
            nombre='Bolso Actualizado Test',
            descripcion='Descripción actualizada en el test',
            precio=119.99,
            stock=20,
            categoria='Bandolera',
            codigo_sku='BAND-CLAS-001',
            activo=True
        )

        if actualizado:
            print(f'✅ Bolso ID {bolso_id} actualizado correctamente')
        else:
            print(f'❌ No se pudo actualizar (¿existe el ID {bolso_id}?)')
    except Exception as e:
        print('❌ Error al actualizar bolso →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python tests/test_update_bolso.py
