
create table private.payments (
    id bigint generated by default as identity primary key unique not null,
    payment_dates timestamp[] default null,
    end_pro timestamp default null

);

-- Private types (editing is allowed)
create table private.users (
    id bigint generated by default as identity primary key unique not null,
    created_at timestamp with time zone null default now(),
    email text unique not null,
    password text not null,
    fullname text not null,
    pays bigint default null references private.payments(id) ON DELETE CASCADE
);


-- Public types
create type public.article_type as enum('webpage', 'video', 'document');

-- mirror the private table, but strip out password
create view public.users with (security_invoker = true) as (
    select id, created_at, email, fullname from private.users
);

create table public.documents (
    id bigint generated by default as identity primary key unique not null,
    created_at timestamp with time zone null default now(),
    type article_type not null,
    filename text default null,
    source_url text default null,
    file bytea default null,
    title text default null,
    body bytea default null,
    summary bytea default null
);


create table public.links (
    id bigint generated by default as identity primary key unique not null,
    given_link text not null,
    shortened_link text unique not null
);

-- Summerize history of documents
create table private.history (
    user_id bigint not null references private.users(id) ON DELETE CASCADE,
    document_id bigint not null references public.documents(id),
    -- maybe we should store link too?
    link_id bigint not null references public.links(id) ON DELETE CASCADE
);
