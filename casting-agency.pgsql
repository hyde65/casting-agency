--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Actor; Type: TABLE; Schema: public; Owner: manuel
--

CREATE TABLE public."Actor" (
    id integer NOT NULL,
    name character varying,
    gender character varying
);


ALTER TABLE public."Actor" OWNER TO manuel;

--
-- Name: Actor_id_seq; Type: SEQUENCE; Schema: public; Owner: manuel
--

CREATE SEQUENCE public."Actor_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Actor_id_seq" OWNER TO manuel;

--
-- Name: Actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: manuel
--

ALTER SEQUENCE public."Actor_id_seq" OWNED BY public."Actor".id;


--
-- Name: Movie; Type: TABLE; Schema: public; Owner: manuel
--

CREATE TABLE public."Movie" (
    id integer NOT NULL,
    title character varying,
    release_date timestamp without time zone
);


ALTER TABLE public."Movie" OWNER TO manuel;

--
-- Name: Movie_Actor; Type: TABLE; Schema: public; Owner: manuel
--

CREATE TABLE public."Movie_Actor" (
    "Movie_id" integer,
    "Actor_id" integer
);


ALTER TABLE public."Movie_Actor" OWNER TO manuel;

--
-- Name: Movie_id_seq; Type: SEQUENCE; Schema: public; Owner: manuel
--

CREATE SEQUENCE public."Movie_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Movie_id_seq" OWNER TO manuel;

--
-- Name: Movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: manuel
--

ALTER SEQUENCE public."Movie_id_seq" OWNED BY public."Movie".id;


--
-- Name: Actor id; Type: DEFAULT; Schema: public; Owner: manuel
--

ALTER TABLE ONLY public."Actor" ALTER COLUMN id SET DEFAULT nextval('public."Actor_id_seq"'::regclass);


--
-- Name: Movie id; Type: DEFAULT; Schema: public; Owner: manuel
--

ALTER TABLE ONLY public."Movie" ALTER COLUMN id SET DEFAULT nextval('public."Movie_id_seq"'::regclass);


--
-- Data for Name: Actor; Type: TABLE DATA; Schema: public; Owner: manuel
--

COPY public."Actor" (id, name, gender) FROM stdin;
1	Daniel Radcliffe	Male
2	Emma Watson	Female
3	Tom Hardy	Male
4	Anya Taylor-Joy	Fame
5	Noah Wyle	Male
6	Anthony Michael Hall	Male
\.


--
-- Data for Name: Movie; Type: TABLE DATA; Schema: public; Owner: manuel
--

COPY public."Movie" (id, title, release_date) FROM stdin;
1	Harry poter 3	2004-01-01 00:00:00
2	Mad Max: Fury Road	2015-01-01 00:00:00
3	Your name	2016-01-01 00:00:00
4	Pirates of Silicon Valley	1999-01-01 00:00:00
5	Beauty and the Beast	2017-01-01 00:00:00
\.


--
-- Data for Name: Movie_Actor; Type: TABLE DATA; Schema: public; Owner: manuel
--

COPY public."Movie_Actor" ("Movie_id", "Actor_id") FROM stdin;
1	1
1	2
2	3
2	4
4	5
4	6
5	2
\.


--
-- Name: Actor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: manuel
--

SELECT pg_catalog.setval('public."Actor_id_seq"', 6, true);


--
-- Name: Movie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: manuel
--

SELECT pg_catalog.setval('public."Movie_id_seq"', 5, true);


--
-- Name: Actor Actor_pkey; Type: CONSTRAINT; Schema: public; Owner: manuel
--

ALTER TABLE ONLY public."Actor"
    ADD CONSTRAINT "Actor_pkey" PRIMARY KEY (id);


--
-- Name: Movie Movie_pkey; Type: CONSTRAINT; Schema: public; Owner: manuel
--

ALTER TABLE ONLY public."Movie"
    ADD CONSTRAINT "Movie_pkey" PRIMARY KEY (id);


--
-- Name: Movie_Actor Movie_Actor_Actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: manuel
--

ALTER TABLE ONLY public."Movie_Actor"
    ADD CONSTRAINT "Movie_Actor_Actor_id_fkey" FOREIGN KEY ("Actor_id") REFERENCES public."Actor"(id);


--
-- Name: Movie_Actor Movie_Actor_Movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: manuel
--

ALTER TABLE ONLY public."Movie_Actor"
    ADD CONSTRAINT "Movie_Actor_Movie_id_fkey" FOREIGN KEY ("Movie_id") REFERENCES public."Movie"(id);


--
-- PostgreSQL database dump complete
--

