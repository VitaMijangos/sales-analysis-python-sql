from pathlib import Path
import sqlite3

import pandas as pd


# Ruta principal del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

# Archivo CSV limpio
RUTA_CSV = RUTA_PROYECTO / "data" / "ventas_limpias.csv"

# Base de datos SQLite
RUTA_BD = RUTA_PROYECTO / "database" / "ventas.db"


def cargar_csv(ruta_csv: Path) -> pd.DataFrame:
    """Carga el archivo CSV limpio."""

    if not ruta_csv.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo limpio en: {ruta_csv}"
        )

    return pd.read_csv(ruta_csv)


def crear_base_datos(ventas: pd.DataFrame, ruta_bd: Path) -> None:
    """Crea la base de datos y guarda el DataFrame en una tabla."""

    ruta_bd.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(ruta_bd) as conexion:
        ventas.to_sql(
            name="ventas",
            con=conexion,
            if_exists="replace",
            index=False
        )


def verificar_datos(ruta_bd: Path) -> pd.DataFrame:
    """Consulta los primeros registros guardados."""

    consulta = """
    SELECT *
    FROM ventas
    LIMIT 5;
    """

    with sqlite3.connect(ruta_bd) as conexion:
        resultado = pd.read_sql_query(consulta, conexion)

    return resultado


def contar_registros(ruta_bd: Path) -> int:
    """Cuenta cuántas ventas hay en la tabla."""

    consulta = """
    SELECT COUNT(*) AS total_registros
    FROM ventas;
    """

    with sqlite3.connect(ruta_bd) as conexion:
        resultado = pd.read_sql_query(consulta, conexion)

    return int(resultado.loc[0, "total_registros"])


def main() -> None:
    try:
        ventas = cargar_csv(RUTA_CSV)

        crear_base_datos(ventas, RUTA_BD)

        primeros_registros = verificar_datos(RUTA_BD)
        total_registros = contar_registros(RUTA_BD)

        print("=" * 60)
        print("BASE DE DATOS CREADA CORRECTAMENTE")
        print("=" * 60)

        print(f"Ubicación: {RUTA_BD}")
        print(f"Registros guardados: {total_registros}")

        print("\nPrimeros registros:")
        print(primeros_registros)

    except FileNotFoundError as error:
        print(f"Error: {error}")

    except sqlite3.Error as error:
        print(f"Error de SQLite: {error}")

    except Exception as error:
        print(f"Error inesperado: {error}")


if __name__ == "__main__":
    main()