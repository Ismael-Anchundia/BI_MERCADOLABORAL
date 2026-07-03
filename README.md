# BI_MERCADOLABORAL

Proyecto desarrollado para la asignatura **Inteligencia de Negocios** de la Universidad Estatal Península de Santa Elena (UPSE).

El objetivo del proyecto es construir un **Pipeline ETL** que permita obtener ofertas laborales desde múltiples fuentes, almacenarlas en la zona Raw, transformarlas en la zona Staging y aplicar controles de calidad antes de su carga al Data Warehouse.

# Tecnologías utilizadas
- Python 3.13
- Pandas
- Requests
- BeautifulSoup
- Playwright
- Git

# Estructura del proyecto

data/
│
├── raw/
│   ├── api/
│   ├── archivos/
│   ├── fuente_propia/
│   └── scraping/
│
├── staging/
│
└── quality/

scripts/
│
├── api/
├── archivos/
├── fuente_propia/
├── quality/
├── scraping/
└── staging/

# Crear el entorno virtual
Windows
```bash
python -m venv .venv
```

Activar el entorno
```bash
.venv\Scripts\activate
```

Instalar las dependencias
```bash
pip install -r requirements.txt
```

# Dataset externo requerido
Este proyecto utiliza el dataset público:
**Stack Overflow Developer Survey**
Debe descargarse desde el sitio oficial de Stack Overflow:
https://survey.stackoverflow.co/

El archivo:
```
survey_results_public.csv
```

debe copiarse en:
```
data/raw/archivos/stackoverflow/
```

# Ejecución del Pipeline

## 1. Web Scraping
```bash
python scripts/scraping/computrabajo_scraper.py
```

```bash
python scripts/scraping/computrabajo_scraper_pe.py
```

```bash
python scripts/scraping/multitrabajos_scraper.py
```

```bash
python scripts/scraping/trabajosdiarios_scraper.py
```

```bash
python scripts/scraping/unmejorempleo_scraper.py
```

## 2. API
```bash
python scripts/api/github_api.py
```

## 3. Archivo estructurado
```bash
python scripts/archivos/stackoverflow_loader.py
```

## 4. Fuente propia
```bash
python scripts/fuente_propia/encuesta_loader.py
```

## 5. Procesamiento Staging
```bash
python scripts/staging/run_staging.py
```

Este proceso ejecuta automáticamente:
- stg_normalize_columns.py
- stg_dates.py
- stg_currency.py
- stg_roles.py
- stg_dedup.py

---

## 6. Framework de Calidad
```bash
python scripts/quality/run_quality.py
```

Este proceso genera automáticamente:
- reporte_calidad_ofertas.csv
- metricas_calidad_resumen.csv
- error_log_calidad.csv

# Resultado Final

Al finalizar la ejecución del pipeline se obtiene:
- Datos Raw organizados por fuente.
- Datos consolidados en Staging.
- Controles automáticos de calidad.
- Reportes de métricas.
- Registro de errores.
- Dataset preparado para el Data Warehouse.
