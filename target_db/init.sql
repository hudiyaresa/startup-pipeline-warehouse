CREATE DATABASE staging;

-- Staging table for acquisition data
CREATE TABLE public.acquisition (
    acquisition_id integer NOT NULL,
    acquiring_object_id character varying(255),
    acquired_object_id character varying(255),
    term_code character varying(255),
    price_amount numeric(15,2),
    price_currency_code character varying(3),
    acquired_at timestamp without time zone,
    source_url text,
    source_description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

-- Staging table for company data
CREATE TABLE public.company (
    office_id integer NOT NULL,
    object_id character varying(255),
    description text,
    region character varying(255),
    address1 text,
    address2 text,
    city character varying(255),
    zip_code character varying(200),
    state_code character varying(255),
    country_code character varying(255),
    latitude numeric(9,6),
    longitude numeric(9,6),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

-- Staging table for funding rounds data
CREATE TABLE public.funding_rounds (
    funding_round_id integer NOT NULL,
    object_id character varying(255),
    funded_at date,
    funding_round_type character varying(255),
    funding_round_code character varying(255),
    raised_amount_usd numeric(15,2),
    raised_amount numeric(15,2),
    raised_currency_code character varying(255),
    pre_money_valuation_usd numeric(15,2),
    pre_money_valuation numeric(15,2),
    pre_money_currency_code character varying(255),
    post_money_valuation_usd numeric(15,2),
    post_money_valuation numeric(15,2),
    post_money_currency_code character varying(255),
    participants text,
    is_first_round boolean,
    is_last_round boolean,
    source_url text,
    source_description text,
    created_by character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

-- Staging table for funds data
CREATE TABLE public.funds (
    fund_id character varying(255) NOT NULL,
    object_id character varying(255),
    name character varying(255),
    funded_at date,
    raised_amount numeric(15,2),
    raised_currency_code character varying(3),
    source_url text,
    source_description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

-- Staging table for investments data
CREATE TABLE public.investments (
    investment_id integer NOT NULL,
    funding_round_id integer,
    funded_object_id character varying,
    investor_object_id character varying,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

-- Staging table for IPOs data
CREATE TABLE public.ipos (
    ipo_id character varying(255) NOT NULL,
    object_id character varying(255),
    valuation_amount numeric(15,2),
    valuation_currency_code character varying(3),
    raised_amount numeric(15,2),
    raised_currency_code character varying(3),
    public_at timestamp without time zone,
    stock_symbol character varying(255),
    source_url text,
    source_description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

-- Staging table for people data
CREATE TABLE public.people (
    people_id integer NOT NULL,
    object_id character varying(255),
    first_name character varying(255),
    last_name character varying(255),
    birthplace text,
    affiliation_name text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

-- Staging table for relationships data
CREATE TABLE public.relationships (
    relationship_id integer NOT NULL,
    person_object_id character varying(255),
    relationship_object_id character varying(255),
    start_at timestamp without time zone,
    end_at timestamp without time zone,
    is_past boolean,
    sequence integer,
    title character varying(255),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


CREATE DATABASE etl_log;
