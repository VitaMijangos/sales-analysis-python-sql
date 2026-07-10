from pathlib import Path
import sqlite3

import pandas as pd


RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_BD = RUTA_PROYECTO / "database" / "ventas.db"


def ejecutar_consulta(consulta: str) -> pd.DataFrame:
    """Ejecuta una consulta SQL y devuelve el resultado en un DataFrame."""

    if not RUTA_BD.exists():
        raise FileNotFoundError(
            f"No se encontró la base de datos en: {RUTA_BD}"
        )

    with sqlite3.connect(RUTA_BD) as conexion:
        resultado = pd.read_sql_query(consulta, conexion)

    return resultado


def mostrar_resultado(titulo: str, resultado: pd.DataFrame) -> None:
    """Muestra un resultado con formato."""

    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)
    print(resultado.to_string(index=False))


def main() -> None:
    try:
        consulta_ingresos = """
        SELECT
            ROUND(SUM(total_venta), 2) AS ingresos_totales
        FROM ventas;
        """

        consulta_ticket_promedio = """
        SELECT
            ROUND(AVG(total_venta), 2) AS ticket_promedio
        FROM ventas;
        """

        consulta_productos = """
        SELECT
            producto,
            SUM(cantidad) AS unidades_vendidas,
            ROUND(SUM(total_venta), 2) AS ingresos
        FROM ventas
        GROUP BY producto
        ORDER BY ingresos DESC;
        """

        consulta_ciudades = """
        SELECT
            ciudad,
            COUNT(*) AS numero_ventas,
            ROUND(SUM(total_venta), 2) AS ingresos
        FROM ventas
        GROUP BY ciudad
        ORDER BY ingresos DESC;
        """

        consulta_categorias = """
        SELECT
            categoria,
            SUM(cantidad) AS unidades_vendidas,
            ROUND(SUM(total_venta), 2) AS ingresos
        FROM ventas
        GROUP BY categoria
        ORDER BY ingresos DESC;
        """

        consulta_metodos_pago = """
        SELECT
            metodo_pago,
            COUNT(*) AS numero_ventas,
            ROUND(SUM(total_venta), 2) AS ingresos
        FROM ventas
        GROUP BY metodo_pago
        ORDER BY ingresos DESC;
        """

        ingresos = ejecutar_consulta(consulta_ingresos)
        ticket_promedio = ejecutar_consulta(consulta_ticket_promedio)
        productos = ejecutar_consulta(consulta_productos)
        ciudades = ejecutar_consulta(consulta_ciudades)
        categorias = ejecutar_consulta(consulta_categorias)
        metodos_pago = ejecutar_consulta(consulta_metodos_pago)

        mostrar_resultado("INGRESOS TOTALES", ingresos)
        mostrar_resultado("TICKET PROMEDIO", ticket_promedio)
        mostrar_resultado("VENTAS POR PRODUCTO", productos)
        mostrar_resultado("VENTAS POR CIUDAD", ciudades)
        mostrar_resultado("VENTAS POR CATEGORÍA", categorias)
        mostrar_resultado("VENTAS POR MÉTODO DE PAGO", metodos_pago)

    except FileNotFoundError as error:
        print(f"Error: {error}")

    except sqlite3.Error as error:
        print(f"Error de SQLite: {error}")

    except Exception as error:
        print(f"Error inesperado: {error}")


if __name__ == "__main__":
    main()