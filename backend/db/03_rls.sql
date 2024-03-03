alter table private.users enable row level security;
alter table public.documents enable row level security;
alter table public.links enable row level security;
alter table private.history enable row level security;


-- no reason to grant anon access; they can't query or update anything
grant select, update(email, fullname) on public.users to pgrest_auth;
grant select(id, created_at, email, fullname), update(email, fullname) on private.users to pgrest_auth;

-- since the view was created with security_invoker, policies from the
-- impersonated role will be applied (instead of view author's permissions).
-- so, this policy will apply to both private.users and public.users
create policy public_users_rls on private.users as restrictive for select
    using (id = (current_setting('request.jwt.claims', true)::json->>'uid')::int);


create policy private_history_rls on private.history as restrictive for all
    using (user_id = (current_setting('request.jwt.claims', true)::json->>'uid')::int);


grant select on public.documents to pgrest_auth;
grant select on public.documents to pgrest_anon;

