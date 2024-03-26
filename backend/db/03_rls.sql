-- this function is called by postgrest via the db-pre-request config option.
-- if any exception is raised, the request from that token are rejected.
create or replace function private.check_jwt() returns void as $$
declare
  token json := current_setting('request.jwt.claims', true)::json;
begin
  if not exists(select * from private.users where (id = token->>'uid')) then
    raise insufficient_privilege;
  end if;
end
$$ language plpgsql;

alter table private.users enable row level security;
alter table public.documents enable row level security;
alter table public.links enable row level security;
alter table public.history enable row level security;
alter table private.payments enable row level security;


-- no reason to grant anon access; they can't query or update anything
grant select, update(email, fullname) on public.users to pgrest_auth;
grant select(id, created_at, email, fullname), update(email, fullname) on private.users to pgrest_auth;

-- since the view was created with security_invoker, policies from the
-- impersonated role will be applied (instead of view author's permissions).
-- so, this policy will apply to both private.users and public.users
create policy public_users_rls on private.users as restrictive for select
    using (id = (current_setting('request.jwt.claims', true)::json->>'uid')::int);

grant select on public.history to pgrest_auth;
grant select on public.history to pgrest_anon;
create policy public_history_rls on public.history as restrictive for all
    using (user_id = (current_setting('request.jwt.claims', true)::json->>'uid')::int);


grant select on public.documents to pgrest_auth;
grant select on public.documents to pgrest_anon;
