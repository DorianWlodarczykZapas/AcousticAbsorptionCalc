--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1
-- Dumped by pg_dump version 15.1

-- Started on 2025-03-18 14:36:46

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
-- TOC entry 216 (class 1259 OID 16644)
-- Name: materials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.materials (
    pkey integer NOT NULL,
    type character varying(100) NOT NULL,
    name character varying(100) NOT NULL,
    _120 numeric(22,2) NOT NULL,
    _250 numeric(22,2) NOT NULL,
    _500 numeric(22,2) NOT NULL,
    _1000 numeric(22,2) NOT NULL,
    _2000 numeric(22,2) NOT NULL,
    _4000 numeric(22,2) NOT NULL
);


ALTER TABLE public.materials OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16399)
-- Name: materials_pkey_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.materials_pkey_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.materials_pkey_seq OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16643)
-- Name: materials_pkey_seq1; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.materials_pkey_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.materials_pkey_seq1 OWNER TO postgres;

--
-- TOC entry 3392 (class 0 OID 0)
-- Dependencies: 215
-- Name: materials_pkey_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.materials_pkey_seq1 OWNED BY public.materials.pkey;


--
-- TOC entry 218 (class 1259 OID 16651)
-- Name: norms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.norms (
    pkey integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.norms OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16659)
-- Name: norms_absorption_multiplayer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.norms_absorption_multiplayer (
    norm_id integer NOT NULL,
    absorption_multiplayer numeric(22,2) NOT NULL
);


ALTER TABLE public.norms_absorption_multiplayer OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16650)
-- Name: norms_pkey_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.norms_pkey_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.norms_pkey_seq OWNER TO postgres;

--
-- TOC entry 3393 (class 0 OID 0)
-- Dependencies: 217
-- Name: norms_pkey_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.norms_pkey_seq OWNED BY public.norms.pkey;


--
-- TOC entry 222 (class 1259 OID 16683)
-- Name: norms_reverb_time_height_req; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.norms_reverb_time_height_req (
    norm_id integer NOT NULL,
    h_less_4 numeric(22,2),
    h_between_4_16 numeric(22,2),
    h_more_16 numeric(22,2)
);


ALTER TABLE public.norms_reverb_time_height_req OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16667)
-- Name: norms_reverb_time_no_req; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.norms_reverb_time_no_req (
    norm_id integer NOT NULL,
    no_cubature_req numeric(22,2)
);


ALTER TABLE public.norms_reverb_time_no_req OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16675)
-- Name: norms_reverb_time_volume_req; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.norms_reverb_time_volume_req (
    norm_id integer NOT NULL,
    less_120 numeric(22,2),
    between_120_250 numeric(22,2),
    between_250_500 numeric(22,2),
    between_500_2000 numeric(22,2),
    more_2000 numeric(22,2),
    less_5000 numeric(22,2),
    more_5000 numeric(22,2)
);


ALTER TABLE public.norms_reverb_time_volume_req OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16691)
-- Name: norms_speech_transmission_index; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.norms_speech_transmission_index (
    norm_id integer NOT NULL,
    between_120_250 numeric(22,2),
    between_250_500 numeric(22,2),
    between_500_2000 numeric(22,2),
    more_2000 numeric(22,2)
);


ALTER TABLE public.norms_speech_transmission_index OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16753)
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id integer NOT NULL,
    user_id integer,
    name character varying(255) NOT NULL,
    norm_id integer NOT NULL,
    up_to_norm text NOT NULL,
    length numeric(22,2) NOT NULL,
    width numeric(22,2) NOT NULL,
    height numeric(22,2) NOT NULL,
    floor numeric(22,2) NOT NULL,
    sufit_id integer NOT NULL,
    wall1_id integer NOT NULL,
    wall2_id integer NOT NULL,
    wall3_id integer NOT NULL,
    wall4_id integer NOT NULL,
    furniture text NOT NULL,
    _120 numeric(22,2) NOT NULL,
    _250 numeric(22,2) NOT NULL,
    _500 numeric(22,2) NOT NULL,
    _1000 numeric(22,2) NOT NULL,
    _2000 numeric(22,2) NOT NULL,
    _4000 numeric(22,2) NOT NULL,
    reverb_time_120 numeric(22,2) NOT NULL,
    reverb_time_250 numeric(22,2) NOT NULL,
    reverb_time_500 numeric(22,2) NOT NULL,
    reverb_time_1000 numeric(22,2) NOT NULL,
    reverb_time_2000 numeric(22,2) NOT NULL,
    reverb_time_4000 numeric(22,2) NOT NULL,
    requirements text NOT NULL
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16752)
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_id_seq OWNER TO postgres;

--
-- TOC entry 3394 (class 0 OID 0)
-- Dependencies: 226
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- TOC entry 225 (class 1259 OID 16710)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(150),
    password character varying(150),
    first_name character varying(150)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16709)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 3395 (class 0 OID 0)
-- Dependencies: 224
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 3209 (class 2604 OID 16647)
-- Name: materials pkey; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials ALTER COLUMN pkey SET DEFAULT nextval('public.materials_pkey_seq1'::regclass);


--
-- TOC entry 3210 (class 2604 OID 16654)
-- Name: norms pkey; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.norms ALTER COLUMN pkey SET DEFAULT nextval('public.norms_pkey_seq'::regclass);


--
-- TOC entry 3212 (class 2604 OID 16756)
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- TOC entry 3211 (class 2604 OID 16713)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3375 (class 0 OID 16644)
-- Dependencies: 216
-- Data for Name: materials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materials (pkey, type, name, _120, _250, _500, _1000, _2000, _4000) FROM stdin;
1	Ściany	Fasada aluminiowa słupowo-ryglowa	0.15	0.05	0.03	0.03	0.02	0.02
2	Ściany	Beton niemalowany (surowy)	0.01	0.01	0.02	0.02	0.02	0.04
3	Ściany	Beton szorstki 	0.02	0.03	0.03	0.03	0.04	0.07
4	Ściany	Beton zatarty na gładko	0.01	0.01	0.02	0.02	0.02	0.05
5	Ściany	Beton, gładki lub malowany	0.01	0.01	0.02	0.02	0.02	0.02
6	Ściany	Beton, szorstkie wykończenie	0.02	0.03	0.03	0.03	0.04	0.07
7	Ściany	Bloczki - 115mm malowane	0.10	0.08	0.05	0.03	0.04	0.07
8	Ściany	Bloczki - 115mm porowate	0.13	0.10	0.07	0.08	0.14	0.20
9	Ściany	Bloczki malowane	0.02	0.03	0.03	0.03	0.04	0.07
10	Ściany	Bloczki porowate	0.05	0.05	0.05	0.08	0.14	0.20
11	Ściany	Boazeria drewniana z desek o grubości od 16 mm do 22 mm z pustką 50 mm wypełnioną wełną mineralną	0.25	0.15	0.10	0.09	0.08	0.07
12	Ściany	Cegła ceramiczna licowa porowata	0.15	0.13	0.15	0.15	0.13	0.14
13	Ściany	Cegła nieotynkowana	0.02	0.02	0.03	0.04	0.05	0.07
14	Ściany	Cegła nieotynkowana z głębokimi fugami (10 mm)	0.08	0.09	0.12	0.16	0.22	0.24
15	Ściany	Deski sosnowe na murze	0.10	0.11	0.10	0.08	0.08	0.11
16	Ściany	Deskowanie z otwartymi szczelinami, pustka 50 mm	0.24	0.80	0.35	0.18	0.10	0.10
17	Ściany	Drewniane płyty akustyczne z włókniną akustyczną, pustka 50 mm	0.70	0.59	0.71	0.67	0.66	0.63
18	Ściany	Drewniane płyty akustyczne ze specjalnym tynkiem, pustka 50 mm	0.25	0.54	0.64	0.63	0.72	0.68
19	Ściany	Drewno politurowane	0.05	0.04	0.03	0.03	0.04	0.04
20	Sufit	Beton niemalowany	0.01	0.01	0.02	0.02	0.02	0.02
21	Sufit	Miękkie włókna 20mm na twardym podłożu	0.05	0.20	0.60	0.80	0.67	0.53
22	Sufit	Płyta na 200mm pustki powietrznej	0.45	0.65	0.70	0.55	0.95	0.95
23	Sufit	Płyta (Ecophon) na 200mm pustki powietrznej	0.50	0.85	0.90	0.85	0.95	0.85
24	Sufit	Płyta (Ecophon) 200mm pustki powietrznej	0.50	0.85	0.95	0.85	1.00	1.00
25	Sufit	Płyta (Ecophon)	0.40	0.95	1.00	0.95	0.95	1.00
26	Sufit	Płyta na 200mm pustki powietrznej	0.55	0.75	0.95	0.85	1.00	1.00
27	Sufit	Płyta na 200mm pustki powietrznej	0.40	0.85	1.00	0.95	0.80	0.70
28	Sufit	Płyta na 200mm pustki powietrznej	0.40	0.70	0.70	0.65	0.90	1.00
29	Sufit	Płyty gipsowo-kartonowe na 200mm przestrzeni powietrznej	0.55	0.70	0.75	0.65	0.04	0.04
30	Sufit	Płyty gipsowo-kartonowe na legarach	0.20	0.15	0.10	0.05	0.60	0.55
31	Sufit	Płyty z wełny drzewnej 50mm na 50mm pustce	0.15	0.45	0.75	0.60	0.60	0.55
32	Sufit	Płyty z wełny drzewnej 50mm na twardym podłożu	0.10	0.20	0.45	0.80	0.80	0.75
33	Sufit	Stal	0.02	0.03	0.03	0.02	0.10	0.05
34	Sufit	Strop drewniany gładki bez rys	0.28	0.10	0.07	0.06	0.05	0.06
35	Sufit	Strop z siatką Rabitza	0.25	0.20	0.10	0.05	0.70	0.75
36	Sufit	Tynk akustyczny 9-12mm na płycie gipsowo-kartonowej	0.25	0.25	0.35	0.50	0.02	0.03
37	Sufit	Tynk akustyczny 9-12mm na twardym podłożu	0.05	0.15	0.30	0.50	0.70	0.75
38	Sufit	Tynk na listwach	0.20	0.15	0.10	0.05	0.50	0.35
39	Sufit	Tynk na twardym podłożu	0.03	0.03	0.02	0.02	0.04	0.04
40	Inne	Alpha ClassFrames	0.20	0.60	1.00	1.00	1.00	1.00
41	Inne	Axam Acoustic 1.44m2 	0.27	0.47	0.76	1.17	1.32	1.29
42	Inne	Axam Acoustic 2.16m2	0.41	0.71	1.14	1.75	1.98	1.94
43	Inne	Axam Acoustic 2.88m2	0.55	0.95	1.51	2.33	2.63	2.58
44	Inne	Axam Acoustic 3.24m2	0.61	1.07	1.70	2.63	2.96	2.90
45	Inne	Axam  Acoustic 3.60m2	0.68	1.19	1.89	2.92	3.29	3.23
46	Inne	Axam Acoustic 4.32m2	0.82	1.42	2.27	3.50	3.95	3.87
47	Inne	Axam Acoustic 5.40m2	1.02	1.78	2.84	4.38	4.94	4.84
48	Inne	Axam Acoustic 5.76m2	1.09	1.90	3.03	4.67	5.27	5.16
49	Inne	Axam Acoustic 7.20m2	1.36	2.37	3.79	5.84	6.59	6.45
50	Inne	Axam Acoustic 9.00m2	1.70	2.97	4.73	7.30	8.23	8.07
51	Inne	Axam Acoustic 2.54m2	0.48	0.84	1.34	2.06	2.32	2.28
52	Inne	Axam Plain 4.52m2	0.85	1.49	2.38	3.67	4.13	4.05
53	Inne	Axam Plain 3.62m2	0.68	1.19	1.90	2.94	3.31	3.24
54	Inne	Axam Plain 4.70m2	0.89	1.55	2.47	3.81	4.30	4.21
55	Inne	Axam Plain 5.07m2	0.96	1.67	2.67	4.11	4.64	4.54
56	Inne	Axam Plain 6.50m2	1.23	2.14	3.42	5.27	5.95	5.83
57	Inne	Axam Plain Acoustic 8.30m2	1.57	2.74	4.37	6.73	7.59	7.44
58	Inne	Axam Acoustic 1.44m2	0.25	0.29	0.37	0.43	0.57	0.74
59	Inne	Axam Plain 2.16m2	0.38	0.44	0.56	0.65	0.86	1.12
60	Inne	Okno, pełnej wysokości z podwójną ramą	0.15	0.05	0.03	0.03	0.02	0.02
61	Inne	Drzwi drewniane pełne	0.15	0.10	0.08	0.08	0.05	0.05
62	Inne	Drzwi drewniane puste	0.30	0.25	0.15	0.10	0.10	0.07
63	Inne	Drzwi drewniane, masywne Tab. B.1.	0.14	0.10	0.08	0.08	0.08	0.08
64	Inne	Pustka powietrzna	0.25	0.30	0.40	0.45	0.50	0.50
65	Inne	Pustka powietrzna dla innej otwartej przestrzenie - estymacja	0.40	0.40	0.60	0.70	0.80	0.80
66	Inne	Pustka powietrzna, scena z dekoracją	0.40	0.40	0.60	0.70	0.80	0.80
67	Inne	Szyba podwójna 2 ÷ 3 mm z pustką powietrzną ≥ 30 mm	0.15	0.05	0.03	0.03	0.02	0.02
68	Inne	Szyba podwójna 2 ÷ 3 mm z pustką powietrzną 10 mm	0.10	0.07	0.05	0.03	0.02	0.02
69	Inne	Szyba podwójna z izolacją akustyczną	0.15	0.05	0.03	0.03	0.02	0.02
70	Inne	Szyba podwójna z izolacją cieplną	0.10	0.07	0.05	0.03	0.02	0.02
71	Inne	Szyba pojedyncza 3 mm	0.08	0.04	0.03	0.03	0.02	0.02
72	Inne	Szklana fasada z izolacją termiczną	0.15	0.05	0.03	0.03	0.02	0.02
73	Inne	Drzwi drewniane, masywne	0.14	0.10	0.08	0.08	0.08	0.08
74	Inne	Szyba podwójna 2+3mm z pustką 10 mm	0.10	0.07	0.05	0.03	0.02	0.02
75	Inne	Drzwi malowane olejno	0.08	0.14	0.12	0.15	0.19	0.17
76	Inne	Dzrwi malowane olejno 	0.08	0.14	0.12	0.15	0.19	0.17
77	Inne	Drzwi malowane olejowo	0.08	0.14	0.12	0.15	0.19	0.17
78	Inne	Drzwi malowane olejno	0.08	0.14	0.12	0.15	0.19	0.17
79	Inne	PCV (dwuszybowe)	0.10	0.07	0.05	0.03	0.02	0.02
80	Inne	Meble w zabudowie kuchennej i przedsionku	0.00	0.00	0.00	0.00	0.00	0.00
81	Inne	Krzesła w rzędach w odstepach od 0,9 do 1,2 m, bez ludzi (drewno, tw, sztuczne)	0.06	0.08	0.10	0.12	0.14	0.16
82	Inne	Krzesła drewniane z siedzącą osobą	0.72	0.88	0.95	0.98	0.99	1.00
83	Inne	Krzesła puste	0.10	0.12	0.12	0.30	0.25	0.14
84	Inne	Ludzie na krzesłach materiałowych	0.00	0.00	0.42	0.47	0.00	0.00
85	Inne	Płyty gipsowe perforowane	0.65	0.60	0.65	0.71	0.75	0.70
86	Inne	osoba siedząca na miękkim krześle	0.16	0.35	0.42	0.47	0.52	0.53
87	Inne	Fotele teatralne częściowo wyścielane puste	0.56	0.64	0.70	0.72	0.68	0.62
88	Inne	Krzesło miękkie	0.10	0.12	0.12	0.30	0.25	0.14
89	Inne	Osoba siedząca na miękkim krześle	0.16	0.35	0.42	0.47	0.52	0.53
90	Inne	Krzesła z widownią	0.68	0.75	0.79	0.83	0.87	0.87
91	Inne	Publiczność na krzesłach v.1	0.76	0.83	0.88	0.91	0.91	0.89
92	Inne	Publiczność na widowni (osoba)	0.15	0.25	0.40	0.50	0.60	0.60
93	Inne	Krzesło twarde	0.02	0.03	0.03	0.04	0.04	0.04
94	Inne	Krzesło miękkie	0.10	0.12	0.12	0.30	0.25	0.14
95	Inne	Meble drewniane: stoły, krzesła, regał, szafki, biurko	0.35	0.40	0.45	0.45	0.60	0.60
96	Inne	Fotel bujany	0.04	0.04	0.07	0.06	0.06	0.07
97	Podłogi	Lite drewno na twardym podłożu	0.02	0.04	0.05	0.06	0.06	0.05
98	Podłogi	Chropowata posadzka kamienna, piaskowiec	0.02	0.02	0.03	0.04	0.05	0.05
99	Podłogi	Deski na legarach	0.15	0.11	0.10	0.07	0.06	0.07
100	Podłogi	Drewno lub płyta wiórowa grubości 19mm na legarach lub listwach	0.15	0.11	0.10	0.07	0.06	0.05
101	Podłogi	Dywan długowłosy na betonie	0.09	0.08	0.21	0.26	0.27	0.37
102	Podłogi	Dywan na piance poliuretanowej	0.30	0.35	0.35	0.65	0.62	0.75
103	Podłogi	Dywan tłoczony, 5mm na miękkim podłożu	0.11	0.09	0.06	0.15	0.30	0.40
104	Podłogi	Dywan tłoczony, 5mm na twardym podłożu	0.01	0.02	0.05	0.15	0.30	0.40
105	Podłogi	Dywan wyplatany, 6mm na miękkim podłożu	0.13	0.16	0.26	0.31	0.33	0.44
106	Podłogi	Dywan wyplatany, 6mm na miękkim podłożu z izolacją	0.18	0.17	0.31	0.60	0.75	0.80
107	Podłogi	Dywan wyplatany, 6mm na twardym podłożu	0.03	0.09	0.25	0.31	0.33	0.44
108	Podłogi	Dywan wyplatany, 6mm na twardym podłożu z izolacją	0.08	0.10	0.30	0.60	0.75	0.80
109	Podłogi	Dywan z nylonu, 2mm na miękkim podłożu	0.11	0.09	0.04	0.05	0.08	0.10
110	Podłogi	Dywan z nylonu, 2mm na twardym podłożu	0.01	0.02	0.03	0.05	0.08	0.10
111	Podłogi	Dywan z przędzy włosowej	0.07	0.11	0.19	0.30	0.39	0.41
112	Podłogi	Gładka posadzka kamienna, płytki ceramiczne	0.01	0.01	0.02	0.02	0.03	0.03
113	Podłogi	Guma na miękkim podłożu	0.12	0.10	0.05	0.04	0.02	0.02
114	Podłogi	Guma na twardym podłożu	0.02	0.03	0.04	0.04	0.02	0.02
115	Podłogi	Lawa bazaltowa o grubości płyt 20 mm	0.06	0.13	0.17	0.20	0.22	0.24
116	Podłogi	Linoleum	0.02	0.03	0.03	0.04	0.06	0.05
117	Inne	Chór (<= 0,5 m² / osoba)	0.15	0.25	0.40	0.50	0.60	0.60
118	Inne	Dziecko w przedszkolu (2 m² / osoba)	0.03	0.14	0.17	0.20	0.30	0.23
119	Inne	Krzesła drewniane teatralne całkowicie zapełnione	0.50	0.30	0.40	0.76	0.80	0.76
120	Inne	Krzesła drewniane teatralne puste	0.03	0.04	0.05	0.07	0.08	0.08
121	Inne	Krzesła drewniane teatralne w 2/3 zajete	0.34	0.21	0.28	0.53	0.56	0.53
122	Inne	Krzesła w rzędach w odstępach od 0,9 m do 1,2 m (drewno, tworzywo sztuczne)	0.06	0.08	0.10	0.12	0.14	0.16
123	Inne	Krzesła z fabryczną tapicerką, puste	0.49	0.66	0.80	0.88	0.82	0.70
124	Inne	Krzesła z fabryczną tapicerką, zapełnione	0.60	0.74	0.88	0.96	0.93	0.85
125	Inne	Ławki drewniane całkowicie zapełnione	0.50	0.56	0.66	0.76	0.80	0.76
126	Inne	Ławki drewniane, proste	0.10	0.09	0.08	0.08	0.08	0.08
127	Inne	Ławki drewniane, w 2/3 zajęte	0.37	0.40	0.47	0.53	0.56	0.53
128	Inne	Ławki z wyścielanymi siedzeniami i oparciami całkowicie zapełnione	0.50	0.64	0.76	0.86	0.86	0.76
129	Inne	Ławki z wyścielanymi siedzeniami i oparciami puste	0.32	0.40	0.42	0.44	0.43	0.48
130	Inne	Ławki z wyścielanymi siedzeniami i oparciami w 2/3 zajęte	0.44	0.56	0.65	0.72	0.72	0.67
131	Inne	Łóżka szpitalne, składane 	0.60	0.70	0.80	0.90	1.00	1.00
132	Inne	Meble biurowe	0.25	0.15	0.07	0.05	0.05	0.05
133	Inne	Meble biurowe + osoby siedząca (6 m² / osoba)	0.37	0.33	0.42	0.61	0.73	0.79
134	Inne	Muzyk z instrumentem (1,1 m² / osoba)	0.16	0.42	0.87	1.07	1.04	0.94
135	Inne	Muzyk z instrumentem (2,3 m² / osoba)	0.03	0.13	0.43	0.70	0.86	0.99
136	Inne	Osoba dorosła	0.25	0.35	0.42	0.46	0.50	0.50
\.


--
-- TOC entry 3377 (class 0 OID 16651)
-- Dependencies: 218
-- Data for Name: norms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.norms (pkey, name) FROM stdin;
1	Sale i pracownie szkolne, sale audytoryjne, wykładowe w szkołach podstawowych,średnich i wyższych, pomieszczenia do nauki przedmiotów ogólnych w szkołach muzycznych i inne pomieszczenia o podobnym przeznaczeniu
2	Sale w żłobkach i przedszkolach
3	Świetlice szkolne
4	Sale konsumpcyjne w stołówkach szkolnych
5	Pokoje nauczycielskie, socjalne i inne pomieszczenia o podobnym przeznaczeniu w szkołach i przedszkolach
6	Pracownie do zajęć technicznych i warsztaty szkolne
7	Szatnie w szkołach i przedszkolach, w których ubrania zamknięte są w szafkach z pełnymi drzwiami
8	Czytelnie, wypożyczalnie oraz pomieszczenia księgozbiorów z wolnym dostępem w bibliotekach
9	Sale gimnastyczne, hale sportowe i inne pomieszczenia o podobnym przeznaczeniu
10	Hale basenowe pływalni, parków wodnych i innych obiektów o podobnym przeznaczeniu
11	Sale rozpraw sądowych, sale konferencyjne, audytoria i inne pomieszczenia o podobnym przeznaczeniu
12	Biura wielkoprzestrzenne, pomieszczenia biurowe typu "open space", sale operacyjne banków i urzędów, biura obsługi klienta oraz inne pomieszczenia o podobnym przeznaczeniu
13	Centra obsługi telefonicznej
14	Pokoje biurowe i inne pomieszczenia o zbliżonej funkcji
15	Gabinety lekarskie i zabiegowe oraz inne pomieszczenia o podobnym przeznaczeniu
16	Sale chorych na oddziałach intensywnej opieki medycznej
17	Poczekalnie i punkty przyjęć w szpitalach i przychodniach lekarskich
18	Korytarze w przedszkolach, szkołach podstawowych, gimnazjach i szkołach ponadgimnazjalnych
19	Korytarze w hotelach, szpitalach i przychodniach lekarskich
20	Klatki schodowe w przedszkolach, szkołach, obiektach służby zdrowia i administracji publicznej
21	Kuchnie i pomieszczenia zaplecza gastronomicznego (z wyjatkiem magazynów)
22	Atria, hole, foyer i inne pomieszczenia o podobnym przeznaczeniu, wielokondygnacyjne strefy komunikacji ogólnej w centrach handlowych
23	Terminale pasażerskie portów lotniczych, dworce kolejowe i autobusowe: obszary komunikacji ogólnej, strefy odpraw pasażerów, odbioru bagażu, kas i informacji, poczekalnie
24	Galerie wystawowe, sale ekspozycyjne w muzeach i inne pomieszczenia o podobnym przeznaczeniu
\.


--
-- TOC entry 3378 (class 0 OID 16659)
-- Dependencies: 219
-- Data for Name: norms_absorption_multiplayer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.norms_absorption_multiplayer (norm_id, absorption_multiplayer) FROM stdin;
6	0.60
7	0.60
18	1.00
20	0.40
12	1.10
13	1.30
16	0.80
17	0.80
19	0.60
21	0.60
\.


--
-- TOC entry 3381 (class 0 OID 16683)
-- Dependencies: 222
-- Data for Name: norms_reverb_time_height_req; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.norms_reverb_time_height_req (norm_id, h_less_4, h_between_4_16, h_more_16) FROM stdin;
8	0.60	0.80	0.80
22	1.20	1.50	1.80
23	1.20	1.50	1.80
24	1.50	2.00	2.50
\.


--
-- TOC entry 3379 (class 0 OID 16667)
-- Dependencies: 220
-- Data for Name: norms_reverb_time_no_req; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.norms_reverb_time_no_req (norm_id, no_cubature_req) FROM stdin;
2	0.40
3	0.60
4	0.60
5	0.60
14	0.60
15	0.80
\.


--
-- TOC entry 3380 (class 0 OID 16675)
-- Dependencies: 221
-- Data for Name: norms_reverb_time_volume_req; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.norms_reverb_time_volume_req (norm_id, less_120, between_120_250, between_250_500, between_500_2000, more_2000, less_5000, more_5000) FROM stdin;
1	0.60	0.60	0.80	1.00	99.90	\N	\N
9	1.50	1.50	1.50	1.50	\N	1.50	1.80
10	1.80	1.80	1.80	1.80	\N	1.80	2.20
11	0.80	0.80	0.80	1.00	99.90	\N	\N
\.


--
-- TOC entry 3382 (class 0 OID 16691)
-- Dependencies: 223
-- Data for Name: norms_speech_transmission_index; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.norms_speech_transmission_index (norm_id, between_120_250, between_250_500, between_500_2000, more_2000) FROM stdin;
1	\N	0.60	0.60	99.90
11	0.60	0.60	0.60	99.90
\.


--
-- TOC entry 3386 (class 0 OID 16753)
-- Dependencies: 227
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (id, user_id, name, norm_id, up_to_norm, length, width, height, floor, sufit_id, wall1_id, wall2_id, wall3_id, wall4_id, furniture, _120, _250, _500, _1000, _2000, _4000, reverb_time_120, reverb_time_250, reverb_time_500, reverb_time_1000, reverb_time_2000, reverb_time_4000, requirements) FROM stdin;
13	1	test 2	8	Czas poglosu jest niezgodny z norma	12.00	12.00	12.00	103.00	24	13	11	12	9	[["Axam Acoustic 2.16m2", 2], ["Axam Acoustic 2.88m2", 3], ["Axam Acoustic 3.24m2", 4], ["Axam Acoustic 4.32m2", 5]]	160.21	198.53	215.04	227.15	273.84	294.57	1.74	1.40	1.29	1.22	1.02	0.94	Dla pomieszczenia o wysokosci wiekszej od 4, T musi byc mniejsze badz rowne 0.8s
14	1	test4	24	Pomieszczenie spelnia wymagana norme	2.00	3.00	4.00	106.00	21	15	12	10	12	[["Alpha ClassFrames", 3], ["Axam Acoustic 1.44m2 ", 4], ["Axam Acoustic 2.16m2", 5]]	9.51	13.53	21.60	29.43	31.62	31.92	0.41	0.29	0.18	0.13	0.12	0.12	Dla pomieszczenia o wysokosci mniejszej badz rownej 4, T musi byc mniejsze badz rowne 1.5s
15	1	test 5	16	Pomieszczenie spelnia wymagana norme	2.00	2.00	2.00	105.00	31	11	2	14	12	[["Alpha ClassFrames", 2], ["Axam Acoustic 2.16m2", 3]]	4.71	7.29	11.02	12.57	13.46	13.74	0.27	0.18	0.12	0.10	0.10	0.09	Dla kazdego pomieszczenia A musi byc wieksze badz rowne 0.8 * S
16	1	test 3	13	Chlonnosc akustyczna jest niezgodna z norma	2.00	3.00	2.00	101.00	23	14	11	10	6	[["Alpha ClassFrames", 2], ["Axam Acoustic 1.44m2 ", 3], ["Axam Acoustic 2.88m2", 4]]	8.69	13.43	18.34	23.15	26.08	26.37	0.22	0.14	0.11	0.08	0.07	0.07	Dla kazdego pomieszczenia A musi byc wieksze badz rowne 1.3 * S
\.


--
-- TOC entry 3384 (class 0 OID 16710)
-- Dependencies: 225
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password, first_name) FROM stdin;
1	12345@wp.pl	sha256$0xGEy1dLgPoOnl0E$61ddc42041706e3c47b1bed473d6ad7b2af1af6e7585b79e6d5e3100302e9d21	Dorian
\.


--
-- TOC entry 3396 (class 0 OID 0)
-- Dependencies: 214
-- Name: materials_pkey_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materials_pkey_seq', 1, false);


--
-- TOC entry 3397 (class 0 OID 0)
-- Dependencies: 215
-- Name: materials_pkey_seq1; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materials_pkey_seq1', 136, true);


--
-- TOC entry 3398 (class 0 OID 0)
-- Dependencies: 217
-- Name: norms_pkey_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.norms_pkey_seq', 24, true);


--
-- TOC entry 3399 (class 0 OID 0)
-- Dependencies: 226
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_id_seq', 16, true);


--
-- TOC entry 3400 (class 0 OID 0)
-- Dependencies: 224
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- TOC entry 3214 (class 2606 OID 16649)
-- Name: materials materials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_pkey PRIMARY KEY (pkey);


--
-- TOC entry 3216 (class 2606 OID 16658)
-- Name: norms norms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.norms
    ADD CONSTRAINT norms_pkey PRIMARY KEY (pkey);


--
-- TOC entry 3222 (class 2606 OID 16762)
-- Name: projects projects_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_name_key UNIQUE (name);


--
-- TOC entry 3224 (class 2606 OID 16760)
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- TOC entry 3218 (class 2606 OID 16717)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 3220 (class 2606 OID 16715)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3225 (class 2606 OID 16662)
-- Name: norms_absorption_multiplayer norms_absorption_multiplayer_norm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.norms_absorption_multiplayer
    ADD CONSTRAINT norms_absorption_multiplayer_norm_id_fkey FOREIGN KEY (norm_id) REFERENCES public.norms(pkey);


--
-- TOC entry 3228 (class 2606 OID 16686)
-- Name: norms_reverb_time_height_req norms_reverb_time_height_req_norm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.norms_reverb_time_height_req
    ADD CONSTRAINT norms_reverb_time_height_req_norm_id_fkey FOREIGN KEY (norm_id) REFERENCES public.norms(pkey);


--
-- TOC entry 3226 (class 2606 OID 16670)
-- Name: norms_reverb_time_no_req norms_reverb_time_no_req_norm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.norms_reverb_time_no_req
    ADD CONSTRAINT norms_reverb_time_no_req_norm_id_fkey FOREIGN KEY (norm_id) REFERENCES public.norms(pkey);


--
-- TOC entry 3227 (class 2606 OID 16678)
-- Name: norms_reverb_time_volume_req norms_reverb_time_volume_req_norm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.norms_reverb_time_volume_req
    ADD CONSTRAINT norms_reverb_time_volume_req_norm_id_fkey FOREIGN KEY (norm_id) REFERENCES public.norms(pkey);


--
-- TOC entry 3229 (class 2606 OID 16694)
-- Name: norms_speech_transmission_index norms_speech_transmission_index_norm_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.norms_speech_transmission_index
    ADD CONSTRAINT norms_speech_transmission_index_norm_id_fkey FOREIGN KEY (norm_id) REFERENCES public.norms(pkey);


--
-- TOC entry 3230 (class 2606 OID 16763)
-- Name: projects projects_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2025-03-18 14:36:48

--
-- PostgreSQL database dump complete
--

