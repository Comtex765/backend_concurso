-- Table: public.ciudad

-- DROP TABLE IF EXISTS public.ciudad;

CREATE TABLE IF NOT EXISTS public.ciudad
(
    id_ciudad integer NOT NULL,
    nombre_ciudad character varying(50) COLLATE pg_catalog."default",
    id_pais integer,
    id_estado integer,
    latitude character varying(50) COLLATE pg_catalog."default",
    longitude character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT ciudad_pkey PRIMARY KEY (id_ciudad),
    CONSTRAINT ciudad_id_estado_fkey FOREIGN KEY (id_estado)
        REFERENCES public.estado (id_estado) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT ciudad_id_pais_fkey FOREIGN KEY (id_pais)
        REFERENCES public.pais (id_pais) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ciudad
    OWNER to comtex;
-- Index: ix_cities_id

-- DROP INDEX IF EXISTS public.ix_cities_id;

CREATE INDEX IF NOT EXISTS ix_cities_id
    ON public.ciudad USING btree
    (id_ciudad ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.estado

-- DROP TABLE IF EXISTS public.estado;

CREATE TABLE IF NOT EXISTS public.estado
(
    id_estado integer NOT NULL,
    nombre_estado character varying COLLATE pg_catalog."default",
    id_pais integer,
    cod_pais character varying(5) COLLATE pg_catalog."default",
    iso2 character varying(5) COLLATE pg_catalog."default",
    type_state character varying(50) COLLATE pg_catalog."default",
    latitude character varying(50) COLLATE pg_catalog."default",
    longitude character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT estado_pkey PRIMARY KEY (id_estado),
    CONSTRAINT estado_country_id_fkey FOREIGN KEY (id_pais)
        REFERENCES public.pais (id_pais) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.estado
    OWNER to comtex;
-- Index: ix_states_id

-- DROP INDEX IF EXISTS public.ix_states_id;

CREATE INDEX IF NOT EXISTS ix_states_id
    ON public.estado USING btree
    (id_estado ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.pais

-- DROP TABLE IF EXISTS public.pais;

CREATE TABLE IF NOT EXISTS public.pais
(
    id_pais integer NOT NULL,
    nombre_pais character varying(50) COLLATE pg_catalog."default",
    iso2 character varying(2) COLLATE pg_catalog."default",
    iso3 character varying(3) COLLATE pg_catalog."default",
    phonecode character varying(16) COLLATE pg_catalog."default",
    capital character varying(50) COLLATE pg_catalog."default",
    currency character varying(3) COLLATE pg_catalog."default",
    CONSTRAINT pais_pkey PRIMARY KEY (id_pais)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.pais
    OWNER to comtex;
-- Index: ix_countries_id

-- DROP INDEX IF EXISTS public.ix_countries_id;

CREATE INDEX IF NOT EXISTS ix_countries_id
    ON public.pais USING btree
    (id_pais ASC NULLS LAST)
    TABLESPACE pg_default;