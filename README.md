# 🎒 BolsosApp - Tienda de Bolsos

**Alumna:** Yasbel Olivares Soto  
**Curso:** 2DAW

---

##  Descripción

API REST desarrollada con FastAPI para la gestión de una tienda de bolsos. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre un catálogo simplificado de productos.

##  Características

-  CRUD completo de bolsos
-  Solo 3 tipos de bolsos: bandolera, mochila y tote
-  Validación de datos con Pydantic
-  Documentación automática con Swagger/OpenAPI
-  Conexión a MySQL
-  Tests unitarios completos

##  Requisitos Previos

- Python 3.8 o superior
- MySQL Server (XAMPP recomendado)
- pip (gestor de paquetes de Python)

##  Instalación

### 1. Clonar o descargar el proyecto

```bash
cd C:\xampp\htdocs\BolsosApp
```

### 2. Crear entorno virtual

```powershell
py -m venv .venv
```

### 3. Activar el entorno virtual

```powershell
.venv\Scripts\Activate.ps1
```

Si tienes problemas con PowerShell, usa:
```powershell
.venv\Scripts\Activate
```

### 4. Instalar las dependencias

```powershell
py -m pip install -r requirements.txt
```

### 5. Configurar la base de datos

#### a) Asegúrate de que MySQL esté corriendo (XAMPP)

Inicia Apache y MySQL desde el panel de control de XAMPP.

#### b) Ejecutar el script de inicialización

```powershell
Get-Content docs/init_db.sql | mysql -u root -p
```

Cuando te pida la contraseña, ingresa tu contraseña de root de MySQL.

### 6. Verificar el archivo .env

Asegúrate de que el archivo `.env` exista en la raíz del proyecto:

```env
DB_HOST=localhost
DB_USER=2DAW
DB_PASSWORD=2DAW_pass
DB_NAME=yasbel
DB_PORT=3306
```

##  Ejecución de la Aplicación

### Iniciar el servidor

```powershell
py -m uvicorn app.main:app --reload
```

La aplicación estará disponible en: `http://127.0.0.1:8000`

###  Documentación Interactiva

Una vez iniciado el servidor:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## 🔌 Endpoints de la API

### GET `/`
Página de bienvenida con información del proyecto.

### GET `/ping`
Healthcheck - verifica que la API esté activa.

### GET `/bolsos`
Lista todos los bolsos disponibles.

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Bolso a Eliminar",
    "marca": "Delete Test",
    "precio": 25.00,
    "color": "Gris",
    "tipo": "bandolera",
    "stock": 3,
    "created_at": "2025-02-09T10:00:00",
    "updated_at": "2025-02-09T10:00:00"
  }
]
```

### GET `/bolsos/{id}`
Obtiene un bolso específico por su ID.

### POST `/bolsos`
Crea un nuevo bolso.

**Body de ejemplo:**
```json
{
  "nombre": "Mochila Urban",
  "marca": "UrbanStyle",
  "precio": 79.99,
  "color": "Negro",
  "tipo": "mochila",
  "stock": 15
}
```

### PUT `/bolsos/{id}`
Actualiza un bolso existente.

**Body de ejemplo:**
```json
{
  "nombre": "Mochila Urban Pro",
  "marca": "UrbanStyle",
  "precio": 89.99,
  "color": "Negro Mate",
  "tipo": "mochila",
  "stock": 20
}
```

### DELETE `/bolsos/{id}`
Elimina un bolso por su ID.

**Respuesta:**
```json
{
  "mensaje": "Bolso eliminado correctamente",
  "id": 1
}
```

##  Tipos de Bolso Válidos

Solo se aceptan estos 3 tipos:
- `bandolera`
- `mochila`
- `tote`

## Tests

### Ejecutar todos los tests

```powershell
py -m pytest
```

### Ejecutar con detalles

```powershell
py -m pytest -v
```

### Ejecutar un test específico

```powershell
py -m pytest tests/test_delete_bolso.py -v
```

### Tests disponibles:
- `test_get_connection.py` - Verifica conexión a BD
- `test_fetch_all_bolsos.py` - Prueba listar todos los bolsos
- `test_fetch_bolso_by_id.py` - Prueba obtener por ID
- `test_insert_bolso.py` - Prueba crear bolso
- `test_update_bolso.py` - Prueba actualizar bolso
- `test_delete_bolso.py` - Prueba eliminar bolso

##  Modelo de Base de Datos


##  Tecnologías Utilizadas

- **FastAPI** - Framework web moderno
- **Pydantic** - Validación de datos
- **MySQL Connector** - Conexión a MySQL
- **Python-dotenv** - Variables de entorno
- **Uvicorn** - Servidor ASGI
- **Pytest** - Framework de testing

##   Troubleshooting

###  Error: "Unable to create process using..."

Usa `py -m` antes del comando:
```powershell
py -m uvicorn app.main:app --reload
py -m pip install <paquete>
py -m pytest
```

###  Error de conexión a MySQL

Verifica:
1. MySQL está corriendo en XAMPP
2. Usuario `2DAW` existe con contraseña `2DAW_pass`
3. Base de datos `yasbel` existe
4. Archivo `.env` tiene las credenciales correctas

###  Recrear el entorno virtual

Si tienes problemas con el entorno virtual:
```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

##  Datos de Prueba

La base de datos incluye un bolso de ejemplo:

```
Nombre: Bolso a Eliminar
Marca: Delete Test
Precio: 25.00€
Color: Gris
Tipo: bandolera
Stock: 3 unidades
```

##    Información del Proyecto

**Proyecto:** BolsosApp - API REST de Tienda de Bolsos  
**Alumna:** Yasbel Olivares Soto  
**Curso:** 2DAW  
**Framework:** FastAPI  
**Base de Datos:** MySQL  

---

**Desarrollado por Yasbel Olivares Soto - 2DAW**
