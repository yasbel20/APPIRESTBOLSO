from dotenv import load_dotenv, find_dotenv
import os
import mysql.connector
from typing import List, Dict, Any, Optional
from mysql.connector.cursor import MySQLCursorDict

# Cargar variables de entorno
load_dotenv(find_dotenv())

def get_connection():
    """Establece conexión con la base de datos MySQL."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "yasbel"),
        port=int(os.getenv("DB_PORT", "3306")),
        charset="utf8mb4"
    )

def fetch_all_bolsos() -> List[Dict[str, Any]]:
    """Obtiene todos los bolsos de la base de datos."""
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict = conn.cursor(dictionary=True)  # type: ignore
        try:
            cur.execute("SELECT * FROM bolsos ORDER BY created_at DESC;")
            rows = cur.fetchall()
            return list(rows) if rows else []
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def fetch_bolso_by_id(bolso_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene un bolso por su ID."""
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict = conn.cursor(dictionary=True)  # type: ignore
        try:
            cur.execute("SELECT * FROM bolsos WHERE id = %s", (bolso_id,))
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def insert_bolso(
    nombre: str,
    marca: str,
    precio: float,
    color: str,
    tipo: str,
    stock: int
) -> int:
    """Inserta un nuevo bolso y retorna el ID generado."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            sql = """
                INSERT INTO bolsos (nombre, marca, precio, color, tipo, stock)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (nombre, marca, precio, color, tipo, stock)
            cur.execute(sql, params)
            conn.commit()
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def update_bolso(
    bolso_id: int,
    nombre: str,
    marca: str,
    precio: float,
    color: str,
    tipo: str,
    stock: int
) -> bool:
    """Actualiza un bolso existente. Retorna True si se actualizó correctamente."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            sql = """
                UPDATE bolsos
                SET nombre = %s, marca = %s, precio = %s, 
                    color = %s, tipo = %s, stock = %s
                WHERE id = %s
            """
            params = (nombre, marca, precio, color, tipo, stock, bolso_id)
            cur.execute(sql, params)
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def delete_bolso(bolso_id: int) -> bool:
    """Elimina un bolso por su ID."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM bolsos WHERE id = %s", (bolso_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()
