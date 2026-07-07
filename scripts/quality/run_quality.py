"""
==========================================================
RUN QUALITY
==========================================================

Descripción:
Este script automatiza la ejecución completa del Framework de Calidad de Datos.

Su función es ejecutar, en el orden correcto, los procesos encargados de evaluar la calidad del conjunto
de datos generado durante la etapa de Staging.

Procesos ejecutados:
1. Evaluación de los controles de calidad.
2. Generación del registro de errores.

Salidas:
- reporte_calidad_ofertas.csv
- metricas_calidad_resumen.csv
- error_log_calidad.csv
==========================================================
"""

import subprocess
import sys
from pathlib import Path

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]

# Scripts que conforman el Framework de Calidad.
# Se ejecutan secuencialmente para garantizar que primero se generen las métricas y posteriormente
# el registro de errores.
SCRIPTS = [
    "quality_checks.py",
    "error_logger.py"
]

# ==========================================================
# EJECUCIÓN DE UN SCRIPT
# ==========================================================

def ejecutar_script(script):
    """
    Ejecuta un script perteneciente al Framework de Calidad de Datos.
    Si alguno de los procesos falla, la ejecución del pipeline se detiene para evitar resultados
    inconsistentes.
    """
    ruta_script = BASE_DIR / "scripts" / "quality" / script

    print("\n" + "=" * 70)
    print(f"Ejecutando: {script}")
    print("=" * 70)

    resultado = subprocess.run(
        [sys.executable, str(ruta_script)],
        cwd=BASE_DIR
    )

    if resultado.returncode != 0:
        raise RuntimeError(f"Error ejecutando {script}")
    
# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():
    """
    Ejecuta de forma secuencial todos los procesos del Framework de Calidad de Datos y muestra la ubicación
    de los archivos generados.
    """
    print("=" * 70)
    print("PIPELINE DE CALIDAD DE DATOS")
    print("=" * 70)

    for script in SCRIPTS:
        ejecutar_script(script)

    print("\n" + "=" * 70)
    print("FRAMEWORK DE CALIDAD FINALIZADO CORRECTAMENTE")
    print("=" * 70)
    print("Archivos generados:")
    print(BASE_DIR / "data" / "quality" / "reporte_calidad_ofertas.csv")
    print(BASE_DIR / "data" / "quality" / "metricas_calidad_resumen.csv")
    print(BASE_DIR / "data" / "quality" / "error_log_calidad.csv")

# ==========================================================
# EJECUCIÓN DEL SCRIPT
# ==========================================================

if __name__ == "__main__":
    main()