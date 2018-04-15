--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.5
-- Dumped by pg_dump version 9.6.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: objects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE objects (
    img_id character varying(255),
    box_height double precision,
    box_width double precision,
    box_x double precision NOT NULL,
    box_y double precision NOT NULL,
    label character varying(255),
    score double precision
);


ALTER TABLE objects OWNER TO postgres;

--
-- Data for Name: objects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY objects (img_id, box_height, box_width, box_x, box_y, label, score) FROM stdin;
test_images/image2.jpg	0.0392478704452514648	0.0149138569831848145	0.394223809242248535	0.553876817226409912	person	0.916877999999999971
test_images/image2.jpg	0.0192545056343078613	0.0132057666778564453	0.345824122428894043	0.382946431636810303	kite	0.829444999999999988
test_images/image2.jpg	0.0491851568222045898	0.0170867927372455597	0.0576669983565807343	0.574166655540466309	person	0.778505000000000003
test_images/image2.jpg	0.0859880298376083374	0.0631937384605407715	0.437409102916717529	0.0799144208431243896	kite	0.769985000000000031
test_images/image2.jpg	0.0418922901153564453	0.0219709277153015137	0.201122939586639404	0.265642821788787842	kite	0.755538999999999961
test_images/image2.jpg	0.157207369804382324	0.0393958389759063721	0.0784299373626708984	0.683380782604217529	person	0.634233999999999964
test_images/image2.jpg	0.0156322121620178223	0.0160083770751953125	0.431722164154052734	0.385100245475769043	kite	0.60740700000000003
test_images/image2.jpg	0.176305770874023438	0.0444724857807159424	0.157396554946899414	0.760619640350341797	person	0.589102000000000015
test_images/image2.jpg	0.0195335149765014648	0.011361241340637207	0.256047427654266357	0.542812526226043701	person	0.512376999999999971
test_images/image2.jpg	0.0333569049835205078	0.0143448840826749802	0.0269931424409151077	0.58708113431930542	person	0.501464000000000021
test_images/image1.jpg	0.833019405603408813	0.296558454632759094	0.0192150324583053589	0.0390840470790863037	dog	0.940691000000000055
test_images/image1.jpg	0.815131068229675293	0.570212244987487793	0.402835607528686523	0.109515011310577393	dog	0.934502999999999973
\.


--
-- Name: objects objects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (box_x, box_y);


--
-- PostgreSQL database dump complete
--

