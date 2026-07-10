from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_BD = RUTA_PROYECTO / "database" / "ventas.db"
RUTA_IMAGENES = RUTA_PROYECTO / "images"


def ejecutar_consulta(consulta: str) -> pd.DataFrame:
    """Ejecuta una consulta SQL y devuelve un DataFrame."""

    if not RUTA_BD.exists():
        raise FileNotFoundError(
            f"No se encontró la base de datos en: {RUTA_BD}"
        )

    with sqlite3.connect(RUTA_BD) as conexion:
        resultado = pd.read_sql_query(consulta, conexion)

    return resultado


def preparar_carpeta_imagenes() -> None:
    """Crea la carpeta de imágenes si no existe."""

    RUTA_IMAGENES.mkdir(parents=True, exist_ok=True)


def grafica_ingresos_por_producto() -> None:
    consulta = """
    SELECT
        producto,
        SUM(total_venta) AS ingresos
    FROM ventas
    GROUP BY producto
    ORDER BY ingresos DESC;
    """

    datos = ejecutar_consulta(consulta)

    plt.figure(figsize=(10, 6))
    plt.bar(datos["producto"], datos["ingresos"])
    plt.title("Ingresos por producto")
    plt.xlabel("Producto")
    plt.ylabel("Ingresos")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    ruta = RUTA_IMAGENES / "ingresos_por_producto.png"
    plt.savefig(ruta, dpi=300)
    plt.close()


def grafica_ingresos_por_ciudad() -> None:
    consulta = """
    SELECT
        ciudad,
        SUM(total_venta) AS ingresos
    FROM ventas
    GROUP BY ciudad
    ORDER BY ingresos DESC;
    """

    datos = ejecutar_consulta(consulta)

    plt.figure(figsize=(9, 6))
    plt.bar(datos["ciudad"], datos["ingresos"])
    plt.title("Ingresos por ciudad")
    plt.xlabel("Ciudad")
    plt.ylabel("Ingresos")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    ruta = RUTA_IMAGENES / "ingresos_por_ciudad.png"
    plt.savefig(ruta, dpi=300)
    plt.close()


def grafica_ingresos_por_categoria() -> None:
    consulta = """
    SELECT
        categoria,
        SUM(total_venta) AS ingresos
    FROM ventas
    GROUP BY categoria
    ORDER BY ingresos DESC;
    """

    datos = ejecutar_consulta(consulta)

    plt.figure(figsize=(9, 6))
    plt.bar(datos["categoria"], datos["ingresos"])
    plt.title("Ingresos por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Ingresos")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    ruta = RUTA_IMAGENES / "ingresos_por_categoria.png"
    plt.savefig(ruta, dpi=300)
    plt.close()


def grafica_ventas_por_metodo_pago() -> None:
    consulta = """
    SELECT
        metodo_pago,
        COUNT(*) AS numero_ventas
    FROM ventas
    GROUP BY metodo_pago
    ORDER BY numero_ventas DESC;
    """

    datos = ejecutar_consulta(consulta)

    plt.figure(figsize=(8, 6))
    plt.pie(
        datos["numero_ventas"],
        labels=datos["metodo_pago"],
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Distribución de ventas por método de pago")
    plt.tight_layout()

    ruta = RUTA_IMAGENES / "ventas_por_metodo_pago.png"
    plt.savefig(ruta, dpi=300)
    plt.close()


def grafica_ventas_por_mes() -> None:
    consulta = """
    SELECT
        strftime('%Y-%m', fecha) AS mes,
        SUM(total_venta) AS ingresos
    FROM ventas
    GROUP BY mes
    ORDER BY mes;
    """

    datos = ejecutar_consulta(consulta)

    plt.figure(figsize=(10, 6))
    plt.plot(
        datos["mes"],
        datos["ingresos"],
        marker="o"
    )
    plt.title("Ingresos mensuales")
    plt.xlabel("Mes")
    plt.ylabel("Ingresos")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    ruta = RUTA_IMAGENES / "ingresos_mensuales.png"
    plt.savefig(ruta, dpi=300)
    plt.close()


def main() -> None:
    try:
        preparar_carpeta_imagenes()

        grafica_ingresos_por_producto()
        grafica_ingresos_por_ciudad()
        grafica_ingresos_por_categoria()
        grafica_ventas_por_metodo_pago()
        grafica_ventas_por_mes()

        print("=" * 60)
        print("GRÁFICAS GENERADAS CORRECTAMENTE")
        print("=" * 60)
        print(f"Ubicación: {RUTA_IMAGENES}")

    except FileNotFoundError as error:
        print(f"Error: {error}")

    except sqlite3.Error as error:
        print(f"Error de SQLite: {error}")

    except Exception as error:
        print(f"Error inesperado: {error}")


if __name__ == "__main__":
    main()