from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Annotated
from datetime import datetime
from decimal import Decimal

from app.database import (
    fetch_all_bolsos,
    fetch_bolso_by_id,
    insert_bolso,
    update_bolso,
    delete_bolso
)

app = FastAPI(
    title="BolsosApp - Tienda de Bolsos",
    version="1.0.0",
    description="API REST para gestión de tienda de bolsos - Yasbel Olivares Soto 2DAW"
)

# ========================
# Modelos Pydantic
# ========================

class BolsoBase(BaseModel):
    """Modelo base con los campos del bolso."""
    nombre: Annotated[str, Field(min_length=1, max_length=100)]
    marca: Annotated[str, Field(min_length=1, max_length=100)]
    precio: Annotated[float, Field(gt=0)]
    color: Annotated[str, Field(min_length=1, max_length=50)]
    tipo: Annotated[str, Field(pattern='^(bandolera|mochila|tote)$')]
    stock: int = Field(ge=0)

class BolsoDB(BolsoBase):
    """Modelo para lectura desde BD (incluye ID y timestamps)."""
    id: int
    created_at: datetime
    updated_at: datetime

class BolsoCreate(BolsoBase):
    """Modelo para crear bolso."""
    pass

class BolsoUpdate(BolsoBase):
    """Modelo para actualizar bolso."""
    pass

# ========================
# Funciones Helper
# ========================

def map_row_to_bolso(row: dict) -> BolsoDB:
    """Convierte una fila de la BD en objeto BolsoDB."""
    bolso_data = dict(row)
    # Convertir Decimal a float para Pydantic
    if 'precio' in bolso_data and isinstance(bolso_data['precio'], Decimal):
        bolso_data['precio'] = float(bolso_data['precio'])
    return BolsoDB(**bolso_data)

# ========================
# Endpoints
# ========================

@app.get("/")
def root():
    """Endpoint raíz."""
    return {
        "message": "BolsosApp - Tienda de Bolsos",
        "alumna": "Yasbel Olivares Soto",
        "curso": "2DAW"
    }

@app.get("/ping")
def ping():
    """Healthcheck - Verifica que la API esté activa."""
    return {"message": "pong"}

@app.get("/bolsos", response_model=List[BolsoDB])
def listar_bolsos():
    """Lista todos los bolsos disponibles."""
    rows = fetch_all_bolsos()
    return [map_row_to_bolso(row) for row in rows]

@app.get("/bolsos/{bolso_id}", response_model=BolsoDB)
def obtener_bolso(bolso_id: int):
    """Obtiene un bolso específico por su ID."""
    row = fetch_bolso_by_id(bolso_id)
    if not row:
        raise HTTPException(status_code=404, detail="Bolso no encontrado")
    return map_row_to_bolso(row)

@app.post("/bolsos", response_model=BolsoDB, status_code=201)
def crear_bolso(bolso: BolsoCreate):
    """Crea un nuevo bolso en la tienda."""
    nuevo_id = insert_bolso(**bolso.model_dump())
    
    if not nuevo_id:
        raise HTTPException(status_code=500, detail="Error al crear bolso")
    
    row = fetch_bolso_by_id(nuevo_id)
    return map_row_to_bolso(row)

@app.put("/bolsos/{bolso_id}", response_model=BolsoDB)
def actualizar_bolso(bolso_id: int, bolso: BolsoUpdate):
    """Actualiza un bolso existente."""
    if not fetch_bolso_by_id(bolso_id):
        raise HTTPException(status_code=404, detail="Bolso no encontrado")
    
    exito = update_bolso(bolso_id=bolso_id, **bolso.model_dump())
    
    if not exito:
        raise HTTPException(status_code=500, detail="Error al actualizar")
    
    row = fetch_bolso_by_id(bolso_id)
    return map_row_to_bolso(row)

@app.delete("/bolsos/{bolso_id}")
def eliminar_bolso(bolso_id: int):
    """Elimina un bolso de la tienda."""
    if not fetch_bolso_by_id(bolso_id):
        raise HTTPException(status_code=404, detail="Bolso no encontrado")
    
    if delete_bolso(bolso_id):
        return {"mensaje": "Bolso eliminado correctamente", "id": bolso_id}
    
    raise HTTPException(status_code=500, detail="Error al eliminar")