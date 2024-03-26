create extension if not exists pgcrypto;
create extension if not exists citext;


-- only the public schema is exposed to postgrest
-- public should be autocreated by postgres, but just in case it isn't
create schema if not exists public;
create schema if not exists private;


-- workaround for the lack of `create role if not exists`
-- you may have to run `alter user your_user createrole;` as superuser
do $$
begin
    -- create our postgrest roles:
    -- pgrest_anon, for anonymous access only
    if not exists (select * from pg_catalog.pg_roles where rolname = 'pgrest_anon') then
        create role pgrest_anon nologin noinherit;
        grant pgrest_anon to CURRENT_USER;
    end if;

    -- and pgrest_auth, for authenticated users
    if not exists (select * from pg_catalog.pg_roles where rolname = 'pgrest_auth') then
        create role pgrest_auth nologin noinherit;
        grant pgrest_auth to CURRENT_USER;
    end if;
end
$$ ;


grant usage on schema public to pgrest_anon;
grant usage on schema public to pgrest_auth;
