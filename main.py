import subprocess
import sys
from pathlib import Path


RUTA_PROYECTO = Path(__file__).resolve().parent


def ejecutar_script(nombre_script: str) -> None:
    """Ejecuta un archivo de Python ubicado en la carpeta python."""

    ruta_script = RUTA_PROYECTO / "python" / nombre_script

    print("\n" + "=" * 70)
    print(f"EJECUTANDO: {nombre_script}")
    print("=" * 70)

    resultado = subprocess.run(
        [sys.executable, str(ruta_script)],
        check=False
    )

    if resultado.returncode != 0:
        raise RuntimeError(
            f"El archivo {nombre_script} terminó con un error."
        )


def main() -> None:
    scripts = [
        "explorar_datos.py",
        "limpiar_datos.py",
        "crear_base_datos.py",
        "analisis_sql.py",
        "generar_graficas.py",
        "generar_reportes.py"
    ]

    try:
        for script in scripts:
            ejecutar_script(script)

        print("\n" + "=" * 70)
        print("PROCESO COMPLETADO CORRECTAMENTE")
        print("=" * 70)
        print("Se limpiaron los datos.")
        print("Se creó la base de datos.")
        print("Se ejecutaron las consultas SQL.")
        print("Se generaron las gráficas.")
        print("Se generaron los reportes.")

    except FileNotFoundError as error:
        print(f"Error: no se encontró un archivo requerido: {error}")

    except RuntimeError as error:
        print(f"Error: {error}")

    except Exception as error:
        print(f"Error inesperado: {error}")


if __name__ == "__main__":
    main()