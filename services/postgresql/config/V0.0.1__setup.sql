CREATE DATABASE smarthome;
\connect smarthome;
CREATE SCHEMA smarthome;

CREATE ROLE backend LOGIN PASSWORD 'md58f03c909bc9ab63255941fb86a434e27';
ALTER ROLE backend SET search_path TO '$user',smarthome,public;
