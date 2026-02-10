from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Annotated
from decimal import Decimal

from app.database import fetch_all_bolsos, fetch_bolso_by_id, insert_bolso, update_bolso, delete_bolso

app = FastAPI(
    title="BolsosApp API",
    version="1.0.0",
    description="API REST desacoplada para gestiÃ³n de tienda de bolsos - Yasbel Olivares Soto 2DAW"
)

@app.get("/")
def root():
    return {"message": "Bienvenido a BolsosApi - GestiÃ³n de Reservas"}


# ========================
# Modelos Pydantic
# ========================

class BolsoBase(BaseModel):
    """Modelo base con validaciones compartidas para Bolso."""
    nombre: Annotated[str, Field(min_length=1, max_length=80)]
    descripcion: Optional[Annotated[str, Field(max_length=255)]] = None
    precio: float = Field(ge=0)
    stock: int = Field(ge=0)
    categoria: Annotated[str, Field(min_length=1, max_length=50)]
    codigo_sku: Annotated[str, Field(min_length=1, max_length=20)]
    activo: bool = True

    @field_validator('nombre', 'categoria')
    @classmethod
    def validar_nombre_categoria(cls, v: str) -> str:
        """Valida nombre y categorÃ­a."""
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacÃ­o')
        return v.strip()

    @field_validator('codigo_sku')
    @classmethod
    def validar_codigo_sku(cls, v: str) -> str:
        """Valida cÃ³digo SKU."""
        v = v.strip().upper()
        if not v:
            raise ValueError('El SKU no puede estar vacÃ­o')
        return v

    @field_validator('descripcion')
    @classmethod
    def validar_descripcion(cls, v: Optional[str]) -> Optional[str]:
        """Valida descripciÃ³n."""
        if v is None or v.strip() == '':
            return None
        return v.strip()


class BolsoDB(BaseModel):
    """Modelo para lectura desde BD (sin validaciones estrictas para datos histÃ³ricos)."""
    id_bolso: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    categoria: str
    codigo_sku: str
    activo: bool


class BolsoCreate(BolsoBase):
    """Modelo para crear nuevo bolso (sin ID)."""
    pass


class BolsoUpdate(BolsoBase):
    """Modelo para actualizar bolso (sin ID)."""
    pass


class Bolso(BolsoBase):
    """Modelo completo de Bolso (con ID y validaciones)."""
    id_bolso: int


# ========================
# Funciones Helper
# ========================

def map_rows_to_bolsos(rows: List[dict]) -> List[BolsoDB]:
    """
    Convierte las filas del SELECT * FROM bolso (dict) 
    en objetos BolsoDB. Maneja conversiÃ³n de tipos incompatibles
    como Decimal â†’ float.
    """
    bolsosapp_db = []
    for row in rows:
        # Preparar datos para BolsoDB
        bolso_data = dict(row)
        
        # Convertir Decimal a float si es necesario
        if isinstance(bolso_data.get("precio"), Decimal):
            bolso_data["precio"] = float(bolso_data["precio"])
        
        # Garantizar booleano para activo
        bolso_data["activo"] = bool(bolso_data.get("activo", False))
        
        # Crear objeto BolsoDB desempacando el diccionario
        bolso = BolsoDB(**bolso_data)
        bolsosapp_db.append(bolso)

    return bolsosapp_db


# ========================
# Endpoints
# ========================

@app.get("/ping")
def ping():
    """Endpoint de prueba."""
    return {"message": "pong"}


@app.get("/bolso", response_model=List[Bolso])
def listar_bolsos():
    """
    Devuelve la lista de todos los bolsos desde la base de datos.
    
    - Obtiene datos raw de MySQL
    - Mapea a BolsoDB (convierte tipos incompatibles)
    - Valida estructura con Pydantic
    - Retorna lista de Bolsos
    """
    # 1. Obtener datos desde MySQL
    rows = fetch_all_bolsos()

    # 2. Mapear a BolsoDB (conversiÃ³n de tipos)
    bolsosapp = map_rows_to_bolsos(rows)

    # 3. Retornar como Bolso (con validaciÃ³n de Pydantic)
    return bolsosapp


@app.get("/bolso/{bolso_id}", response_model=Bolso)
def obtener_bolso(bolso_id: int):
    """
    Devuelve un bolso especÃ­fico por su ID.
    
    - Obtiene datos raw de MySQL
    - Mapea a BolsoDB (convierte tipos incompatibles)
    - Valida estructura con Pydantic
    - Retorna el Bolso o lanza HTTPException 404 si no existe
    """
    # 1. Obtener datos desde MySQL
    row = fetch_bolso_by_id(bolso_id)
    
    # 2. Validar que el bolso existe
    if not row:
        raise HTTPException(
            status_code=404,
            detail=f"Bolso con ID {bolso_id} no encontrado"
        )
    
    # 3. Mapear a BolsoDB (conversiÃ³n de tipos)
    bolsosapp = map_rows_to_bolsos([row])
    
    # 4. Retornar el primer (y Ãºnico) elemento
    return bolsosapp[0]


@app.post("/bolso", response_model=Bolso, status_code=201)
def crear_bolso(bolso: BolsoCreate):
    """
    Crea un nuevo bolso en la base de datos.
    
    - Valida datos con Pydantic (BolsoCreate)
    - Inserta en MySQL
    - Retorna el bolso creado con ID asignado
    """
    # 1. Insertar el bolso en MySQL (retorna ID)
    nuevo_id = insert_bolso(
        nombre=bolso.nombre,
        descripcion=bolso.descripcion,
        precio=bolso.precio,
        stock=bolso.stock,
        categoria=bolso.categoria,
        codigo_sku=bolso.codigo_sku,
        activo=bolso.activo
    )
    
    # 2. Validar que la inserciÃ³n fue exitosa
    if not nuevo_id or nuevo_id == 0:
        raise HTTPException(
            status_code=500,
            detail="Error al insertar el bolso en la base de datos"
        )
    
    # 3. Recuperar el bolso creado desde la BD
    row = fetch_bolso_by_id(nuevo_id)
    
    if not row:
        raise HTTPException(
            status_code=500,
            detail="Error al recuperar el bolso reciÃ©n creado"
        )
    
    # 4. Mapear y retornar
    bolsosapp = map_rows_to_bolsos([row])
    return bolsosapp[0]


@app.put("/bolso/{bolso_id}", response_model=Bolso)
def actualizar_bolso(bolso_id: int, bolso: BolsoUpdate):
    """
    Actualiza un bolso existente en la base de datos.
    
    - Valida que el bolso existe (404 si no)
    - Valida datos con Pydantic (BolsoUpdate)
    - Actualiza en MySQL
    - Retorna el bolso actualizado
    """
    # 1. Validar que el bolso existe
    row_existente = fetch_bolso_by_id(bolso_id)
    
    if not row_existente:
        raise HTTPException(
            status_code=404,
            detail=f"Bolso con ID {bolso_id} no encontrado"
        )
    
    # 2. Actualizar el bolso en MySQL
    actualizado = update_bolso(
        bolso_id=bolso_id,
        nombre=bolso.nombre,
        descripcion=bolso.descripcion,
        precio=bolso.precio,
        stock=bolso.stock,
        categoria=bolso.categoria,
        codigo_sku=bolso.codigo_sku,
        activo=bolso.activo
    )
    
    # 3. Validar que la actualizaciÃ³n fue exitosa
    if not actualizado:
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar el bolso en la base de datos"
        )
    
    # 4. Recuperar el bolso actualizado desde la BD
    row_actualizado = fetch_bolso_by_id(bolso_id)
    
    if not row_actualizado:
        raise HTTPException(
            status_code=500,
            detail="Error al recuperar el bolso actualizado"
        )
    
    # 5. Mapear y retornar
    bolsosapp = map_rows_to_bolsos([row_actualizado])
    return bolsosapp[0]


@app.delete("/bolso/{bolso_id}", status_code=200)
def eliminar_bolso(bolso_id: int):
    """
    Elimina un bolso existente de la base de datos.
    
    - Valida que el bolso existe (404 si no)
    - Elimina de MySQL
    - Retorna mensaje de Ã©xito
    """
    # 1. Validar que el bolso existe
    row_existente = fetch_bolso_by_id(bolso_id)
    
    if not row_existente:
        raise HTTPException(
            status_code=404,
            detail=f"Bolso con ID {bolso_id} no encontrado"
        )
    
    # 2. Eliminar el bolso de MySQL
    eliminado = delete_bolso(bolso_id)
    
    # 3. Validar que la eliminaciÃ³n fue exitosa
    if not eliminado:
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar el bolso de la base de datos"
        )
    
    # 4. Retornar mensaje de Ã©xito
    return {
        "mensaje": "Bolso eliminado exitosamente",
        "id_bolso": bolso_id
    }