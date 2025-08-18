import sqlite3
import pandas as pd
import os
from langchain_core.tools import tool

def get_db_connection():
    return sqlite3.connect('datos.sqlite')

@tool
def query_customer_master(id_acuerdo: str):
    """
    Consultar la información del cliente por número de acuerdo.
    """
    conn = get_db_connection()
    query = f"SELECT * FROM maestro WHERE id_acuerdo = '{id_acuerdo}'"
    df = pd.read_sql(query, conn)
    conn.close()
    if df.empty:
        return f"No se encontró información para el acuerdo {id_acuerdo}."
    return "Fuente: Tabla maestro\n" + df.to_markdown(index=False)

@tool
def query_consumption_records(id_acuerdo: str):
    """
    Consultar el historial de consumo de un cliente por número de acuerdo, incluyendo los detalles del cliente.
    """
    conn = get_db_connection()
    query = f"""
    SELECT
        m.nombre_cliente,
        c.fecha,
        c.consumo_kwh
    FROM consumos c
    JOIN maestro m ON c.id_acuerdo = m.id_acuerdo
    WHERE c.id_acuerdo = '{id_acuerdo}'
    """
    df = pd.read_sql(query, conn)
    conn.close()
    if df.empty:
        return f"No se encontró historial de consumo para el acuerdo {id_acuerdo}."
    return "Fuente: Tablas consumos y maestro\n" + df.to_markdown(index=False)

@tool
def query_field_activities(id_acuerdo: str):
    """
    Consultar las actividades de campo de un cliente por número de acuerdo, uniendo con el punto de servicio.
    """
    conn = get_db_connection()
    query = f"""
    SELECT
        m.nombre_cliente,
        a.descripcion_actividad,
        a.fecha_actividad
    FROM actividades a
    JOIN maestro m ON a.id_punto_servicio = m.id_punto_servicio
    WHERE m.id_acuerdo = '{id_acuerdo}'
    """
    df = pd.read_sql(query, conn)
    conn.close()
    if df.empty:
        return f"No se encontraron actividades de campo para el acuerdo {id_acuerdo}."
    return "Fuente: Tablas actividades y maestro\n" + df.to_markdown(index=False)

def get_all_tools():
    return [
        query_customer_master,
        query_consumption_records,
        query_field_activities
    ]
