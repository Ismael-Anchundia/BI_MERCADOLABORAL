CREATE DATABASE bi_ofertas_dw;
-- ============================================================
-- ENTREGABLE 4 - DATA WAREHOUSE
-- Proyecto: Análisis de ofertas laborales tecnológicas
-- Motor: PostgreSQL
-- ============================================================

DROP SCHEMA IF EXISTS dw_ofertas CASCADE;
CREATE SCHEMA dw_ofertas;

SET search_path TO dw_ofertas;

-- ============================================================
-- DIMENSIÓN TIEMPO
-- ============================================================

CREATE TABLE dim_tiempo (
    id_tiempo INT PRIMARY KEY,
    fecha DATE NOT NULL,
    dia INT NOT NULL CHECK (dia BETWEEN 1 AND 31),
    mes INT NOT NULL CHECK (mes BETWEEN 1 AND 12),
    trimestre INT NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    anio INT NOT NULL
);

-- ============================================================
-- DIMENSIÓN FUENTE
-- ============================================================

CREATE TABLE dim_fuente (
    id_fuente SERIAL PRIMARY KEY,
    nombre_fuente VARCHAR(100) NOT NULL UNIQUE,
    tipo_fuente VARCHAR(50) NOT NULL
);

-- ============================================================
-- DIMENSIÓN CIUDAD
-- ============================================================

CREATE TABLE dim_ciudad (
    id_ciudad SERIAL PRIMARY KEY,
    ciudad VARCHAR(100) NOT NULL,
    provincia VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    CONSTRAINT uq_dim_ciudad UNIQUE (ciudad, provincia, pais)
);

-- ============================================================
-- DIMENSIÓN ROL
-- ============================================================

CREATE TABLE dim_rol (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(100) NOT NULL UNIQUE,
    categoria_rol VARCHAR(50) NOT NULL
);

-- ============================================================
-- DIMENSIÓN MODALIDAD
-- ============================================================

CREATE TABLE dim_modalidad (
    id_modalidad SERIAL PRIMARY KEY,
    modalidad VARCHAR(20) NOT NULL UNIQUE
);

-- ============================================================
-- DIMENSIÓN TECNOLOGÍA
-- ============================================================

CREATE TABLE dim_tecnologia (
    id_tecnologia SERIAL PRIMARY KEY,
    nombre_tecnologia VARCHAR(100) NOT NULL UNIQUE,
    categoria_tecnologia VARCHAR(50) NOT NULL
);

-- ============================================================
-- TABLA DE HECHOS
-- ============================================================

CREATE TABLE fact_ofertas_laborales (
    id_hecho SERIAL PRIMARY KEY,

    id_tiempo INT NOT NULL,
    id_fuente INT NOT NULL,
    id_ciudad INT NOT NULL,
    id_rol INT NOT NULL,
    id_modalidad INT NOT NULL,
    id_tecnologia INT NOT NULL,

    salario_usd DECIMAL(10,2) CHECK (salario_usd >= 0),
    num_vacantes INT NOT NULL DEFAULT 1 CHECK (num_vacantes >= 1),
    experiencia_anios INT CHECK (experiencia_anios >= 0),

    CONSTRAINT fk_fact_tiempo
        FOREIGN KEY (id_tiempo)
        REFERENCES dim_tiempo(id_tiempo),

    CONSTRAINT fk_fact_fuente
        FOREIGN KEY (id_fuente)
        REFERENCES dim_fuente(id_fuente),

    CONSTRAINT fk_fact_ciudad
        FOREIGN KEY (id_ciudad)
        REFERENCES dim_ciudad(id_ciudad),

    CONSTRAINT fk_fact_rol
        FOREIGN KEY (id_rol)
        REFERENCES dim_rol(id_rol),

    CONSTRAINT fk_fact_modalidad
        FOREIGN KEY (id_modalidad)
        REFERENCES dim_modalidad(id_modalidad),

    CONSTRAINT fk_fact_tecnologia
        FOREIGN KEY (id_tecnologia)
        REFERENCES dim_tecnologia(id_tecnologia)
);

-- ============================================================
-- ÍNDICES PARA CONSULTAS ANALÍTICAS
-- ============================================================

CREATE INDEX idx_fact_tiempo ON fact_ofertas_laborales(id_tiempo);
CREATE INDEX idx_fact_fuente ON fact_ofertas_laborales(id_fuente);
CREATE INDEX idx_fact_ciudad ON fact_ofertas_laborales(id_ciudad);
CREATE INDEX idx_fact_rol ON fact_ofertas_laborales(id_rol);
CREATE INDEX idx_fact_modalidad ON fact_ofertas_laborales(id_modalidad);
CREATE INDEX idx_fact_tecnologia ON fact_ofertas_laborales(id_tecnologia);