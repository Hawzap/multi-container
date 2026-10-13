CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO users (name, email) VALUES
    ('Іван Петренко', 'ivan.petrenko@example.com'),
    ('Олена Коваленко', 'olena.kovalenko@example.com'),
    ('Степан Мельник', 'stepan.melnyk@example.com')
ON CONFLICT (email) DO NOTHING;
