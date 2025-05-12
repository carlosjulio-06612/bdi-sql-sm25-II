-- 1. Show current user and database
SELECT current_user, current_database();

-- 2. Show current search path (schema)
SHOW search_path;

-- 3. Optionally set the schema to 'public'
SET search_path TO public;

-- 4. List all visible tables in the schema
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;

-- 5. Describe a specific table (columns and types)
SELECT *
FROM information_schema.columns
WHERE table_name = 'transactions';

-- 6. View current session details
SELECT * FROM pg_stat_activity
WHERE pid = pg_backend_pid();

-- 7. (Optional) List constraints like primary keys, unique, etc.
SELECT conname, contype, conrelid::regclass AS table_name
FROM pg_constraint
WHERE conrelid::regclass::text = 'fintech.transactions';

-- 8. Count list constraints like primary keys, unique, foreign key, etc
SELECT contype AS type_constraint,
       COUNT(*) AS total_constraints
FROM pg_constraint
WHERE conrelid::regclass::text = 'fintech.transactions'
GROUP BY type_constraint
ORDER BY type_constraint DESC;
