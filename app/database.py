from dotenv import load_dotenv, find_dotenv
import os
import mysql.connector
from typing import List, Dict, Any, cast
from mysql.connector.cursor import MySQLCursorDict

# Carga .env desde la raíz
load_dotenv(find_dotenv())

def get_connection():
    """
    Crea una conexión a MySQL con configuración corregida.
    
    CAMBIOS IMPORTANTES:
    - charset='utf8mb4' (antes era 'utf8mb4_general_ci' que causaba error)
    - autocommit=False para asegurar control manual de transacciones
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "Yasbel"),
        password=os.getenv("DB_PASSWORD", "1234567"),
        database=os.getenv("DB_NAME", "bolsosapp"),
        port=int(os.getenv("DB_PORT", "3306")),
        charset="utf8mb4",  # ✅ CORREGIDO: era utf8mb4_general_ci (collation)
        autocommit=False     # ✅ AÑADIDO: Asegura que necesitamos commit explícito
    )

def fetch_all_bolsos() -> List[Dict[str, Any]]:
    """
    Ejecuta SELECT * FROM bolso y devuelve una lista de dicts.
    """
    conn = None
    try:
        conn = get_connection()

        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]

        try:
            cur.execute(
                """
                SELECT
                    id_bolso,
                    nombre,
                    descripcion,
                    precio,
                    stock,
                    categoria,
                    codigo_sku,
                    activo
                FROM bolso;
                """
            )

            rows = cast(List[Dict[str, Any]], cur.fetchall())
            return rows

        finally:
            cur.close()

    finally:
        if conn:
            conn.close()

def insert_bolso(
    nombre: str,
    descripcion: str | None,
    precio: float,
    stock: int,
    categoria: str,
    codigo_sku: str,
    activo: bool = True
) -> int:
    """
    Inserta un nuevo bolso en la base de datos.
    Retorna el ID del bolso insertado.
    
    ⚠️ IMPORTANTE: Ahora incluye manejo de errores mejorado
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO bolso
                    (nombre, descripcion, precio, stock, categoria, codigo_sku, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    nombre,
                    descripcion,
                    precio,
                    stock,
                    categoria,
                    codigo_sku,
                    activo
                )
            )
            # ✅ CRÍTICO: COMMIT para guardar cambios
            conn.commit()
            
            inserted_id = cur.lastrowid or 0
            
            # Log para debug (puedes comentarlo después)
            print(f"[DEBUG] INSERT exitoso - ID: {inserted_id}")
            
            return inserted_id
            
        except Exception as e:
            # ✅ AÑADIDO: Rollback en caso de error
            conn.rollback()
            print(f"[ERROR] Error en insert_bolso: {e}")
            raise  # Re-lanzar la excepción para que FastAPI la maneje
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def delete_bolso(bolso_id: int) -> bool:
    """
    Elimina un bolso de la base de datos por su ID.
    Retorna True si se eliminó correctamente, False si no se encontró.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM bolso WHERE id_bolso = %s",
                (bolso_id,)
            )
            # ✅ CRÍTICO: COMMIT para guardar cambios
            conn.commit()
            
            deleted = cur.rowcount > 0
            
            # Log para debug
            print(f"[DEBUG] DELETE - ID: {bolso_id}, Eliminado: {deleted}")
            
            return deleted
            
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Error en delete_bolso: {e}")
            raise
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def fetch_bolso_by_id(bolso_id: int) -> Dict[str, Any] | None:
    """
    Obtiene un bolso por su ID.
    Retorna un dict con los datos del bolso o None si no existe.
    """
    conn = None
    try:
        conn = get_connection()

        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]

        try:
            cur.execute(
                """
                SELECT
                    id_bolso,
                    nombre,
                    descripcion,
                    precio,
                    stock,
                    categoria,
                    codigo_sku,
                    activo
                FROM bolso
                WHERE id_bolso = %s
                """,
                (bolso_id,)
            )
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def update_bolso(
    bolso_id: int,
    nombre: str,
    descripcion: str | None,
    precio: float,
    stock: int,
    categoria: str,
    codigo_sku: str,
    activo: bool
) -> bool:
    """
    Actualiza los datos de un bolso existente.
    Retorna True si se actualizó correctamente, False si no se encontró.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                UPDATE bolso
                SET
                    nombre = %s,
                    descripcion = %s,
                    precio = %s,
                    stock = %s,
                    categoria = %s,
                    codigo_sku = %s,
                    activo = %s
                WHERE id_bolso = %s
                """,
                (
                    nombre,
                    descripcion,
                    precio,
                    stock,
                    categoria,
                    codigo_sku,
                    activo,
                    bolso_id
                )
            )
            # ✅ CRÍTICO: COMMIT para guardar cambios
            conn.commit()
            
            updated = cur.rowcount > 0
            
            # Log para debug
            print(f"[DEBUG] UPDATE - ID: {bolso_id}, Actualizado: {updated}")
            
            return updated
            
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Error en update_bolso: {e}")
            raise
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()