import re
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_staging_final.csv"
OUTPUT_FILE = BASE_DIR / "data" / "staging" / "ofertas_staging_dw.csv"

CIUDADES_ECUADOR = {
    "quito": ("Quito", "Pichincha"),
    "guayaquil": ("Guayaquil", "Guayas"),
    "chongon": ("Chongón", "Guayas"),
    "chongón": ("Chongón", "Guayas"),
    "duran": ("Durán", "Guayas"),
    "durán": ("Durán", "Guayas"),
    "daule": ("Daule", "Guayas"),
    "cuenca": ("Cuenca", "Azuay"),
    "ambato": ("Ambato", "Tungurahua"),
    "machala": ("Machala", "El Oro"),
    "esmeraldas": ("Esmeraldas", "Esmeraldas"),
    "echeandia": ("Echeandía", "Bolívar"),
    "echeandía": ("Echeandía", "Bolívar"),
    "guaranda": ("Guaranda", "Bolívar"),
}

CIUDADES_PERU = {
    "lima": ("Lima", "Lima"),
    "san isidro": ("San Isidro", "Lima"),
    "san borja": ("San Borja", "Lima"),
    "santiago de surco": ("Santiago de Surco", "Lima"),
    "surquillo": ("Surquillo", "Lima"),
    "miraflores": ("Miraflores", "Lima"),
    "tacna": ("Tacna", "Tacna"),
}

VALORES_GEOGRAFICOS_INVALIDOS = {
    "",
    "ecuador",
    "peru",
    "perú",
    "teletrabajo",
    "remoto",
    "pichincha",
    "guayas",
    "bolivar",
    "bolívar",
}

PROVINCIAS_ECUADOR = {
    "azuay": "Azuay",
    "bolivar": "Bolívar",
    "canar": "Cañar",
    "carchi": "Carchi",
    "chimborazo": "Chimborazo",
    "cotopaxi": "Cotopaxi",
    "el oro": "El Oro",
    "esmeraldas": "Esmeraldas",
    "galapagos": "Galápagos",
    "guayas": "Guayas",
    "imbabura": "Imbabura",
    "loja": "Loja",
    "los rios": "Los Ríos",
    "manabi": "Manabí",
    "morona santiago": "Morona Santiago",
    "napo": "Napo",
    "orellana": "Orellana",
    "pastaza": "Pastaza",
    "pichincha": "Pichincha",
    "santa elena": "Santa Elena",
    "santo domingo de los tsachilas": "Santo Domingo de los Tsáchilas",
    "sucumbios": "Sucumbíos",
    "tungurahua": "Tungurahua",
    "zamora chinchipe": "Zamora Chinchipe",
}

def limpiar_texto(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()

def normalizar_clave(valor):
    texto = limpiar_texto(valor).lower()

    reemplazos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
    }

    for original, reemplazo in reemplazos.items():
        texto = texto.replace(original, reemplazo)

    return re.sub(r"\s+", " ", texto).strip()


def completar_fecha_publicacion(row):
    fecha_publicacion = limpiar_texto(row.get("fecha_publicacion"))
    fecha_raw = limpiar_texto(row.get("fecha_raw"))

    if fecha_publicacion:
        fecha = pd.to_datetime(fecha_publicacion, errors="coerce")
        if not pd.isna(fecha):
            return fecha.strftime("%Y-%m-%d")

    if fecha_raw:
        fecha = pd.to_datetime(fecha_raw, errors="coerce", dayfirst=True)
        if not pd.isna(fecha):
            return fecha.strftime("%Y-%m-%d")

    return None


def normalizar_geografia(row):
    ciudad_original = limpiar_texto(row.get("ciudad"))
    fuente = normalizar_clave(row.get("fuente"))

    titulo = limpiar_texto(row.get("titulo_oferta"))
    descripcion = limpiar_texto(row.get("descripcion_raw"))

    texto_busqueda = normalizar_clave(
        f"{ciudad_original} {titulo} {descripcion}"
    )

    pais = "Perú" if "_pe" in fuente or "peru" in fuente else "Ecuador"

    catalogo = CIUDADES_PERU if pais == "Perú" else CIUDADES_ECUADOR

    clave_ciudad = normalizar_clave(ciudad_original)

    # Caso 1: el campo viene como "Ciudad, Provincia"
    if "," in ciudad_original:
        partes = [
            parte.strip()
            for parte in ciudad_original.split(",")
            if parte.strip()
        ]

        if partes:
            clave_primera_parte = normalizar_clave(partes[0])

            if clave_primera_parte in catalogo:
                ciudad, provincia = catalogo[clave_primera_parte]
                return pd.Series([ciudad, provincia, pais])

    # Caso 2: ciudad válida sin provincia
    if clave_ciudad in catalogo:
        ciudad, provincia = catalogo[clave_ciudad]
        return pd.Series([ciudad, provincia, pais])

    # Caso 3: valores numéricos como 4,2; 4,4; etc.
    es_numerico = bool(
        re.fullmatch(r"\d+(?:[.,]\d+)?", clave_ciudad)
    )

    # Caso 4: provincia, país o modalidad en lugar de ciudad
    es_invalido = (
        es_numerico
        or clave_ciudad in VALORES_GEOGRAFICOS_INVALIDOS
    )

    # Intentar recuperar la ciudad desde título y descripción
    if es_invalido:
        for clave, (ciudad, provincia) in catalogo.items():
            patron = rf"\b{re.escape(normalizar_clave(clave))}\b"

            if re.search(patron, texto_busqueda):
                return pd.Series([ciudad, provincia, pais])

        # Si no se encontró ciudad, intentar recuperar solo la provincia
        provincia_recuperada = "No especificado"

        if pais == "Ecuador":
            for clave_provincia, nombre_provincia in PROVINCIAS_ECUADOR.items():
                patron_provincia = (
                    rf"\b{re.escape(normalizar_clave(clave_provincia))}\b"
                )

                if re.search(patron_provincia, texto_busqueda):
                    provincia_recuperada = nombre_provincia
                    break

        return pd.Series(
            ["No especificado", provincia_recuperada, pais]
        )

    # Caso 5: valor textual no catalogado
    ciudad_limpia = ciudad_original.title()

    return pd.Series(
        [ciudad_limpia, "No especificado", pais]
    )

def homologar_modalidad(valor):
    texto = limpiar_texto(valor).lower()

    if "remoto" in texto or "desde casa" in texto or "teletrabajo" in texto:
        return "Remoto"

    if "híbrido" in texto or "hibrido" in texto:
        return "Híbrido"

    if (
        "presencial" in texto
        or "tiempo completo" in texto
        or "medio tiempo" in texto
        or "por contrato" in texto
    ):
        return "Presencial"

    return "No especificado"


def inferir_tipo_fuente(fuente):
    fuente = limpiar_texto(fuente).lower()

    if "api" in fuente:
        return "API"

    return "Scraping"


def detectar_tecnologia(titulo, descripcion):
    texto = normalizar_clave(
        f"{limpiar_texto(titulo)} {limpiar_texto(descripcion)}"
    )

    tecnologias = [
        ("Python", [r"\bpython\b"]),
        ("JavaScript", [r"\bjavascript\b", r"\bjquery\b", r"\bjs\b"]),
        ("TypeScript", [r"\btypescript\b"]),
        ("PHP", [r"\bphp\b"]),
        ("Laravel", [r"\blaravel\b"]),
        ("React", [r"\breact(?:\.js)?\b"]),
        ("Vue.js", [r"\bvue(?:\.js)?\b"]),
        ("Angular", [r"\bangular\b"]),
        ("Node.js", [r"\bnode(?:\.js|js)?\b"]),
        ("Java", [r"\bjava\b"]),
        ("C#", [r"(?<!\w)c#(?!\w)", r"\b(?:asp\.)?net\b"]),
        ("SQL", [r"\bsql\b"]),
        ("PostgreSQL", [r"\bpostgresql\b", r"\bpostgres\b"]),
        ("MySQL", [r"\bmysql\b"]),
        ("SQL Server", [r"\bsql server\b"]),
        ("Oracle", [r"\boracle\b"]),
        ("MongoDB", [r"\bmongodb\b"]),
        ("Power BI", [r"\bpower bi\b"]),
        ("Tableau", [r"\btableau\b"]),
        ("Excel", [r"\bexcel\b"]),
        ("Docker", [r"\bdocker\b"]),
        ("Kubernetes", [r"\bkubernetes\b", r"\bk8s\b"]),
        ("AWS", [r"\baws\b", r"amazon web services"]),
        ("Azure", [r"\bazure\b"]),
        ("Git", [r"\bgit\b", r"\bgithub\b"]),
        (
            "API REST",
            [
                r"\bapi rest\b",
                r"\brest api\b",
                r"\bservicios web\b",
                r"\bweb services\b",
            ],
        ),
        ("WordPress", [r"\bwordpress\b"]),
        ("Unity", [r"\bunity\b"]),
        (
            "Inteligencia Artificial",
            [
                r"\binteligencia artificial\b",
                r"\bmachine learning\b",
                r"\baprendizaje automatico\b",
                r"\bia\b",
            ],
        ),
        ("PLC", [r"\bplc\b", r"\bhmi\b"]),
        ("CCTV", [r"\bcctv\b", r"\bdvr\b", r"\bnvr\b"]),
        ("Civil 3D", [r"\bcivil 3d\b"]),
        ("CAD", [r"\bcad\b", r"\bautocad\b"]),
        ("ERP", [r"\berp\b"]),
        ("Hardware", [r"\bhardware\b", r"\bhadware\b"]),
        (
            "Redes",
            [
                r"\bredes\b",
                r"\bnetwork(?:ing)?\b",
                r"\btelecomunicaciones\b",
                r"\bfibra optica\b",
            ],
        ),
        ("Linux", [r"\blinux\b"]),
        ("Cisco", [r"\bcisco\b"]),
        ("SAP", [r"\bsap\b"]),
        ("Scrum", [r"\bscrum\b"]),
        ("Jenkins", [r"\bjenkins\b"]),
    ]

    for tecnologia, patrones in tecnologias:
        if any(re.search(patron, texto) for patron in patrones):
            return tecnologia

    return "No especificado"


def categorizar_tecnologia(tecnologia):
    categorias = {
        "Python": "Lenguaje",
        "JavaScript": "Lenguaje",
        "TypeScript": "Lenguaje",
        "PHP": "Lenguaje",
        "Java": "Lenguaje",
        "C#": "Lenguaje",

        "Laravel": "Framework",
        "React": "Framework",
        "Vue.js": "Framework",
        "Angular": "Framework",
        "Node.js": "Framework",

        "SQL": "Base de Datos",
        "PostgreSQL": "Base de Datos",
        "MySQL": "Base de Datos",
        "SQL Server": "Base de Datos",
        "Oracle": "Base de Datos",
        "MongoDB": "Base de Datos",

        "Power BI": "BI",
        "Tableau": "BI",
        "Excel": "Herramienta",
        "Git": "Herramienta",
        "WordPress": "CMS",
        "Unity": "Desarrollo / Motor",

        "Docker": "DevOps",
        "Kubernetes": "DevOps",
        "Jenkins": "DevOps",

        "AWS": "Cloud",
        "Azure": "Cloud",

        "API REST": "Integración",
        "Inteligencia Artificial": "IA",
        "PLC": "Automatización",
        "CCTV": "Seguridad Electrónica",
        "Civil 3D": "Diseño / CAD",
        "CAD": "Diseño / CAD",
        "ERP": "Software Empresarial",
        "Hardware": "Infraestructura",
        "Redes": "Infraestructura",
        "Linux": "Sistema Operativo",
        "Cisco": "Redes",
        "SAP": "Software Empresarial",
        "Scrum": "Metodología",
    }

    return categorias.get(tecnologia, "No especificado")


def extraer_experiencia(titulo, descripcion):
    texto = f"{limpiar_texto(titulo)} {limpiar_texto(descripcion)}".lower()

    patron = r"(\d+)\s*(años|año|anos|ano)"
    coincidencia = re.search(patron, texto)

    if coincidencia:
        return int(coincidencia.group(1))

    return None

def homologar_rol(titulo, descripcion):
    texto = normalizar_clave(
        f"{limpiar_texto(titulo)} {limpiar_texto(descripcion)}"
    )

    reglas = [
        (
            [
                r"\bqa\b",
                r"\btesting\b",
                r"\btester\b",
                r"calidad de software",
                r"control de calidad de software",
            ],
            "QA / Testing",
            "QA / Testing",
        ),
        (
            [
                r"data analyst",
                r"analista de datos",
                r"business intelligence",
                r"\bbi\b",
                r"power bi",
                r"ciencia de datos",
                r"data science",
                r"ingeniero de datos",
            ],
            "Analista de Datos / BI",
            "Data / BI",
        ),
        (
            [
                r"frontend",
                r"front end",
                r"desarrollador web",
                r"developer web",
                r"wordpress",
            ],
            "Desarrollador Frontend",
            "Frontend",
        ),
        (
            [
                r"backend",
                r"back end",
                r"php",
                r"laravel",
                r"java",
                r"\.net",
                r"node\.?js",
            ],
            "Desarrollador Backend",
            "Backend",
        ),
        (
            [
                r"full stack",
                r"fullstack",
            ],
            "Desarrollador Full Stack",
            "Desarrollo de Software",
        ),
        (
            [
                r"arquitecto de software",
                r"software architect",
            ],
            "Arquitecto de Software",
            "Desarrollo de Software",
        ),
        (
            [
                r"analista de sistemas",
                r"software analyst",
                r"analista programador",
            ],
            "Analista de Sistemas",
            "Desarrollo de Software",
        ),
        (
            [
                r"pasante",
                r"practicante",
                r"pasantia",
            ],
            "Pasante TI",
            "Formación",
        ),
        (
            [
                r"desarrollador de software",
                r"desarrollador software",
                r"ingeniero de software",
                r"programador",
                r"developer",
                r"desarrollo de software",
            ],
            "Desarrollador de Software",
            "Desarrollo de Software",
        ),
        (
            [
                r"devops",
                r"cloud",
                r"aws",
                r"azure",
                r"kubernetes",
                r"docker",
                r"infraestructura",
            ],
            "DevOps / Cloud",
            "Infraestructura",
        ),
        (
            [
                r"ciberseguridad",
                r"seguridad informatica",
                r"seguridad de la informacion",
                r"seguridad electronica",
            ],
            "Ciberseguridad",
            "Seguridad",
        ),
        (
            [
                r"soporte tecnico",
                r"support",
                r"help desk",
                r"mesa de ayuda",
                r"mantenimiento de software",
                r"mantenimiento de hardware",
            ],
            "Soporte Técnico",
            "Soporte Técnico",
        ),
        (
            [
                r"project manager",
                r"jefe de proyecto",
                r"gestor de proyectos",
                r"coordinador de proyectos",
            ],
            "Gestor de Proyectos TI",
            "Gestión de Proyectos",
        ),
        (
            [
                r"docente",
                r"profesor",
                r"instructor",
            ],
            "Docente TI",
            "Educación",
        ),
        (
            [
                r"comercial",
                r"ventas",
                r"vendedor",
                r"asesor comercial",
                r"ejecutivo comercial",
                r"sales",
            ],
            "Comercial de Tecnología",
            "Comercial",
        ),
        (
            [
                r"arquitecto software",
                r"arquitecto de software",
                r"superintendente de aplicaciones",
            ],
            "Arquitecto de Software",
            "Desarrollo de Software",
        ),
        (
            [
                r"itsm",
                r"platform engineer",
                r"plataforma ims",
                r"redes",
                r"network",
            ],
            "Infraestructura TI",
            "Infraestructura",
        ),
        (
            [
                r"hardware",
                r"software y hardware",
                r"reparar placas",
                r"laptop",
                r"impresora",
            ],
            "Soporte Técnico",
            "Soporte Técnico",
        ),
        (
            [
                r"analista de tics",
                r"analista tic",
            ],
            "Analista de Sistemas",
            "Desarrollo de Software",
        ),
        (
            [
                r"desarrollador de nuevos negocios",
            ],
            "Comercial de Tecnología",
            "Comercial",
        ),
    ]

    for patrones, nombre_rol, categoria_rol in reglas:
        for patron in patrones:
            if re.search(patron, texto):
                return pd.Series([nombre_rol, categoria_rol])

    return pd.Series(["Otros", "Otros"])

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    # Completar fechas faltantes usando fecha_raw
    df["fecha_publicacion"] = df.apply(completar_fecha_publicacion, axis=1)

    df[
        [
            "ciudad_limpia",
            "provincia",
            "pais",
        ]
    ] = df.apply(
        normalizar_geografia,
        axis=1,
    )

    df[
        [
            "nombre_rol",
            "categoria_rol",
        ]
    ] = df.apply(
        lambda row: homologar_rol(
            row.get("titulo_oferta"),
            row.get("descripcion_raw"),
        ),
        axis=1,
    )

    df["modalidad"] = df["modalidad_raw"].apply(homologar_modalidad)

    df["nombre_tecnologia"] = df.apply(
        lambda row: detectar_tecnologia(row.get("titulo_oferta"), row.get("descripcion_raw")),
        axis=1,
    )

    df["categoria_tecnologia"] = df["nombre_tecnologia"].apply(categorizar_tecnologia)

    df["tipo_fuente"] = df["fuente"].apply(inferir_tipo_fuente)

    df["num_vacantes"] = 1

    df["experiencia_anios"] = df.apply(
        lambda row: extraer_experiencia(row.get("titulo_oferta"), row.get("descripcion_raw")),
        axis=1,
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("=" * 70)
    print("STAGING ENRIQUECIDO PARA DATA WAREHOUSE")
    print("=" * 70)
    print(f"Archivo origen: {INPUT_FILE}")
    print(f"Archivo generado: {OUTPUT_FILE}")
    print(f"Registros procesados: {len(df)}")

    fechas_invalidas = pd.to_datetime(df["fecha_publicacion"], errors="coerce").isna().sum()
    print(f"Fechas inválidas pendientes: {fechas_invalidas}")

    print()
    print("Columnas generadas:")
    nuevas_columnas = [
        "ciudad_limpia",
        "provincia",
        "pais",
        "nombre_rol",
        "modalidad",
        "nombre_tecnologia",
        "categoria_tecnologia",
        "tipo_fuente",
        "num_vacantes",
        "experiencia_anios",
    ]

    for columna in nuevas_columnas:
        print(f"- {columna}")

    print()
    print("Vista previa:")
    print(
        df[
            [
                "titulo_oferta",
                "fecha_publicacion",
                "ciudad_limpia",
                "provincia",
                "pais",
                "modalidad",
                "nombre_tecnologia",
                "categoria_tecnologia",
                "categoria_rol",
                "salario_usd",
                "num_vacantes",
                "experiencia_anios",
            ]
        ].head(10)
    )

    print()
    print("Registros con fecha inválida:")
    fechas = pd.to_datetime(df["fecha_publicacion"], errors="coerce")
    print(
        df[fechas.isna()][
            [
                "titulo_oferta",
                "empresa",
                "fecha_raw",
                "fecha_publicacion",
                "fuente",
            ]
        ]
    )

    print()
    print("RESUMEN GEOGRÁFICO NORMALIZADO")
    print(
        df[
            [
                "ciudad",
                "ciudad_limpia",
                "provincia",
                "pais",
            ]
        ]
        .value_counts()
        .to_string()
    )

    print()
    print("REGISTROS QUE SIGUEN SIN CIUDAD")
    print(
        df[
            df["ciudad_limpia"] == "No especificado"
        ][
            [
                "titulo_oferta",
                "ciudad",
                "fuente",
            ]
        ].to_string(index=False)
    )

    print()
    print("RESUMEN DE ROLES HOMOLOGADOS")
    print(
        df[
            [
                "nombre_rol",
                "categoria_rol",
            ]
        ]
        .value_counts()
        .to_string()
    )

    print()
    print(f"Roles únicos homologados: {df['nombre_rol'].nunique()}")

    print()
    print("REGISTROS CLASIFICADOS COMO OTROS")
    print(
        df[df["nombre_rol"] == "Otros"][
            [
                "titulo_oferta",
                "fuente",
                "categoria_rol",
            ]
        ].to_string(index=False)
    )

    print()
    print("RESUMEN DE TECNOLOGÍAS DETECTADAS")
    print(
        df[
            [
                "nombre_tecnologia",
                "categoria_tecnologia",
            ]
        ]
        .value_counts()
        .to_string()
    )

    print()
    print(f"Tecnologías únicas detectadas: {df['nombre_tecnologia'].nunique()}")

    print()

    sin_tecnologia = df[
        df["nombre_tecnologia"] == "No especificado"
    ][
        [
            "titulo_oferta",
            "descripcion_raw",
            "fuente",
        ]
    ]

    archivo_sin_tecnologia = (
        BASE_DIR
        / "data"
        / "quality"
        / "ofertas_sin_tecnologia.csv"
    )

    archivo_sin_tecnologia.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    sin_tecnologia.to_csv(
        archivo_sin_tecnologia,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"Registros sin tecnología: {len(sin_tecnologia)}")
    print(f"Detalle generado en: {archivo_sin_tecnologia}")

if __name__ == "__main__":
    main()