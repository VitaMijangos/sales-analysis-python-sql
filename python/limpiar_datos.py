from pathlib import Path
import pandas as pd

# Ruta principal del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

# Archivo de entrada
RUTA_VENTAS = RUTA_PROYECTO / "data" / "ventas.csv"

# Archivo limpio
RUTA_LIMPIA = RUTA_PROYECTO / "data" / "ventas_limpias.csv"


def cargar_datos():
    return pd.read_csv(RUTA_VENTAS)


def limpiar_datos(df):

    # Convertir fecha
    df["fecha"] = pd.to_datetime(df["fecha"])

    # Total de cada venta
    df["total_venta"] = df["precio_unitario"] * df["cantidad"]

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Eliminar espacios
    columnas_texto = [
        "cliente",
        "producto",
        "categoria",
        "ciudad",
        "metodo_pago"
    ]

    for columna in columnas_texto:
        df[columna] = df[columna].str.strip()

    return df


def guardar(df):
    df.to_csv(RUTA_LIMPIA, index=False)


def main():

    ventas = cargar_datos()

    ventas = limpiar_datos(ventas)

    guardar(ventas)

    print("="*60)
    print("Datos limpiados correctamente")
    print("="*60)

    print(ventas.head())


if __name__ == "__main__":
    main()