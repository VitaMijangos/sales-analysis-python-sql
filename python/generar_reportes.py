from pathlib import Path
import sqlite3

import pandas as pd


RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_BD = RUTA_PROYECTO / "database" / "ventas.db"
RUTA_REPORTES = RUTA_PROYECTO / "reports"


def ejecutar_consulta(consulta: str) -> pd.DataFrame:
    """Ejecuta una consulta SQL y devuelve el resultado."""

    if not RUTA_BD.exists():
        raise FileNotFoundError(
            f"No se encontró la base de datos en: {RUTA_BD}"
        )

    with sqlite3.connect(RUTA_BD) as conexion:
        resultado = pd.read_sql_query(consulta, conexion)

    return resultado


def preparar_carpeta_reportes() -> None:
    """Crea la carpeta de reportes si no existe."""

    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)


def generar_reporte_kpis() -> None:
    consulta = """
    SELECT
        COUNT(*) AS numero_ventas,
        SUM(cantidad) AS unidades_vendidas,
        ROUND(SUM(total_venta), 2) AS ingresos_totales,
        ROUND(AVG(total_venta), 2) AS ticket_promedio,
        ROUND(MAX(total_venta), 2) AS venta_mas_alta,
        ROUND(MIN(total_venta), 2) AS venta_mas_baja
    FROM ventas;
    """

    resultado = ejecutar_consulta(consulta)

    ruta = RUTA_REPORTES / "kpis_generales.csv"
    resultado.to_csv(ruta, index=False)


def generar_reporte_productos() -> None:
    consulta = """
    SELECT
        producto,
        SUM(cantidad) AS unidades_vendidas,
        ROUND(SUM(total_venta), 2) AS ingresos_totales,
        ROUND(AVG(total_venta), 2) AS venta_promedio
    FROM ventas
    GROUP BY producto
    ORDER BY ingresos_totales DESC;
    """

    resultado = ejecutar_consulta(consulta)

    ruta = RUTA_REPORTES / "reporte_productos.csv"
    resultado.to_csv(ruta, index=False)


def generar_reporte_ciudades() -> None:
    consulta = """
    SELECT
        ciudad,
        COUNT(*) AS numero_ventas,
        SUM(cantidad) AS unidades_vendidas,
        ROUND(SUM(total_venta), 2) AS ingresos_totales
    FROM ventas
    GROUP BY ciudad
    ORDER BY ingresos_totales DESC;
    """

    resultado = ejecutar_consulta(consulta)

    ruta = RUTA_REPORTES / "reporte_ciudades.csv"
    resultado.to_csv(ruta, index=False)


def generar_reporte_mensual() -> None:
    consulta = """
    SELECT
        strftime('%Y-%m', fecha) AS mes,
        COUNT(*) AS numero_ventas,
        SUM(cantidad) AS unidades_vendidas,
        ROUND(SUM(total_venta), 2) AS ingresos_totales
    FROM ventas
    GROUP BY mes
    ORDER BY mes;
    """

    resultado = ejecutar_consulta(consulta)

    ruta = RUTA_REPORTES / "reporte_mensual.csv"
    resultado.to_csv(ruta, index=False)


def mostrar_resumen() -> None:
    consulta = """
    SELECT
        ROUND(SUM(total_venta), 2) AS ingresos_totales,
        ROUND(AVG(total_venta), 2) AS ticket_promedio,
        COUNT(*) AS numero_ventas
    FROM ventas;
    """

    resultado = ejecutar_consulta(consulta)

    ingresos = resultado.loc[0, "ingresos_totales"]
    ticket = resultado.loc[0, "ticket_promedio"]
    ventas = resultado.loc[0, "numero_ventas"]

    print("=" * 60)
    print("RESUMEN DEL ANÁLISIS")
    print("=" * 60)
    print(f"Número de ventas: {ventas}")
    print(f"Ingresos totales: ${ingresos:,.2f}")
    print(f"Ticket promedio: ${ticket:,.2f}")


def main() -> None:
    try:
        preparar_carpeta_reportes()

        generar_reporte_kpis()
        generar_reporte_productos()
        generar_reporte_ciudades()
        generar_reporte_mensual()

        mostrar_resumen()

        print("\nReportes generados correctamente.")
        print(f"Ubicación: {RUTA_REPORTES}")

    except FileNotFoundError as error:
        print(f"Error: {error}")

    except sqlite3.Error as error:
        print(f"Error de SQLite: {error}")

    except Exception as error:
        print(f"Error inesperado: {error}")


if __name__ == "__main__":
    main()