REVOKE USAGE ON SCHEMA russify from authenticator;
REVOKE SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA russify from authenticator;
REVOKE USAGE, SELECT ON ALL SEQUENCES IN SCHEMA russify from authenticator;

DROP SCHEMA IF EXISTS russify CASCADE;

DROP ROLE IF EXISTS authenticator;