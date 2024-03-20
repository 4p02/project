-- Insert test data for 'users' table
insert into private.users (email, password, fullname)
values
    ('user1@example.com', crypt('password!', gen_salt('bf', 12)), 'John Smith'),
    ('user2@example.com', crypt('password!', gen_salt('bf', 12)), 'Mr. Trudeau'),
    ('user3@example.com', crypt('password!', gen_salt('bf', 12)), 'Margaret Thatcher');

-- Insert test data into private.payments
INSERT INTO private.payments (owner, payment_dates, end_pro)
VALUES
  (1, '{"2024-03-15 10:00:00", "2024-03-16 10:00:00"}', '2024-03-16 10:00:00'),
  (2, '{"2024-03-14 10:00:00", "2024-03-15 10:00:00"}', '2024-03-15 10:00:00'),
  (3, '{"2024-03-13 10:00:00", "2024-03-14 10:00:00"}', '2024-03-14 10:00:00');

-- Insert test data into public.documents
INSERT INTO public.documents (created_at, type, filename, source_url, title, image, body, summary)
VALUES
  ('2024-03-15 10:00:00', 'document', 'doc1.pdf', 'http://example.com/doc1.pdf', 'Document 1', NULL, NULL, NULL),
  ('2024-03-15 10:00:00', 'document', 'doc2.pdf', 'http://example.com/doc2.pdf', 'Document 2', NULL, NULL, NULL),
  ('2024-03-15 10:00:00', 'document', 'doc3.pdf', 'http://example.com/doc3.pdf', 'Document 3', NULL, NULL, NULL);

-- Insert test data into public.links
INSERT INTO public.links (given_link, shortened_link)
VALUES
  ('http://example.com/longlink1', 'http://short.link/abc123'),
  ('http://example.com/longlink2', 'http://short.link/def456'),
  ('http://example.com/longlink3', 'http://short.link/ghi789');

-- Insert test data into private.history
INSERT INTO public.history (user_id, document_id, link_id)
VALUES
  (1, 1, 1),
  (2, 2, 2),
  (3, 3, 3);

-- Insert test data into public.tasks
INSERT INTO public.tasks (created_at, document_id, user_id, task)
VALUES
  ('2024-03-15 10:00:00', 1, 1, 'Task for Document 1'),
  ('2024-03-15 10:00:00', 2, 2, 'Task for Document 2'),
  ('2024-03-15 10:00:00', 3, 3, 'Task for Document 3');
