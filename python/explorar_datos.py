from pathlib import Path

import pandas as pd


# Obtiene la carpeta principal del proyecto.
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

# Construye la ruta hacia el archivo CSV.
RUTA_VENTAS = RUTA_PROYECTO / "data" / "ventas.csv"


def cargar_ventas(ruta: Path) -> pd.DataFrame:
    """Carga el archivo de ventas y devuelve un DataFrame."""

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de ventas en: {ruta}"
        )

    return pd.read_csv(ruta)


def explorar_datos(ventas: pd.DataFrame) -> None:
    """Muestra información general del dataset."""

    print("=" * 60)
    print("PRIMERAS FILAS DEL DATASET")
    print("=" * 60)
    print(ventas.head())

    print("\n" + "=" * 60)
    print("DIMENSIONES")
    print("=" * 60)
    print(f"Filas: {ventas.shape[0]}")
    print(f"Columnas: {ventas.shape[1]}")

    print("\n" + "=" * 60)
    print("COLUMNAS")
    print("=" * 60)
    print(ventas.columns.tolist())

    print("\n" + "=" * 60)
    print("TIPOS DE DATOS")
    print("=" * 60)
    print(ventas.dtypes)

    print("\n" + "=" * 60)
    print("VALORES NULOS")
    print("=" * 60)
    print(ventas.isnull().sum())


def main() -> None:
    try:
        ventas = cargar_ventas(RUTA_VENTAS)
        explorar_datos(ventas)

    except FileNotFoundError as error:
        print(f"Error: {error}")

    except pd.errors.EmptyDataError:
        print("Error: el archivo CSV está vacío.")

    except pd.errors.ParserError:
        print("Error: el archivo CSV tiene un formato incorrecto.")

    except Exception as error:
        print(f"Ocurrió un error inesperado: {error}")


if __name__ == "__main__":
    main()