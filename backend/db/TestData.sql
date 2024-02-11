-- Test data for 'users' table
INSERT INTO public.users (created_at, email, password)
VALUES
    ('2024-02-09 08:00', 'user1@example.com', 'password1'),
    ('2024-02-09 08:05', 'user2@example.com', 'password2'),
    ('2024-02-09 08:10', 'user3@example.com', 'password3');

-- Test data for 'webpage' table
INSERT INTO public.webpage (created_at, source_url, body, summary)
VALUES
    ('2024-02-09 08:00', 'http://example1.com', '0x012345', '0x012345'),
    ('2024-02-09 08:05', 'http://example2.com', '0xabcdef', '0xabcdef'),
    ('2024-02-09 08:10', 'http://example3.com', '0x123abc', '0x123abc');

-- Test data for 'videos' table
INSERT INTO public.videos (created_at, source_url, transcript, summary)
VALUES
    ('2024-02-09 08:00', 'http://video1.com', '0x012345', '0x012345'),
    ('2024-02-09 08:05', 'http://video2.com', '0xabcdef', '0xabcdef'),
    ('2024-02-09 08:10', 'http://video3.com', '0x123abc', '0x123abc');

-- Test data for 'documents' table
INSERT INTO public.documents (created_at, filename, body, summary)
VALUES
    ('2024-02-09 08:00', 'document1.txt', '0x012345', '0x012345'),
    ('2024-02-09 08:05', 'document2.txt', '0xabcdef', '0xabcdef'),
    ('2024-02-09 08:10', 'document3.txt', '0x123abc', '0x123abc');

-- Test data for 'articles' table
INSERT INTO public.articles (owner, type, history, private)
VALUES
    (1, 'article', '{1,2}', true),
    (2, 'video', '{2,3}', false),
    (3, 'document', '{1,3}', true);

-- Test data for 'links' table
INSERT INTO public.links (given_link, shortened_link)
VALUES
    ('http://longlink1.com', 'short1'),
    ('http://longlink2.com', 'short2'),
    ('http://longlink3.com', 'short3');
