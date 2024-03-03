-- test data for 'users' table
insert into private.users (email, password, fullname)
values
    ('user1@example.com', crypt('password!', gen_salt('bf', 12)), 'John Smith'),
    ('user2@example.com', crypt('password!', gen_salt('bf', 12)), 'Mr. Trudeau'),
    ('user3@example.com', crypt('password!', gen_salt('bf', 12)), 'Margaret Thatcher');

-- test data for 'documents' table
insert into public.documents (type, filename, source_url, file, title, body, summary)
values
    ('document', 'document1.txt', null, null, 'my pdf title!', 'Hello world!', null),
    ('document', 'document2.txt', null, null, 'document2.txt', '0xabcdef', null),
    ('document', 'document3.txt', null, null, 'document3.txt', '0x123abc', null),
    ('video', null, 'https://www.youtube.com/watch?v=dqw4w9wgxcq', null, 'rick astley - never gonna give you up', null, null),
    ('video', null, 'http://video2.com', null, '', '0xabcdef', null),
    ('video', null, 'http://video3.com', null, '', '0x123abc', null),
    ('webpage', null, 'https://gist.githubusercontent.com/mattipv4/045239bc27b16b2bcf7a3a9a4648c08a/raw/2411e31293a35f3e565f61e7490a806d4720ea7e/bee%2520movie%2520script', null, null, null, null);

-- -- test data for 'articles' table
-- insert into public.articles (owner, type, history, private)
-- values
--     (1, 'document', '{1,2,3}', true),
--     (2, 'video', '{4,5,6}', false),
--     (3, 'webpage', '{7,8}', true);

-- test data for 'links' table
insert into public.links (given_link, shortened_link)
values
    ('http://longlink1.com', 'short1'),
    ('http://longlink2.com', 'short2'),
    ('http://longlink3.com', 'short3');
