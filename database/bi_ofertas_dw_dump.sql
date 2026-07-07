--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: dw_ofertas; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA dw_ofertas;


ALTER SCHEMA dw_ofertas OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dim_ciudad; Type: TABLE; Schema: dw_ofertas; Owner: postgres
--

CREATE TABLE dw_ofertas.dim_ciudad (
    id_ciudad integer NOT NULL,
    ciudad character varying(200) NOT NULL,
    provincia character varying(200) NOT NULL,
    pais character varying(100) NOT NULL
);


ALTER TABLE dw_ofertas.dim_ciudad OWNER TO postgres;

--
-- Name: dim_ciudad_id_ciudad_seq; Type: SEQUENCE; Schema: dw_ofertas; Owner: postgres
--

CREATE SEQUENCE dw_ofertas.dim_ciudad_id_ciudad_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dw_ofertas.dim_ciudad_id_ciudad_seq OWNER TO postgres;

--
-- Name: dim_ciudad_id_ciudad_seq; Type: SEQUENCE OWNED BY; Schema: dw_ofertas; Owner: postgres
--

ALTER SEQUENCE dw_ofertas.dim_ciudad_id_ciudad_seq OWNED BY dw_ofertas.dim_ciudad.id_ciudad;


--
-- Name: dim_fuente; Type: TABLE; Schema: dw_ofertas; Owner: postgres
--

CREATE TABLE dw_ofertas.dim_fuente (
    id_fuente integer NOT NULL,
    nombre_fuente character varying(100) NOT NULL,
    tipo_fuente character varying(50) NOT NULL
);


ALTER TABLE dw_ofertas.dim_fuente OWNER TO postgres;

--
-- Name: dim_fuente_id_fuente_seq; Type: SEQUENCE; Schema: dw_ofertas; Owner: postgres
--

CREATE SEQUENCE dw_ofertas.dim_fuente_id_fuente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dw_ofertas.dim_fuente_id_fuente_seq OWNER TO postgres;

--
-- Name: dim_fuente_id_fuente_seq; Type: SEQUENCE OWNED BY; Schema: dw_ofertas; Owner: postgres
--

ALTER SEQUENCE dw_ofertas.dim_fuente_id_fuente_seq OWNED BY dw_ofertas.dim_fuente.id_fuente;


--
-- Name: dim_modalidad; Type: TABLE; Schema: dw_ofertas; Owner: postgres
--

CREATE TABLE dw_ofertas.dim_modalidad (
    id_modalidad integer NOT NULL,
    modalidad character varying(20) NOT NULL
);


ALTER TABLE dw_ofertas.dim_modalidad OWNER TO postgres;

--
-- Name: dim_modalidad_id_modalidad_seq; Type: SEQUENCE; Schema: dw_ofertas; Owner: postgres
--

CREATE SEQUENCE dw_ofertas.dim_modalidad_id_modalidad_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dw_ofertas.dim_modalidad_id_modalidad_seq OWNER TO postgres;

--
-- Name: dim_modalidad_id_modalidad_seq; Type: SEQUENCE OWNED BY; Schema: dw_ofertas; Owner: postgres
--

ALTER SEQUENCE dw_ofertas.dim_modalidad_id_modalidad_seq OWNED BY dw_ofertas.dim_modalidad.id_modalidad;


--
-- Name: dim_rol; Type: TABLE; Schema: dw_ofertas; Owner: postgres
--

CREATE TABLE dw_ofertas.dim_rol (
    id_rol integer NOT NULL,
    nombre_rol character varying(500) NOT NULL,
    categoria_rol character varying(50) NOT NULL
);


ALTER TABLE dw_ofertas.dim_rol OWNER TO postgres;

--
-- Name: dim_rol_id_rol_seq; Type: SEQUENCE; Schema: dw_ofertas; Owner: postgres
--

CREATE SEQUENCE dw_ofertas.dim_rol_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dw_ofertas.dim_rol_id_rol_seq OWNER TO postgres;

--
-- Name: dim_rol_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: dw_ofertas; Owner: postgres
--

ALTER SEQUENCE dw_ofertas.dim_rol_id_rol_seq OWNED BY dw_ofertas.dim_rol.id_rol;


--
-- Name: dim_tecnologia; Type: TABLE; Schema: dw_ofertas; Owner: postgres
--

CREATE TABLE dw_ofertas.dim_tecnologia (
    id_tecnologia integer NOT NULL,
    nombre_tecnologia character varying(200) NOT NULL,
    categoria_tecnologia character varying(50) NOT NULL
);


ALTER TABLE dw_ofertas.dim_tecnologia OWNER TO postgres;

--
-- Name: dim_tecnologia_id_tecnologia_seq; Type: SEQUENCE; Schema: dw_ofertas; Owner: postgres
--

CREATE SEQUENCE dw_ofertas.dim_tecnologia_id_tecnologia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dw_ofertas.dim_tecnologia_id_tecnologia_seq OWNER TO postgres;

--
-- Name: dim_tecnologia_id_tecnologia_seq; Type: SEQUENCE OWNED BY; Schema: dw_ofertas; Owner: postgres
--

ALTER SEQUENCE dw_ofertas.dim_tecnologia_id_tecnologia_seq OWNED BY dw_ofertas.dim_tecnologia.id_tecnologia;


--
-- Name: dim_tiempo; Type: TABLE; Schema: dw_ofertas; Owner: postgres
--

CREATE TABLE dw_ofertas.dim_tiempo (
    id_tiempo integer NOT NULL,
    fecha date NOT NULL,
    dia integer NOT NULL,
    mes integer NOT NULL,
    trimestre integer NOT NULL,
    anio integer NOT NULL,
    CONSTRAINT dim_tiempo_dia_check CHECK (((dia >= 1) AND (dia <= 31))),
    CONSTRAINT dim_tiempo_mes_check CHECK (((mes >= 1) AND (mes <= 12))),
    CONSTRAINT dim_tiempo_trimestre_check CHECK (((trimestre >= 1) AND (trimestre <= 4)))
);


ALTER TABLE dw_ofertas.dim_tiempo OWNER TO postgres;

--
-- Name: fact_ofertas_laborales; Type: TABLE; Schema: dw_ofertas; Owner: postgres
--

CREATE TABLE dw_ofertas.fact_ofertas_laborales (
    id_hecho integer NOT NULL,
    id_tiempo integer NOT NULL,
    id_fuente integer NOT NULL,
    id_ciudad integer NOT NULL,
    id_rol integer NOT NULL,
    id_modalidad integer NOT NULL,
    id_tecnologia integer NOT NULL,
    salario_usd numeric(10,2),
    num_vacantes integer DEFAULT 1 NOT NULL,
    experiencia_anios integer,
    CONSTRAINT fact_ofertas_laborales_experiencia_anios_check CHECK ((experiencia_anios >= 0)),
    CONSTRAINT fact_ofertas_laborales_num_vacantes_check CHECK ((num_vacantes >= 1)),
    CONSTRAINT fact_ofertas_laborales_salario_usd_check CHECK ((salario_usd >= (0)::numeric))
);


ALTER TABLE dw_ofertas.fact_ofertas_laborales OWNER TO postgres;

--
-- Name: fact_ofertas_laborales_id_hecho_seq; Type: SEQUENCE; Schema: dw_ofertas; Owner: postgres
--

CREATE SEQUENCE dw_ofertas.fact_ofertas_laborales_id_hecho_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dw_ofertas.fact_ofertas_laborales_id_hecho_seq OWNER TO postgres;

--
-- Name: fact_ofertas_laborales_id_hecho_seq; Type: SEQUENCE OWNED BY; Schema: dw_ofertas; Owner: postgres
--

ALTER SEQUENCE dw_ofertas.fact_ofertas_laborales_id_hecho_seq OWNED BY dw_ofertas.fact_ofertas_laborales.id_hecho;


--
-- Name: vw_kpi_crecimiento_mensual; Type: VIEW; Schema: dw_ofertas; Owner: postgres
--

CREATE VIEW dw_ofertas.vw_kpi_crecimiento_mensual AS
 WITH ofertas_mensuales AS (
         SELECT dt.anio,
            dt.mes,
            count(fo.id_hecho) AS total_ofertas
           FROM ((dw_ofertas.fact_ofertas_laborales fo
             JOIN dw_ofertas.dim_tiempo dt ON ((fo.id_tiempo = dt.id_tiempo)))
             JOIN dw_ofertas.dim_ciudad dc ON ((fo.id_ciudad = dc.id_ciudad)))
          WHERE ((dc.pais)::text = 'Ecuador'::text)
          GROUP BY dt.anio, dt.mes
        ), calculo_crecimiento AS (
         SELECT ofertas_mensuales.anio,
            ofertas_mensuales.mes,
            ofertas_mensuales.total_ofertas,
            lag(ofertas_mensuales.total_ofertas) OVER (ORDER BY ofertas_mensuales.anio, ofertas_mensuales.mes) AS ofertas_mes_anterior
           FROM ofertas_mensuales
        )
 SELECT anio,
    mes,
    total_ofertas,
    ofertas_mes_anterior,
        CASE
            WHEN (ofertas_mes_anterior IS NULL) THEN NULL::numeric
            WHEN (ofertas_mes_anterior = 0) THEN NULL::numeric
            ELSE round(((((total_ofertas - ofertas_mes_anterior))::numeric * 100.0) / (ofertas_mes_anterior)::numeric), 2)
        END AS porcentaje_crecimiento
   FROM calculo_crecimiento
  ORDER BY anio, mes;


ALTER VIEW dw_ofertas.vw_kpi_crecimiento_mensual OWNER TO postgres;

--
-- Name: vw_kpi_modalidad; Type: VIEW; Schema: dw_ofertas; Owner: postgres
--

CREATE VIEW dw_ofertas.vw_kpi_modalidad AS
 SELECT dm.modalidad,
    count(fo.id_hecho) AS total_ofertas,
    round((((count(fo.id_hecho))::numeric * 100.0) / sum(count(fo.id_hecho)) OVER ()), 2) AS porcentaje
   FROM ((dw_ofertas.fact_ofertas_laborales fo
     JOIN dw_ofertas.dim_modalidad dm ON ((fo.id_modalidad = dm.id_modalidad)))
     JOIN dw_ofertas.dim_ciudad dc ON ((fo.id_ciudad = dc.id_ciudad)))
  WHERE ((dc.pais)::text = 'Ecuador'::text)
  GROUP BY dm.modalidad
  ORDER BY (count(fo.id_hecho)) DESC;


ALTER VIEW dw_ofertas.vw_kpi_modalidad OWNER TO postgres;

--
-- Name: vw_kpi_participacion_ciudades; Type: VIEW; Schema: dw_ofertas; Owner: postgres
--

CREATE VIEW dw_ofertas.vw_kpi_participacion_ciudades AS
 SELECT dc.ciudad,
    dc.provincia,
    dc.pais,
    count(fo.id_hecho) AS total_ofertas,
    round((((count(fo.id_hecho))::numeric * 100.0) / sum(count(fo.id_hecho)) OVER ()), 2) AS porcentaje_participacion
   FROM (dw_ofertas.fact_ofertas_laborales fo
     JOIN dw_ofertas.dim_ciudad dc ON ((fo.id_ciudad = dc.id_ciudad)))
  WHERE ((dc.pais)::text = 'Ecuador'::text)
  GROUP BY dc.ciudad, dc.provincia, dc.pais
  ORDER BY (count(fo.id_hecho)) DESC;


ALTER VIEW dw_ofertas.vw_kpi_participacion_ciudades OWNER TO postgres;

--
-- Name: vw_kpi_participacion_tecnologias; Type: VIEW; Schema: dw_ofertas; Owner: postgres
--

CREATE VIEW dw_ofertas.vw_kpi_participacion_tecnologias AS
 SELECT dtec.nombre_tecnologia,
    dtec.categoria_tecnologia,
    count(fo.id_hecho) AS total_menciones,
    round((((count(fo.id_hecho))::numeric * 100.0) / sum(count(fo.id_hecho)) OVER ()), 2) AS porcentaje_participacion
   FROM ((dw_ofertas.fact_ofertas_laborales fo
     JOIN dw_ofertas.dim_tecnologia dtec ON ((fo.id_tecnologia = dtec.id_tecnologia)))
     JOIN dw_ofertas.dim_ciudad dc ON ((fo.id_ciudad = dc.id_ciudad)))
  WHERE ((dc.pais)::text = 'Ecuador'::text)
  GROUP BY dtec.nombre_tecnologia, dtec.categoria_tecnologia
  ORDER BY (count(fo.id_hecho)) DESC;


ALTER VIEW dw_ofertas.vw_kpi_participacion_tecnologias OWNER TO postgres;

--
-- Name: vw_kpi_salario_promedio_rol; Type: VIEW; Schema: dw_ofertas; Owner: postgres
--

CREATE VIEW dw_ofertas.vw_kpi_salario_promedio_rol AS
 SELECT dr.categoria_rol,
    count(fo.id_hecho) AS total_ofertas_con_salario,
    round(avg(fo.salario_usd), 2) AS salario_promedio_usd,
    round(min(fo.salario_usd), 2) AS salario_minimo_usd,
    round(max(fo.salario_usd), 2) AS salario_maximo_usd
   FROM ((dw_ofertas.fact_ofertas_laborales fo
     JOIN dw_ofertas.dim_rol dr ON ((fo.id_rol = dr.id_rol)))
     JOIN dw_ofertas.dim_ciudad dc ON ((fo.id_ciudad = dc.id_ciudad)))
  WHERE ((fo.salario_usd IS NOT NULL) AND ((dc.pais)::text = 'Ecuador'::text))
  GROUP BY dr.categoria_rol
  ORDER BY (round(avg(fo.salario_usd), 2)) DESC;


ALTER VIEW dw_ofertas.vw_kpi_salario_promedio_rol OWNER TO postgres;

--
-- Name: dim_ciudad id_ciudad; Type: DEFAULT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_ciudad ALTER COLUMN id_ciudad SET DEFAULT nextval('dw_ofertas.dim_ciudad_id_ciudad_seq'::regclass);


--
-- Name: dim_fuente id_fuente; Type: DEFAULT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_fuente ALTER COLUMN id_fuente SET DEFAULT nextval('dw_ofertas.dim_fuente_id_fuente_seq'::regclass);


--
-- Name: dim_modalidad id_modalidad; Type: DEFAULT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_modalidad ALTER COLUMN id_modalidad SET DEFAULT nextval('dw_ofertas.dim_modalidad_id_modalidad_seq'::regclass);


--
-- Name: dim_rol id_rol; Type: DEFAULT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_rol ALTER COLUMN id_rol SET DEFAULT nextval('dw_ofertas.dim_rol_id_rol_seq'::regclass);


--
-- Name: dim_tecnologia id_tecnologia; Type: DEFAULT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_tecnologia ALTER COLUMN id_tecnologia SET DEFAULT nextval('dw_ofertas.dim_tecnologia_id_tecnologia_seq'::regclass);


--
-- Name: fact_ofertas_laborales id_hecho; Type: DEFAULT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.fact_ofertas_laborales ALTER COLUMN id_hecho SET DEFAULT nextval('dw_ofertas.fact_ofertas_laborales_id_hecho_seq'::regclass);


--
-- Data for Name: dim_ciudad; Type: TABLE DATA; Schema: dw_ofertas; Owner: postgres
--

INSERT INTO dw_ofertas.dim_ciudad VALUES (1, 'Quito', 'Pichincha', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (2, '4', '2', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (3, '4', '4', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (4, 'Guayaquil', 'Guayas', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (5, '4', '5', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (6, 'Ambato', 'Tungurahua', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (7, 'San Isidro', 'Lima', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (8, 'Tacna', 'Tacna', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (9, 'San Borja', 'Lima', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (10, 'Lima', 'Lima', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (11, '4', '4', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (12, 'Santiago De Surco', 'Lima', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (13, 'Surquillo', 'Lima', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (14, '4', '6', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (15, '4', '1', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (16, '4', '7', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (17, 'Miraflores', 'Lima', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (18, '4', '3', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (19, '4', '2', 'Perú');
INSERT INTO dw_ofertas.dim_ciudad VALUES (20, 'Guayaquil', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (21, 'Quito', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (22, 'Pichincha', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (23, 'Chongon', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (24, 'Durán', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (25, 'Esmeraldas', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (26, 'Ecuador', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (27, 'Bolívar', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (28, 'Cuenca', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (29, 'Teletrabajo', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (30, 'Guayas', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (31, 'Duran', 'No especificado', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (32, 'Echeandía', 'Bolívar', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (33, 'Machala', 'El Oro', 'Ecuador');
INSERT INTO dw_ofertas.dim_ciudad VALUES (34, 'Cuenca', 'Azuay', 'Ecuador');


--
-- Data for Name: dim_fuente; Type: TABLE DATA; Schema: dw_ofertas; Owner: postgres
--

INSERT INTO dw_ofertas.dim_fuente VALUES (1, 'computrabajo_ec', 'Scraping');
INSERT INTO dw_ofertas.dim_fuente VALUES (2, 'computrabajo_pe', 'Scraping');
INSERT INTO dw_ofertas.dim_fuente VALUES (3, 'trabajosdiarios', 'Scraping');
INSERT INTO dw_ofertas.dim_fuente VALUES (4, 'unmejorempleo', 'Scraping');
INSERT INTO dw_ofertas.dim_fuente VALUES (5, 'multitrabajos', 'Scraping');


--
-- Data for Name: dim_modalidad; Type: TABLE DATA; Schema: dw_ofertas; Owner: postgres
--

INSERT INTO dw_ofertas.dim_modalidad VALUES (1, 'No especificado');
INSERT INTO dw_ofertas.dim_modalidad VALUES (2, 'Presencial');
INSERT INTO dw_ofertas.dim_modalidad VALUES (3, 'Remoto');
INSERT INTO dw_ofertas.dim_modalidad VALUES (4, 'Híbrido');


--
-- Data for Name: dim_rol; Type: TABLE DATA; Schema: dw_ofertas; Owner: postgres
--

INSERT INTO dw_ofertas.dim_rol VALUES (1, 'Desarrollador De Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (2, 'Ejecutivo Comercial', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (3, 'Desarrollador Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (4, 'Ejecutivo Comercial De Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (5, 'Pasante De Desarrollo De Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (6, 'Asesor Comercial Erp / Vendedor De Software Contable', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (7, 'Asesor Comercial', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (8, 'Asesor De Equipos De Tecnologia: Pc, Laptops, Impresoras, Ploters, Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (9, 'Auxiliar Contable', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (10, 'Ejecutiva Comercial B2B – Soluciones De Telecomunicaciones', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (11, 'Arquitecto De Acabados Y Coordinacion De Proyectos', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (12, 'Analista De Tienda', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (13, 'Asistente Técnico De Diseño Y Producción', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (14, 'B2B Sales Representative', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (15, 'Consultor(A) Freelance De Marca Personal Y Posicionamiento B2B (Remoto)', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (16, 'Agente Call Center', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (17, 'Filmmaker Y Editor De Video Junior Quito', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (18, 'Operational Support Agent (Pcd)', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (19, 'Analista Programador(A) – Desarrollo De Software Empresarial / San Isidro', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (20, 'Analista De Calidad De Software Tacna', 'QA / Testing');
INSERT INTO dw_ofertas.dim_rol VALUES (21, 'Asistente De Desarrollo De Software –  San Borja', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (22, 'Software Analyst Lims / Cercado De Lima', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (23, 'Analista De Sistemas/Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (24, 'Analista De Control De Calidad De Software', 'QA / Testing');
INSERT INTO dw_ofertas.dim_rol VALUES (25, 'Analista De Qa', 'QA / Testing');
INSERT INTO dw_ofertas.dim_rol VALUES (26, 'Practicante De Desarrollo De Software (Remoto)', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (27, 'Superintendente De Aplicaciones De Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (28, 'Practicante De Optimización De Datos (Ing. Industrial, Ing. De Software,  Ing. De Sistemas)', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (29, 'Practicante Profesional De Desarrollo De Software Ia', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (30, 'Analista De Calidad De Software', 'QA / Testing');
INSERT INTO dw_ofertas.dim_rol VALUES (31, 'Implementador De Soluciones Itsm', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (32, 'Asistente Técnico De Redes, Software Y Hadware', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (33, 'Docente Pregrado De Software Y Tecnología En La Salud', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (34, 'Customer Service / Galaxy Consultant Samsung Móvil/ Soporte Técnico Software', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (35, 'Ejecutivo Comercial / Venta De Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (36, 'Ejecutivo De Ventas De Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (37, 'Arquitecto Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (38, 'Asistente Comercial', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (39, 'Ejecutivo Comercial / Contac Center Manatel Oferta Laboral: Ejecutivo Comercial. Ubicación: Guayaquil (Norte) Horario: Jornada De Oficina Tiempo Completo O Medio Tiempo Salario: Sueldo Fijo $482 Inicio: Inmediato Descripcion Del Puesto: Buscamos Personas Dinámicas, Con Habilidades Comunicativas Y Orientadas Al Cliente, Para Unirse A Nuestro Equipo... Tiempo Completo Guayaquil, Guayas • 22/05/2026 $482,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (40, 'Asesor/A Comercial De Software Y Tecnología Pacusoft Sas En Pacusoft Buscamos Incorporar A Nuestro Equipo Un/A Asesor/A Comercial Con Iniciativa, Buena Comunicación Y Orientación A Resultados, Para Impulsar La Promoción De Nuestras Soluciones De Software Y Servicios Tecnológicos. Buscamos Una Persona Con Habilidades Comerciales, Facilidad Para Relacionarse Con... Tiempo Completo Quito, Pichincha • 14/05/2026 $550,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (41, 'Asistente Bodega Parabrisas Am Glasses Personal Para Bodega Que Conozca De Logistica E Inventario, Responsable Y Puntual En El Detalle De Su Trabajo, Toma Fisica De Stock Y Registro De Entradas Y Salidas, Uso De Excel O Software, Disponibilidad Inmediata Y Trabajo En Equipo, Sueldo... Tiempo Completo Guayaquil, Guayas • 08/06/2026 $482,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (42, 'Pasantía Laboral / Research And Development Deinsa Global En Deinsa Global Estamos Realizando Un Programa De Pasantía Laboral Para Estudiantes De Alto Desempeño Y Profesionales (Modalidad Virtual), Que Deseen Iniciar Una Carrera Profesional Desempeñando El Puesto De Project Manager En Research & Development. Este Rol Presupone La Realización... Desde Casa Sin Experiencia Pichincha, Pichincha • 29/06/2026', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (43, 'Ventas Sara Ochoa Clínica Ser Humano Se Encuentra En La Búsqueda De Un/A Asesor/A Comercial Digital Para Integrarse A Nuestro Equipo. Requisitos: • Experiencia En Ventas Y Atención Al Cliente. • Manejo De Redes Sociales Y Respuesta A Mensajes. • Conocimientos Básicos De... Tiempo Completo Guayaquil, Guayas • 18/06/2026', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (44, 'Auxiliar Contable Sara Ochoa Oferta Laboral Clínica Ser Humano Se Encuentra En La Búsqueda De Un/A Auxiliar Contable Para Trabajar Medio Tiempo Bajo Modalidad De Servicios Prestados. Requisitos: • Conocimientos En Software Contables. • Experiencia Básica En Procesos Contables Y Administrativos. • Persona Organizada,... Medio Tiempo Guayaquil, Guayas • 18/06/2026', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (45, 'Desarrollador (Parroquia Chongon) Telecom&Net S.A.A Desarrollador De Software / Web Ubicación: Chongón (Presencial) Requisitos: Título En Ingeniería En Software O Ingeniería En Desarrollo De Aplicaciones Web. Conocimientos Sólidos En Html, Css Y Javascript. Experiencia En Wordpress Y Al Menos Un Framework Frontend (React, Vue O... Tiempo Completo Guayaquil, Guayas • 16/06/2026 $700,00 / Mensual', 'Frontend');
INSERT INTO dw_ofertas.dim_rol VALUES (46, 'Asistente Gerencia Administrativa Ventas Gk-Innova Se Requiere Persona Proactiva Con Conocimientos En Áreas Financieras, Administrativas Y Atención Al Cliente, Con La Posibilidad De Viajar, Con Conocimientos De Manejo De Software Administrativo Financiero, Compras Publicas, Realizar Ofertas Seguimiento De Ofertasycotizaciones, Servicio Y Atencion A Clientes, Manejo... Por Contrato Quito, Pichincha • 15/06/2026 $550,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (47, 'Tornero Cnc Worind Componentes Industriales Funciones Principales Interpretación De Planos: Interpretar Planos De Ingeniería Para Entender Las Medidas Y Tolerancias De La Pieza Final. Programación: Introducir O Modificar Códigos Y Parámetros De Mecanizado (Velocidad, Avance, Profundidad) En El Software De La Máquina. Instalar Las Herramientas... Tiempo Completo Durán, Guayas • 12/06/2026', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (48, 'Conductor Licencia C Zetalent Formación: Bachiller. Experiencia De 2 Años En Posiciones Similares. Conocimientos Técnicos En: Equipos Que Se Manejan En La Construcción, Gestión De Inventarios, Logística De Transporte, Manejo De Documentos, Excel O Software Logístico, Conducir Vehículos De 3.5 T. Preferente Experiencia En... Tiempo Completo Quito, Pichincha • 02/06/2026', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (49, 'Operador De Plataformas Autocargables Zetalent Formación: Bachiller. Experiencia De 2 Años En Posiciones Similares. Conocimientos Técnicos En: Equipos Que Se Manejan En La Construcción, Gestión De Inventarios, Logística De Transporte, Manejo De Documentos, Excel O Software Logístico, Conducir Vehículos De 3.5 T. Preferente Experiencia En... Tiempo Completo Quito, Pichincha • 02/06/2026', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (50, 'Tecnico De Seguridad Electronica Especialista En Honeywell Vista Compured Empresa: Compured Ubicación: Guayaquil, Ecuador Modalidad: Presencial / Campo Descripción Del Puesto Buscamos Un Técnico De Seguridad Electrónica De Alto Nivel Con Experiencia Real, Comprobable Y Sólida En La Configuración Avanzada De Sistemas De Intrusión. Experiencia Mínima: 3 A 5... Tiempo Completo Guayaquil, Guayas • 02/06/2026', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (51, 'Asistente De Compras Quito Andicalzado S.A Asistente De Compras Con 3 Años De Experiencia Y Formación Y Conocimientos Educación: Título Técnico O Universitario En Ingeniería Industrial, Administración De Empresas, Comercio Internacional O Carreras Afines. Materiales: Conocimiento Profundo De Cueros, Sintéticos (Pu, Pvc), Suelas (Tpu, Caucho, Pu),... Por Contrato Quito, Pichincha • 02/06/2026 $600,00 / Mensual', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (52, 'Desarrollador De Software Gemeseg Cia Ltda En Gemeseg Buscamos Incorporar Un Profesional En Sistemas O Desarrollo De Software Con Conocimientos En Programación, Automatización E Inteligencia Artificial. Funciones Principales: • Desarrollo E Integración De Automatizaciones Con Ia • Programación De Procesos Y Funciones Automatizadas • Integración De... Tiempo Completo Sin Experiencia Guayaquil, Guayas • 27/05/2026 $800,00 / Mensual', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (53, 'Asesor Comercial Quito Andicalzado S.A ¡Únete A Nuestro Equipo En Andicalzado! Convocatoria Laboral: Asesor Comercial Para: Profesionales Del Área Comercial Y Ventas Tu Próximo Gran Reto Profesional En Andicalzado, Líderes En La Comercialización De Calzado De Alta Calidad Y Distribuidores De Las Reconocidas Botas Westland,... Por Contrato Quito, Pichincha • 26/05/2026 $500,00 / Mensual', 'QA / Testing');
INSERT INTO dw_ofertas.dim_rol VALUES (54, 'Asistente Contable Nova Market Nomarksa Descripción Del Puesto Nos Encontramos En La Búsqueda De Un Asistente Contable Altamente Organizado Y Analítico, Con Sólidos Conocimientos En Procesos Contables Y Financieros. El Candidato Ideal Deberá Garantizar El Adecuado Registro Y Control De Operaciones Contables, Asegurando El Cumplimiento... Por Contrato Guayaquil, Guayas • 18/05/2026 $482,00 / Mensual', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (55, 'Asistente Contable/Sector El Recreo Nova Market Nomarksa Descripción Del Puesto Nos Encontramos En La Búsqueda De Un Asistente Contable Altamente Organizado Y Analítico, Con Sólidos Conocimientos En Procesos Contables Y Financieros. El Candidato Ideal Deberá Garantizar El Adecuado Registro Y Control De Operaciones Contables, Asegurando El Cumplimiento... Tiempo Completo Quito, Pichincha • 18/05/2026 $500,00 / Mensual', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (56, 'Programador De Software Y Soporte Técnico Fisoluciones Estamos En Búsqueda De Un Programador De Software Y Soporte Técnico Para Integrarse A Nuestro Equipo De Desarrollo De Negocio Y Tecnología Informática. La Persona Seleccionada Será Responsable De Apoyar En El Desarrollo, Parametrización Y Soporte Técnico De Los Sistemas... Tiempo Completo Quito, Pichincha • 14/05/2026 $900,00 / Mensual', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (57, 'Practicante De Edición De Video Nebbit Sas ¿Te Apasiona Editar Videos Y Crear Contenido Visual Que Conecte Con Las Personas? En Nebbit Sas Estamos En Búsqueda De Un Practi­Cante De Edición De Video Para Apoyar Al Departamento De Marketing En La Producción De Piezas Audiovisuales Para Redes... Prácticas / Becario Sin Experiencia Quito, Pichincha • 11/05/2026', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (58, 'Soporte Técnico Y Seguimiento De Clientes Implementación Sistemas Gk-Innova Se Requiere Una Persona Proactiva, Que Tenga Disponibilidad De Viajar, Que Sepa Desarrollo En Software Conocimiento En Php, Java, Javascript Base De Datos Postgresql, Con Conocimiento De Software Administrativo, Financiero O Afin, Que Viva Por El Sur Recomendable, Apoyo Para... Tiempo Completo Ciudad De Esmeraldas, Esmeraldas • 10/05/2026 $550,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (59, 'Auxiliar De Soporte Técnico Fisoluciones Actividades: -Revisión De Actividades De Equipo Técnico. -Soporte Técnico -Coordinación Técnica De Cuadrillas Para Instalaciones Y Mantenimientos. -Control De Tickets. Requisitos: -Tecnología O Estudios Universitarios En Sistemas, Redes, Telecomunicaciones O Carreras Afines. -Experiencia Mínima De 1 Año En Soporte Técnico.... Tiempo Completo Quito, Pichincha • 08/05/2026 $500,00 / Mensual', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (60, 'Aaa - Especialista En Proyectos Unity Centro De Ayuda Académica Profesional Convocatoria Nacional – Redactor Académico - Lengua Y Literatura Caap – Centro De Ayuda Académica Profesional, Empresa Líder En El Desarrollo Y Acompañamiento De Proyectos De Investigación Académica En Latinoamérica, Continúa Fortaleciendo Su Equipo De Profesionales Altamente Capacitados Y Comprometidos... Por Contrato Ecuador, Orellana • 04/05/2026', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (61, 'Aaa - Redactor Científico Unity Centro De Ayuda Académica Profesional Convocatoria Nacional – Redactor Académico - Lengua Y Literatura Caap – Centro De Ayuda Académica Profesional, Empresa Líder En El Desarrollo Y Acompañamiento De Proyectos De Investigación Académica En Latinoamérica, Continúa Fortaleciendo Su Equipo De Profesionales Altamente Capacitados Y Comprometidos... Por Contrato Ecuador, Napo • 04/05/2026', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (62, 'Caap - Lengua Y Literatura Con Unity Centro De Ayuda Académica Profesional Convocatoria Nacional – Redactor Académico - Lengua Y Literatura Caap – Centro De Ayuda Académica Profesional, Empresa Líder En El Desarrollo Y Acompañamiento De Proyectos De Investigación Académica En Latinoamérica, Continúa Fortaleciendo Su Equipo De Profesionales Altamente Capacitados Y Comprometidos... Por Contrato Ecuador, Morona Santiago • 04/05/2026', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (63, 'Caap - Desarrollo Académico Unity Centro De Ayuda Académica Profesional Convocatoria Nacional – Redactor Académico - Lengua Y Literatura Caap – Centro De Ayuda Académica Profesional, Empresa Líder En El Desarrollo Y Acompañamiento De Proyectos De Investigación Académica En Latinoamérica, Continúa Fortaleciendo Su Equipo De Profesionales Altamente Capacitados Y Comprometidos... Por Contrato Ecuador, Manabí • 04/05/2026', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (64, 'Asistente Contable / Dpto. Financiero (Femenino) Connetworks Sa Empresa De Telecomunicaciones Busca Asistente Contable Mujer Para Fortalecer Su Equipo Financiero Requisitos: - Título En Contabilidad O Carrera Afín. - Experiencia Mínima De 1 Año En Contabilidad. - Manejo De Facturación Electrónica, Retenciones Y Registros Contables. - Conocimientos En... Tiempo Completo Guayaquil, Guayas • 29/06/2026', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (65, 'Ejecutivo Call Center Con O Sin Experiencia Socace S.A. Compañía Enfocada En La Distribución Y Promoción De Servicios, Se Encuentra Contratando Ejecutivo Call Center, Encargados De Brindar Atención Telefónica, Resolver Dudas Básicas, Canalizar Solicitudes Y Ofrecer Un Servicio Cordial Y Eficiente. Horario Laboral: • Lunes A Viernes: 10:00 A... Tiempo Completo Sin Experiencia Guayaquil, Guayas • 26/06/2026 $500,00 / Mensual', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (66, 'Programador Semi Senior Con Conocimiento En Ia Aloha Ecuador Programador Semi Senior Con Conocimientos En Inteligencia Artificial Nos Encontramos En La Búsqueda De Un Programador Semi Senior Con Conocimientos En Inteligencia Artificial, Orientado Al Desarrollo De Soluciones Tecnológicas Eficientes, Escalables E Innovadoras. La Persona Seleccionada Será Responsable De Diseñar,... Por Contrato Quito, Pichincha • 26/06/2026', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (67, 'Técnico De Servicios Motores Y Generadores Svf Ecuador Sa Empresa Multinacional Dedicada A La Distribución De Motores De Combustión Interna En Todas Sus Aplicaciones, Venta De Maquinaria Pesada Y Afines Busca: Técnico Mecánico De Motores Para La Ciudad De Guayaquil Requisitos: • Bachiller Técnico O Tecnólogo En Mecánica Industrial,... Tiempo Completo Guayaquil, Guayas • 24/06/2026', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (68, 'Analista De Tics 3 Astilleros Navales Ecuatorianos- Astinave Ep- Nivel De Instrucción: Tercer Nivel Titulo Requerido: Si Área De Conocimiento: Sistemas Computacionales, Tiempo De Experiencia: Al Menos 5 Años Especificidad De La Experiencia: Sistemas De Programacion, Diseño Y Manejo De Plataformas Informaticas De Comunicaciones Y Tecnologicas, Arquitectura De Computadoras,... Tiempo Completo Guayaquil, Guayas • 23/06/2026 $1.676,00 / Mensual', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (69, 'Vendedor Freelance Con Experiencia Corporacion Bricko Store Sas Responsabilidades Prospección: Identificar Y Contactar A Clientes Potenciales (A Través De Llamadas, Correos O Redes Sociales). Asesoría Y Negociación: Presentar Los Servicios, Destacar Su Valor Y Resolver Objeciones Para Cerrar El Contrato. Gestión De Clientes: Mantener Una Comunicación Fluida, Fidelizar... Por Horas / Freelance Quito, Pichincha • 22/06/2026 $1.000,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (70, 'Ims Platform Engineer Lescor S.A. Buscamos Ingeniero De Plataforma Ims, Para Actividades De Operación Y Mantenimiento (O&M) Para Plataformas Ims, Garantizando La Disponibilidad, Estabilidad Y Rendimiento Del Servicio. Brindar Soporte Para El Despliegue, La Integración Y La Puesta En Marcha De Ims Y Plataformas De... Tiempo Completo Quito O Guayaquil, Pichincha • 19/06/2026', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (71, 'Practicante Pre Profesional De Programación Humantyx Por Encargo De Una Importante Empresa, Nos Encontramos En La Búsqueda De Talentos En Formación Con Bases Técnicas Y Ganas Reales De Desarrollarse En El Mundo Del Software, Aportando En Proyectos Y Aprendiendo En Un Entorno Profesional. Requisitos: Estudiantes De... Prácticas / Becario Sin Experiencia Quito, Pichincha • 19/06/2026', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (72, 'Residente De Obra Inmobiliaria Agropecuaria Rommel Orbe Rivadeneria S.A. Empresa Constructora Ecuatoriana. Buscamos Un Residente De Obra, Para Unirse A Nuestro Equipo Y Liderar Proyectos De Alto Nivel, Asegurando La Calidad Y El Cumplimiento De Los Estándares. Responsabilidades Principales: Planificación, Ejecución Y Supervisión De Obra Civil. Manejo De Personal... Tiempo Completo Guaranda, Bolívar • 28/05/2026 $900,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (73, 'Practicante Preprofesional De Derecho Humantyx En Humantyx, Creemos Que Las Personas Son El Motor Del Éxito. Combinamos Cercanía Humana Con Innovación Tecnológica Para Transformar Talento En Ventaja Competitiva Sostenible. Únete A Nuestro Equipo Dinámico Y Gana Experiencia Real En Derecho Laboral, Corporativo Y Digital Mientras... Prácticas / Becario Sin Experiencia Quito, Pichincha • 20/05/2026', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (74, 'Asesor Comercial Evolneg Business Solutions Actividades Directas: Identificar Nuevas Oportunidades De Negocio. Buscar Nuevos Clientes Para Ampliación La Cartera Comercial. Mantener Actualizadas Las Bases De Datos De La Compañía. Generar Cotizaciones Y Propuestas Comerciales. Realizar Seguimiento A Cotizaciones Y Oportunidades De Negocio. Asesorar Integralmente A... Tiempo Completo Quito, Pichincha • 19/05/2026 $500,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (75, 'Asesores De Call Center Eckolink Satelital Objetivo Del Puesto ​Contactar A Clientes Potenciales Para Ofrecer Soluciones De Entretenimiento (Televisión Satelital, Internet Fibra Óptica), Brindando Una Asesoría Integral Que Garantice El Cierre De Ventas Y La Satisfacción Del Cliente. Responsabilidades Principales ​Realizar Llamadas De Salida (Outbound) A... Por Horas / Freelance Guayaquil, Guayas • 30/05/2026 $600,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (76, 'Community Manager - Sector Odontologico Tecimdec Cia. Ltda. Modalidad: Presencial En Guayaquil Disponibilidad: Inmediata Horario: Tiempo Completo Buscamos Un Community Manager Con Enfoque Estratégico, Capaz De Manejar Marcas Premium, Crear Contenido Relevante Y Sostener Una Línea Visual Coherente Con Identidad Corporativa. Responsabilidades Principales Gestión Y Programación De Contenido... Tiempo Completo Guayaquil, Guayas • 22/05/2026 $460,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (77, 'Tecnico En Seguridad Electronica Telearseg S.A.S Tecnico En Seguridad Electronica Instalar Equipos De Cctv (Cámaras Ip/Analógicas), Dvr/Nvr Y Cables. Montar Sensores, Paneles Y Dispositivos De Alarmas De Intrusión. Instalar Y Configurar Sistemas De Control De Acceso (Lectores, Cerraduras, Controladoras). Realizar Cableado Estructurado (Utp, Fibra, Canalización, Tubería).... Tiempo Completo Chongon, Guayas • 22/06/2026 $700,00 / Mensual', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (78, 'Ejecutivo Contact Center Eckolink Satelital Objetivo Del Puesto Contactar A Clientes Potenciales Para Ofrecer Soluciones De Entretenimiento (Televisión Satelital, Internet Fibra Óptica), Brindando Una Asesoría Integral Que Garantice El Cierre De Ventas Y La Satisfacción Del Cliente. Responsabilidades Principales Realizar Llamadas De Salida (Outbound) A... Por Horas / Freelance Guayaquil, Guayas • 19/06/2026 $600,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (79, 'Content Manager Servicios Profesionales Botica Alemana La Prensa Nos Encontramos En La Búsqueda De Un Profesional Creativo Y Dinámico Para Brindar Servicios De Creación Y Gestión De Contenido Audiovisual Para Nuestras Marcas Botica Real, Botica Alemana Y Consultorios Alemana. Objeto Del Servicio Planificar, Producir Y Gestionar Contenido Audiovisual... Por Horas / Freelance Quito, Pichincha • 12/06/2026 $600,00 / Mensual', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (80, 'Vendedor Contact Center Eckolink Satelital Objetivo Del Puesto Contactar A Clientes Potenciales Para Ofrecer Soluciones De Entretenimiento (Televisión Satelital, Internet Fibra Óptica), Brindando Una Asesoría Integral Que Garantice El Cierre De Ventas Y La Satisfacción Del Cliente. Responsabilidades Principales Realizar Llamadas De Salida (Outbound) A... Tiempo Completo Guayaquil, Guayas • 09/06/2026 $600,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (81, 'Asistente Administrativa Y Bodega Vazurcorp Atención Al Cliente: Reclamos Y Sugerencias. Supervisar Varias Operaciones Diarias De La Oficina/ Facturación Programar Citas, Recibir Y Entregar La Correspondencia Y Manejar Los Correos Electrónicos Entrantes Y Responderlos. Editar, Hacer Fotocopias Y Archivar Documentos. Programación De Reuniones Y Entrevistas.... Tiempo Completo Cuenca, Azuay • 08/06/2026 $482,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (82, 'Chofer Infertec Estamos Buscando A Un Chofer Que Sea Responsable Y Que Garantice El Transporte Seguro, Oportuno Y Eficiente De Mercadería, Equipos Y Materiales De La Empresa Hacia Las Sucursales, Clientes Y Terminales De Transporte, Proporcionando Una Correcta Custodia Del Vehiculo Asignado... Por Contrato Quito, Pichincha • 03/06/2026 $500,00 / Mensual', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (83, 'Ingeniero/ Tecnológo Electromecánico Astriven Ingeniero/ Tecnológo Electromecánico Para Mantenimiento E Instalación De Equipos Tipo De Contratación Tiempo Completo / A Prueba Descripción De La Plaza Requisitos • Título De Ingeniero/Tecnólogo Electromecánico O A Fin. • 5 Años De Experiencia En Instalación Y Mantenimiento De... Tiempo Completo Guayaquil, Guayas • 27/05/2026', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (84, 'Asesor Contact Center Eckolink Satelital ¿Eres Una Persona Proactiva, Con Gran Fluidez Verbal Y Te Apasiona El Mundo De Las Ventas Y La Tecnología? ¡En Eckolink Satelital, Distribuidor Autorizado De Directv, Te Estamos Buscando! Objetivo Del Puesto Contactar A Clientes Potenciales Para Ofrecer Soluciones De... Por Horas / Freelance Guayaquil, Guayas • 11/05/2026 $600,00 / Mensual', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (85, 'Pasantía Laboral / Media And Strategic Deinsa Global Pasantía Laboral / Media Strategy En Deinsa Global Lanzamos Nuestro Programa De Pasantías Laborales, Dirigido A Estudiantes De Alto Rendimiento Y Profesionales Que Deseen Iniciar Su Carrera En Marketing Digital Y Gestión De Proyectos, Dentro De La Plaza Digital, Nuestra... Prácticas / Becario Sin Experiencia Quito, Pichincha • 04/05/2026', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (86, 'Entrenador/Headcoach Medio Tiempo Fitness For You En Fitness For You No Vendemos Accesos A Máquinas; Diseñamos Experiencias De Transformación Física Y Mental Bajo Estándares Premium. No Buscamos Un Instructor Pasivo, Sino Un Coach Líder, Con Un Dominio Impecable De La Biomecánica, La Programación De La Fuerza... Por Contrato Quito- Cumbaya, Pichincha • 29/06/2026 $400,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (87, 'Tecnico Electronico Para Reparar Placas Laptop Tv Impresora Gye Sinilsa Importadora Requerimos Técnico En Computadoras Para El Debido Diagnóstico Y Reparación De Placas Con Daño En Sus Componentes Electrónicos (Ej: Equipos Que No Encienden, Que Se Apagan, Etc) - Interpretar Diagrama Esquemático, Datasheet Y Boardview - Manejo De Herramientas Y Equipos... Tiempo Completo Guayaquil, Guayas • 29/06/2026 $650,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (88, 'Desarrollador/A Web Bilingüe De Tiempo Completo Dream Big Marketing Services Dream Big Marketing Services Está Buscando Un/A Desarrollador/A Web Bilingüe Español/Inglés De Tiempo Completo Para Unirse A Nuestro Equipo De Marketing En Crecimiento. Estamos Buscando Una Persona Con Sólida Experiencia En El Desarrollo De Sitios Web En Wordpress, Excelentes Habilidades... Desde Casa Teletrabajo, Pichincha • 25/06/2026 $880,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (89, 'Electricista Industrial Sumo+ Experiencia: Mínimo 4 Años En Industrias De Manufactura (Preferiblemente Industria Plástica, Papeleras, Cartoneras) Conocimientos: Mantenimiento Preventivo Y Correctivo, Programación De Variadores, Armado De Tableros De 220 - 440, Sensores De Nivel (Esto Es Muy Importante Ya Que Todas Las Maquinas... Tiempo Completo Guayaquil, Guayas • 24/06/2026 $550,00 / Mensual', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (90, 'Auditor Lider Certificadora I-Next Nos Encontramos En La Búsqueda De Un Profesional Calificado Para Desempeñarse Como Auditor Líder En La Norma Iso 9001:2015, Iso 14001:2015, Iso 45001:2018 O En Sistema Integrado, Para La Ciudad Guayaquil Con El Objetivo De Fortalecer Nuestro Equipo Técnico Y... Por Contrato Guayaquil, Guayas • 19/06/2026 $80,00 / Diario', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (91, 'Agente Inmobiliario Con Experiencia - Globalhaus Aurora Globalhaus Sede Aurora ¿Buscas Crecer Profesionalmente En El Sector Inmobiliario? En Globalhaus Buscamos Agentes Inmobiliarios Con Experiencia, Orientados A Resultados, Con Habilidades Comerciales Y Vocación De Servicio Para Formar Parte De Nuestro Equipo. Perfil Del Candidato * Experiencia En Ventas, Atención Al Cliente... Tiempo Completo Daule, Guayas • 18/06/2026 $2.000,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (92, 'Ingeniero De Energía (Energy Engineer) Lescor S.A. Buscamos Un Ingeniero De Energía Proactivo Y Orientado A Resultados Para Unirse A Nuestro Equipo De Operaciones En Ecuador, Con Base En Guayaquil O Quito. En Este Puesto, Será Responsable De La Puesta En Marcha, El Dimensionamiento, La Operación Y... Tiempo Completo Quito, Pichincha • 15/06/2026 $1.200,00 / Mensual', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (93, 'Desarrollador De Nuevos Negocios Cfo Business Consulting Importante Firma Financiera Buscar Incorporar A Su Staff Un: Desarrollador De Negocios Este Es Un Puesto Muy Demandante Ya Que Implica El Cumplimiento De Dos Resultados Muy Importantes • Consolidación De Una Cartera De Clientes Estratégicos Y Fidelizados. • Cuota... Tiempo Completo Quito, Pichincha • 05/06/2026 $500,00 / Mensual', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (94, 'Electrico Programador Surgalare Programación De Plc Y Hmi Gestión De Variadores De Velocidad Mantenimiento De Sistemas De Control Distribuido Calibración De Instrumentación Análisis De Fallas Control De Tensión Y Velocidad Automatización De Bobinado Sistema De Visión Artificial Para Detección De Roturas Optimización Térmica... Tiempo Completo Duran, Guayas • 02/06/2026 $800,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (95, 'Bordador Con Experiencia Leicoss Se Requiere Bordador Con Experiencia Para Empresa Textil Dedicada A La Confección Y Distribución De Ropa Infantil Al Por Mayor. Buscamos Una Persona Responsable, Detallista Y Comprometida, Con Conocimientos En Manejo De Máquinas De Bordado Industrial Y Dominio Del Programa... Tiempo Completo Quito, Pichincha • 26/05/2026 $450,00 / Mensual', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (96, 'Bordador Ta Designs Bordador Y Programador Con Experiencia De Al Menos 2 Años, Bordadoras De Varios Cabezales Y Manejo Completo Del Equipo. Trabajo Estable Con Afiliación Al Seguro Iess Y Derechos De Ley, Jornada Diurna. Tiempo Completo Quito, Pichincha • 26/05/2026', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (97, 'Supervisor De Obra Satmec Solicitud De Servicios Profesionales Ingeniera Civil – Supervisión De Obra Empresa Del Sector Industrial Ubicada En Guayaquil Busca Contratar Los Servicios De Una Ingeniero O Ingeniera Civil Titulado Y Habilitada Para La Supervisión De Un Proyecto De Rehabilitación Por Contrato Guayaquil, Guayas • 01/07/2026', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (98, 'Operador Corp Union Y Progreso Enfoque En La Gestión De Altos Volúmenes De Llamadas Telefónicas (Entrantes Y Salientes) Y Mensajes Digitales Desde Centros De Contacto. Funciones Clave: Realizar Telemercadeo, Gestionar Encuestas, Agendar Citas Y Ejecutar Soporte Técnico Básico Bajo Métricas De Tiempo Tiempo Completo Sin Experiencia Quito, Pichincha • 30/06/2026 $482,00 / Mensual', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (99, 'Médicos Generales Alfamed Vital Médico General Atención Médica Domiciliaria Importante Empresa Dedicada A La Prestación De Servicios De Atención Médica A Domicilio Se Encuentra En La Búsqueda De Médicos Generales Comprometidos Con La Excelencia, La Calidad Asistencial Y El Trato Humanizado, Para Form Por Contrato Quito, Pichincha • 30/06/2026 $200,00 / Semanal', 'QA / Testing');
INSERT INTO dw_ofertas.dim_rol VALUES (100, 'Vendedor Corp Union Y Progreso ¿Te Apasionan Las Ventas Y Los Resultados? Buscamos Personas Con Actitud, Ambición Y Enfoque En El Cliente Para Formar Parte De Nuestro Equipo Comercial. Funciones Principales: * Contactar Y Asesorar A Clientes Potenciales. * Identificar Necesidades Y Ofrecer So Tiempo Completo Sin Experiencia Quito, Pichincha • 30/06/2026 $482,00 / Mensual', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (101, 'Agente Financiero Corp Union Y Progreso Buscamos Un Analista De Crédito Responsable De Evaluar Solicitudes De Financiamiento, Verificar Documentación, Analizar La Capacidad De Pago De Los Clientes Y Emitir Recomendaciones De Aprobación O Rechazo De Créditos. Se Requiere Capacidad Analítica, Atención Al Detall Por Contrato Sin Experiencia Quito, Pichincha • 30/06/2026 $600,00 / Mensual', 'Otros');
INSERT INTO dw_ofertas.dim_rol VALUES (102, 'Desarrolladores De Software', 'Frontend');
INSERT INTO dw_ofertas.dim_rol VALUES (104, 'Desarrollador Php - Remoto', 'Frontend');
INSERT INTO dw_ofertas.dim_rol VALUES (105, 'Desarrollador De Software Guayaquil', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (106, 'Ing. De Procesos (Software)', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (107, 'Mantenimiento De Software Y Hareware', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (108, 'Jefe De Desarrollo De Software', 'Frontend');
INSERT INTO dw_ofertas.dim_rol VALUES (109, 'Ingeniero De Software Senior', 'Soporte Técnico');
INSERT INTO dw_ofertas.dim_rol VALUES (110, 'Technical Business Analyst (Software / Saas / Tecnología)', 'Backend');
INSERT INTO dw_ofertas.dim_rol VALUES (111, 'Ejecutivo Comercial Senior - Software', 'Desarrollo de Software');
INSERT INTO dw_ofertas.dim_rol VALUES (113, 'Ingeniero Civil - Especialista En Diseño Vial, Geotecnia Y Software Cad', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (114, 'Ejecutivo De Ventas Sector It (Erp - Software)', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (115, 'Desarrollador De Software Junior - Guayaquil', 'Data / BI');
INSERT INTO dw_ofertas.dim_rol VALUES (116, 'Docente De Desarrollo De Software Y Programación (Tiempo Parcial)', 'Data / BI');


--
-- Data for Name: dim_tecnologia; Type: TABLE DATA; Schema: dw_ofertas; Owner: postgres
--

INSERT INTO dw_ofertas.dim_tecnologia VALUES (1, 'No especificado', 'No especificado');
INSERT INTO dw_ofertas.dim_tecnologia VALUES (2, 'Excel', 'Herramienta');
INSERT INTO dw_ofertas.dim_tecnologia VALUES (3, 'Git', 'Herramienta');
INSERT INTO dw_ofertas.dim_tecnologia VALUES (4, 'JavaScript', 'Lenguaje');
INSERT INTO dw_ofertas.dim_tecnologia VALUES (5, 'Angular', 'Framework');
INSERT INTO dw_ofertas.dim_tecnologia VALUES (6, 'Power BI', 'BI');
INSERT INTO dw_ofertas.dim_tecnologia VALUES (7, 'SQL', 'Base de Datos');
INSERT INTO dw_ofertas.dim_tecnologia VALUES (8, 'Python', 'Lenguaje');


--
-- Data for Name: dim_tiempo; Type: TABLE DATA; Schema: dw_ofertas; Owner: postgres
--

INSERT INTO dw_ofertas.dim_tiempo VALUES (20260703, '2026-07-03', 3, 7, 3, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260618, '2026-06-18', 18, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260611, '2026-06-11', 11, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260609, '2026-06-09', 9, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260602, '2026-06-02', 2, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260603, '2026-06-03', 3, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260702, '2026-07-02', 2, 7, 3, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260701, '2026-07-01', 1, 7, 3, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260629, '2026-06-29', 29, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260630, '2026-06-30', 30, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260522, '2026-05-22', 22, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260514, '2026-05-14', 14, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260608, '2026-06-08', 8, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260616, '2026-06-16', 16, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260615, '2026-06-15', 15, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260612, '2026-06-12', 12, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260527, '2026-05-27', 27, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260526, '2026-05-26', 26, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260518, '2026-05-18', 18, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260511, '2026-05-11', 11, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260510, '2026-05-10', 10, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260508, '2026-05-08', 8, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260504, '2026-05-04', 4, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260626, '2026-06-26', 26, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260624, '2026-06-24', 24, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260623, '2026-06-23', 23, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260622, '2026-06-22', 22, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260619, '2026-06-19', 19, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260528, '2026-05-28', 28, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260520, '2026-05-20', 20, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260519, '2026-05-19', 19, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260530, '2026-05-30', 30, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260625, '2026-06-25', 25, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260605, '2026-06-05', 5, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260613, '2026-06-13', 13, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260621, '2026-06-21', 21, 6, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260529, '2026-05-29', 29, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260515, '2026-05-15', 15, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260505, '2026-05-05', 5, 5, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260423, '2026-04-23', 23, 4, 2, 2026);
INSERT INTO dw_ofertas.dim_tiempo VALUES (20260410, '2026-04-10', 10, 4, 2, 2026);


--
-- Data for Name: fact_ofertas_laborales; Type: TABLE DATA; Schema: dw_ofertas; Owner: postgres
--

INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (1, 20260703, 1, 1, 1, 1, 1, 554.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (2, 20260618, 1, 1, 2, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (3, 20260611, 1, 2, 3, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (4, 20260609, 1, 1, 1, 1, 1, 482.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (5, 20260602, 1, 1, 4, 1, 1, 500.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (6, 20260603, 1, 3, 5, 1, 1, 394.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (7, 20260603, 1, 4, 6, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (8, 20260603, 1, 1, 7, 1, 1, 500.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (9, 20260603, 1, 1, 8, 1, 1, 482.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (10, 20260703, 1, 4, 9, 1, 1, 394.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (11, 20260703, 1, 4, 10, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (12, 20260703, 1, 1, 11, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (13, 20260703, 1, 5, 12, 1, 1, 550.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (14, 20260702, 1, 6, 13, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (15, 20260702, 1, 1, 14, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (16, 20260702, 1, 1, 15, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (17, 20260702, 1, 1, 16, 1, 1, 500.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (18, 20260702, 1, 1, 17, 1, 1, 600.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (19, 20260701, 1, 1, 7, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (20, 20260629, 1, 4, 18, 1, 1, 394.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (21, 20260703, 2, 7, 19, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (22, 20260703, 2, 8, 20, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (23, 20260703, 2, 9, 21, 1, 1, 1300.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (24, 20260703, 2, 10, 22, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (25, 20260703, 2, 11, 23, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (26, 20260703, 2, 11, 24, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (27, 20260702, 2, 12, 25, 1, 1, 3000.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (28, 20260702, 2, 13, 26, 1, 1, 1130.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (29, 20260701, 2, 14, 27, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (30, 20260701, 2, 15, 28, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (31, 20260701, 2, 13, 29, 1, 1, 1300.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (32, 20260701, 2, 16, 30, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (33, 20260701, 2, 9, 31, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (34, 20260630, 2, 17, 32, 1, 1, 1300.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (35, 20260630, 2, 14, 33, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (36, 20260630, 2, 18, 34, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (37, 20260630, 2, 19, 35, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (38, 20260630, 2, 19, 36, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (39, 20260630, 2, 19, 37, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (40, 20260630, 2, 12, 38, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (41, 20260522, 3, 20, 39, 2, 1, 482.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (42, 20260514, 3, 21, 40, 2, 1, 550.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (43, 20260608, 3, 20, 41, 2, 2, 482.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (44, 20260629, 3, 22, 42, 3, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (45, 20260618, 3, 20, 43, 2, 3, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (46, 20260618, 3, 20, 44, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (47, 20260616, 3, 23, 45, 2, 4, 700.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (48, 20260615, 3, 21, 46, 2, 1, 550.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (49, 20260612, 3, 24, 47, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (50, 20260602, 3, 21, 48, 2, 2, NULL, 1, 2);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (51, 20260602, 3, 21, 49, 2, 2, NULL, 1, 2);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (52, 20260602, 3, 20, 50, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (53, 20260602, 3, 21, 51, 2, 1, 600.00, 1, 3);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (54, 20260527, 3, 20, 52, 2, 1, 800.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (55, 20260526, 3, 21, 53, 2, 1, 500.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (56, 20260518, 3, 20, 54, 2, 1, 482.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (57, 20260518, 3, 21, 55, 2, 1, 500.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (58, 20260514, 3, 21, 56, 2, 1, 900.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (59, 20260511, 3, 21, 57, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (60, 20260510, 3, 25, 58, 2, 4, 550.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (61, 20260508, 3, 21, 59, 2, 1, 500.00, 1, 1);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (62, 20260504, 3, 26, 60, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (63, 20260504, 3, 26, 61, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (64, 20260504, 3, 26, 62, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (65, 20260504, 3, 26, 63, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (66, 20260629, 3, 20, 64, 2, 1, NULL, 1, 1);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (67, 20260626, 3, 20, 65, 2, 1, 500.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (68, 20260626, 3, 26, 66, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (69, 20260624, 3, 26, 67, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (70, 20260623, 3, 20, 68, 2, 1, 1676.00, 1, 5);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (71, 20260622, 3, 21, 69, 1, 1, 1000.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (72, 20260619, 3, 21, 70, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (73, 20260619, 3, 21, 71, 1, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (74, 20260528, 3, 27, 72, 2, 1, 900.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (75, 20260520, 3, 21, 73, 1, 3, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (76, 20260519, 3, 21, 74, 2, 1, 500.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (77, 20260530, 3, 20, 75, 1, 1, 600.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (78, 20260522, 3, 20, 76, 2, 1, 460.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (79, 20260622, 3, 23, 77, 2, 1, 700.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (80, 20260619, 3, 20, 78, 1, 1, 600.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (81, 20260612, 3, 21, 79, 1, 1, 600.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (82, 20260609, 3, 20, 80, 2, 1, 600.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (83, 20260608, 3, 28, 81, 2, 1, 482.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (84, 20260603, 3, 21, 82, 2, 1, 500.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (85, 20260527, 3, 20, 83, 2, 1, NULL, 1, 5);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (86, 20260511, 3, 20, 84, 1, 1, 600.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (87, 20260504, 3, 21, 85, 1, 3, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (88, 20260629, 3, 21, 86, 2, 1, 400.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (89, 20260629, 3, 20, 87, 2, 1, 650.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (90, 20260625, 3, 29, 88, 2, 2, 880.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (91, 20260624, 3, 20, 89, 2, 1, 550.00, 1, 4);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (92, 20260619, 3, 20, 90, 2, 1, 80.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (93, 20260618, 3, 30, 91, 2, 1, 2000.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (94, 20260615, 3, 26, 92, 2, 1, 1200.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (95, 20260605, 3, 21, 93, 2, 1, 500.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (96, 20260602, 3, 31, 94, 2, 1, 800.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (97, 20260526, 3, 21, 95, 2, 1, 450.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (98, 20260526, 3, 21, 96, 2, 1, NULL, 1, 2);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (99, 20260701, 3, 20, 97, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (100, 20260630, 3, 21, 98, 2, 3, 482.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (101, 20260630, 3, 21, 99, 2, 2, 200.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (102, 20260630, 3, 21, 100, 2, 1, 482.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (103, 20260630, 3, 21, 101, 2, 1, 600.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (104, 20260630, 4, 20, 102, 2, 4, 800.00, 1, 3);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (105, 20260613, 4, 20, 1, 2, 5, 358.00, 1, 3);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (106, 20260526, 4, 20, 104, 3, 4, 405.00, 1, 20);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (107, 20260616, 4, 20, 105, 2, 4, 17.50, 1, 2);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (108, 20260526, 4, 20, 106, 2, 6, 408.00, 1, 20);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (109, 20260630, 4, 20, 107, 2, 1, 800.00, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (110, 20260624, 5, 1, 108, 2, 4, NULL, 1, 6);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (111, 20260605, 5, 1, 1, 2, 4, NULL, 1, 2);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (112, 20260611, 5, 1, 109, 2, 2, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (113, 20260621, 5, 1, 110, 3, 7, NULL, 1, 5);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (114, 20260608, 5, 1, 111, 4, 1, NULL, 1, 5);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (115, 20260529, 5, 1, 4, 2, 2, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (116, 20260605, 5, 32, 113, 2, 1, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (117, 20260515, 5, 1, 114, 2, 2, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (118, 20260505, 5, 4, 115, 4, 4, NULL, 1, 1);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (119, 20260423, 5, 33, 116, 2, 2, NULL, 1, NULL);
INSERT INTO dw_ofertas.fact_ofertas_laborales VALUES (120, 20260410, 5, 34, 1, 2, 8, NULL, 1, 2);


--
-- Name: dim_ciudad_id_ciudad_seq; Type: SEQUENCE SET; Schema: dw_ofertas; Owner: postgres
--

SELECT pg_catalog.setval('dw_ofertas.dim_ciudad_id_ciudad_seq', 34, true);


--
-- Name: dim_fuente_id_fuente_seq; Type: SEQUENCE SET; Schema: dw_ofertas; Owner: postgres
--

SELECT pg_catalog.setval('dw_ofertas.dim_fuente_id_fuente_seq', 5, true);


--
-- Name: dim_modalidad_id_modalidad_seq; Type: SEQUENCE SET; Schema: dw_ofertas; Owner: postgres
--

SELECT pg_catalog.setval('dw_ofertas.dim_modalidad_id_modalidad_seq', 4, true);


--
-- Name: dim_rol_id_rol_seq; Type: SEQUENCE SET; Schema: dw_ofertas; Owner: postgres
--

SELECT pg_catalog.setval('dw_ofertas.dim_rol_id_rol_seq', 117, true);


--
-- Name: dim_tecnologia_id_tecnologia_seq; Type: SEQUENCE SET; Schema: dw_ofertas; Owner: postgres
--

SELECT pg_catalog.setval('dw_ofertas.dim_tecnologia_id_tecnologia_seq', 8, true);


--
-- Name: fact_ofertas_laborales_id_hecho_seq; Type: SEQUENCE SET; Schema: dw_ofertas; Owner: postgres
--

SELECT pg_catalog.setval('dw_ofertas.fact_ofertas_laborales_id_hecho_seq', 120, true);


--
-- Name: dim_ciudad dim_ciudad_pkey; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_ciudad
    ADD CONSTRAINT dim_ciudad_pkey PRIMARY KEY (id_ciudad);


--
-- Name: dim_fuente dim_fuente_nombre_fuente_key; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_fuente
    ADD CONSTRAINT dim_fuente_nombre_fuente_key UNIQUE (nombre_fuente);


--
-- Name: dim_fuente dim_fuente_pkey; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_fuente
    ADD CONSTRAINT dim_fuente_pkey PRIMARY KEY (id_fuente);


--
-- Name: dim_modalidad dim_modalidad_modalidad_key; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_modalidad
    ADD CONSTRAINT dim_modalidad_modalidad_key UNIQUE (modalidad);


--
-- Name: dim_modalidad dim_modalidad_pkey; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_modalidad
    ADD CONSTRAINT dim_modalidad_pkey PRIMARY KEY (id_modalidad);


--
-- Name: dim_rol dim_rol_nombre_rol_key; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_rol
    ADD CONSTRAINT dim_rol_nombre_rol_key UNIQUE (nombre_rol);


--
-- Name: dim_rol dim_rol_pkey; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_rol
    ADD CONSTRAINT dim_rol_pkey PRIMARY KEY (id_rol);


--
-- Name: dim_tecnologia dim_tecnologia_nombre_tecnologia_key; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_tecnologia
    ADD CONSTRAINT dim_tecnologia_nombre_tecnologia_key UNIQUE (nombre_tecnologia);


--
-- Name: dim_tecnologia dim_tecnologia_pkey; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_tecnologia
    ADD CONSTRAINT dim_tecnologia_pkey PRIMARY KEY (id_tecnologia);


--
-- Name: dim_tiempo dim_tiempo_pkey; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_tiempo
    ADD CONSTRAINT dim_tiempo_pkey PRIMARY KEY (id_tiempo);


--
-- Name: fact_ofertas_laborales fact_ofertas_laborales_pkey; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.fact_ofertas_laborales
    ADD CONSTRAINT fact_ofertas_laborales_pkey PRIMARY KEY (id_hecho);


--
-- Name: dim_ciudad uq_dim_ciudad; Type: CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.dim_ciudad
    ADD CONSTRAINT uq_dim_ciudad UNIQUE (ciudad, provincia, pais);


--
-- Name: idx_fact_ciudad; Type: INDEX; Schema: dw_ofertas; Owner: postgres
--

CREATE INDEX idx_fact_ciudad ON dw_ofertas.fact_ofertas_laborales USING btree (id_ciudad);


--
-- Name: idx_fact_fuente; Type: INDEX; Schema: dw_ofertas; Owner: postgres
--

CREATE INDEX idx_fact_fuente ON dw_ofertas.fact_ofertas_laborales USING btree (id_fuente);


--
-- Name: idx_fact_modalidad; Type: INDEX; Schema: dw_ofertas; Owner: postgres
--

CREATE INDEX idx_fact_modalidad ON dw_ofertas.fact_ofertas_laborales USING btree (id_modalidad);


--
-- Name: idx_fact_rol; Type: INDEX; Schema: dw_ofertas; Owner: postgres
--

CREATE INDEX idx_fact_rol ON dw_ofertas.fact_ofertas_laborales USING btree (id_rol);


--
-- Name: idx_fact_tecnologia; Type: INDEX; Schema: dw_ofertas; Owner: postgres
--

CREATE INDEX idx_fact_tecnologia ON dw_ofertas.fact_ofertas_laborales USING btree (id_tecnologia);


--
-- Name: idx_fact_tiempo; Type: INDEX; Schema: dw_ofertas; Owner: postgres
--

CREATE INDEX idx_fact_tiempo ON dw_ofertas.fact_ofertas_laborales USING btree (id_tiempo);


--
-- Name: fact_ofertas_laborales fk_fact_ciudad; Type: FK CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.fact_ofertas_laborales
    ADD CONSTRAINT fk_fact_ciudad FOREIGN KEY (id_ciudad) REFERENCES dw_ofertas.dim_ciudad(id_ciudad);


--
-- Name: fact_ofertas_laborales fk_fact_fuente; Type: FK CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.fact_ofertas_laborales
    ADD CONSTRAINT fk_fact_fuente FOREIGN KEY (id_fuente) REFERENCES dw_ofertas.dim_fuente(id_fuente);


--
-- Name: fact_ofertas_laborales fk_fact_modalidad; Type: FK CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.fact_ofertas_laborales
    ADD CONSTRAINT fk_fact_modalidad FOREIGN KEY (id_modalidad) REFERENCES dw_ofertas.dim_modalidad(id_modalidad);


--
-- Name: fact_ofertas_laborales fk_fact_rol; Type: FK CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.fact_ofertas_laborales
    ADD CONSTRAINT fk_fact_rol FOREIGN KEY (id_rol) REFERENCES dw_ofertas.dim_rol(id_rol);


--
-- Name: fact_ofertas_laborales fk_fact_tecnologia; Type: FK CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.fact_ofertas_laborales
    ADD CONSTRAINT fk_fact_tecnologia FOREIGN KEY (id_tecnologia) REFERENCES dw_ofertas.dim_tecnologia(id_tecnologia);


--
-- Name: fact_ofertas_laborales fk_fact_tiempo; Type: FK CONSTRAINT; Schema: dw_ofertas; Owner: postgres
--

ALTER TABLE ONLY dw_ofertas.fact_ofertas_laborales
    ADD CONSTRAINT fk_fact_tiempo FOREIGN KEY (id_tiempo) REFERENCES dw_ofertas.dim_tiempo(id_tiempo);


--
-- PostgreSQL database dump complete
--

