# Pipeline para Automatizar la Ejecución de Scripts SQL en PostgreSQL

Este script de Python automatiza la ejecución de archivos SQL para crear bases de datos, esquemas y tablas en PostgreSQL. Es especialmente útil para configurar rápidamente el entorno de base de datos **fintech** para un sistema de tarjetas de crédito.

## Requisitos

- Python 3.6 o superior  
- Biblioteca `psycopg2` para la conexión con PostgreSQL

## Instalación

1. Asegúrate de tener Python instalado en tu sistema.
2. Instala las dependencias:

```bash
pip install psycopg2-binary
```

## Estructura de Archivos

El script busca automáticamente los siguientes archivos SQL:

1. `01-create-database.sql` – Crea el usuario, base de datos y esquema
2. `02-create-tables.sql` – Crea las tablas del sistema
3. `countries.sql` – Opcional: inserta datos en la tabla de países (si existe)

Los archivos deben estar en el directorio especificado mediante `--sql-dir` o, si se omite, serán buscados automáticamente en la estructura del proyecto (por ejemplo, `scripts/ddl`).

---

## 🔄 Ejecución en Dos Pasos

1. Para ejecutar tu script, ve hasta la ruta donde tienes el script, la cual es `pipelines/pipeline-create-auto/`.
2. Activa tu entorno virtual `.\venv\Scripts\activate` y asegurate que las dependencias en el paso de _Instalación_ estén correctamente instaladas.
3. Prueba el script `test_connection` para validar si tu script y conección local es exitosa de la siguiente manera
   
    **Console**
    ```shell
    python .\test_connection.py localhost 5432 postgres your_password
    ``` 
    **Console Output**
    ```shell
    === Testing PostgreSQL Connection ===
    Host: localhost
    Port: 5432
    User: postgres
    Password: *********
    System locale: cp1252
    Python version: 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)]

    Attempting connection method 1 (keyword arguments)...
    ✅ Connection successful (Method 1)!

    Attempting connection method 2 (connection string)...
    ✅ Connection successful (Method 2)!

    Attempting connection method 3 (URI)...
    ✅ Connection successful (Method 3)!
    ```

4. Luego de validar, que el usuario si se puede conectar, viene la creación completa de la base de datos y sus tablas, para lograr esto se requiere que la ejecución se haga en **dos pasos independientes**, uno con el usuario administrador (`postgres`) y otro con el nuevo usuario de la aplicación (`fc_admin`):
   1. **🧩 Paso 1: Crear la base de datos y el esquema (como `postgres`)**
        
        Ejecuta el siguiente script, en una sola linea en la terminar actual, que tiene el entorno virtual activo y en la misma ruta
      ```bash
      python sql_pipeline_auto.py --user postgres --password "your_password" --db-name postgres --sql-dir ../../ddl --use-sql-for-db-creation
      ```
      **Console Output**
      ```shell
      2025-05-01 15:39:44,416 - sql_pipeline - INFO - Connecting to PostgreSQL at localhost:5433 with user postgres
      2025-05-01 15:39:44,416 - sql_pipeline - INFO - Using database: postgres, schema: fintech
      2025-05-01 15:39:44,416 - sql_pipeline - INFO - SQL directory: ../../ddl
      2025-05-01 15:39:44,416 - sql_pipeline - INFO - Using SQL directory: ../../ddl
      2025-05-01 15:39:44,460 - sql_pipeline - INFO - Connected to PostgreSQL
      2025-05-01 15:39:44,460 - sql_pipeline - INFO - Executing database creation script: ../../ddl\01-create-database.sql
      2025-05-01 15:39:44,469 - sql_pipeline - INFO - Executing SQL statement 1 of 6
      2025-05-01 15:39:44,491 - sql_pipeline - INFO - Executing SQL statement 2 of 6
      2025-05-01 15:39:44,776 - sql_pipeline - INFO - Executing SQL statement 3 of 6
      2025-05-01 15:39:44,777 - sql_pipeline - INFO - Executing SQL statement 4 of 6
      2025-05-01 15:39:44,780 - sql_pipeline - INFO - Executing SQL statement 5 of 6
      2025-05-01 15:39:44,782 - sql_pipeline - INFO - Executing SQL statement 6 of 6
      2025-05-01 15:39:44,783 - sql_pipeline - INFO - Successfully executed SQL file: ../../ddl\01-create-database.sql
      2025-05-01 15:39:44,783 - sql_pipeline - INFO - Database created!
      2025-05-01 15:39:44,783 - sql_pipeline - INFO - SQL Pipeline completed successfully
      ``` 
    - Abrir una conexión desde SQL-Shell y validar si la base de datos y el usuario se crearon con la siguiente consulta
      ```sql
      SELECT 'rol' AS tipo, rolname AS nombre
      FROM pg_roles
      WHERE rolname = 'fc_admin'

      UNION ALL

      SELECT 'database' AS tipo, datname AS nombre
      FROM pg_database
      WHERE datname = 'fintech_cards'

      UNION ALL

      SELECT 'schema' AS tipo, schema_name AS nombre
      FROM information_schema.schemata
      WHERE schema_name = 'fintech';
      ```
      **Console Output**
      ```shell
        tipo   |    nombre
        ----------+---------------
        rol      | fc_admin
        database | fintech_cards
        schema   | fintech
        (3 filas)
      ```
   - Este paso ejecuta `01-create-database.sql` dentro de la base `postgres`. Aquí se crea:

     - El nuevo usuario (`fc_admin`)
     - La base de datos `fintech_cards`
     - El esquema `fintech` en esa base
     - Comentarios opcionales
---
   2. **🧩 Paso 2: Crear tablas y cargar datos (como `fc_admin`)**
        
        Ejecuta el siguiente script, en una sola linea en la terminar actual, que tiene el entorno virtual activo y en la misma ruta
      ```bash
      python sql_pipeline_auto.py --user fc_admin --password "password_fintech_user" --db-name fintech_cards --sql-dir ../../ddl
      ```

      **Console Output**
      ```shell
      2025-05-01 15:57:21,283 - sql_pipeline - INFO - Connecting to PostgreSQL at localhost:5433 with user fc_admin
      2025-05-01 15:57:21,283 - sql_pipeline - INFO - Using database: fintech_cards, schema: fintech
      2025-05-01 15:57:21,283 - sql_pipeline - INFO - SQL directory: ../../ddl
      2025-05-01 15:57:21,283 - sql_pipeline - INFO - Using SQL directory: ../../ddl
      2025-05-01 15:57:21,340 - sql_pipeline - INFO - Connected to PostgreSQL - fintech_cards
      2025-05-01 15:57:21,345 - sql_pipeline - INFO - Schema 'fintech' created successfully
      2025-05-01 15:57:21,345 - sql_pipeline - INFO - Skipping ../../ddl\01-create-database.sql - Database already created via code
      2025-05-01 15:57:21,345 - sql_pipeline - INFO - Executing ../../ddl\02-create-tables.sql
      2025-05-01 15:57:21,356 - sql_pipeline - INFO - Executing SQL statement 1 of 19
      2025-05-01 15:57:21,376 - sql_pipeline - INFO - Executing SQL statement 2 of 19
      2025-05-01 15:57:21,379 - sql_pipeline - INFO - Executing SQL statement 3 of 19
      2025-05-01 15:57:21,382 - sql_pipeline - INFO - Executing SQL statement 4 of 19
      2025-05-01 15:57:21,385 - sql_pipeline - INFO - Executing SQL statement 5 of 19
      2025-05-01 15:57:21,388 - sql_pipeline - INFO - Executing SQL statement 6 of 19
      2025-05-01 15:57:21,390 - sql_pipeline - INFO - Executing SQL statement 7 of 19
      2025-05-01 15:57:21,393 - sql_pipeline - INFO - Executing SQL statement 8 of 19
      2025-05-01 15:57:21,395 - sql_pipeline - INFO - Executing SQL statement 9 of 19
      2025-05-01 15:57:21,397 - sql_pipeline - INFO - Executing SQL statement 10 of 19
      2025-05-01 15:57:21,404 - sql_pipeline - INFO - Executing SQL statement 11 of 19
      2025-05-01 15:57:21,406 - sql_pipeline - INFO - Executing SQL statement 12 of 19
      2025-05-01 15:57:21,408 - sql_pipeline - INFO - Executing SQL statement 13 of 19
      2025-05-01 15:57:21,409 - sql_pipeline - INFO - Executing SQL statement 14 of 19
      2025-05-01 15:57:21,410 - sql_pipeline - INFO - Executing SQL statement 15 of 19
      2025-05-01 15:57:21,412 - sql_pipeline - INFO - Executing SQL statement 16 of 19
      2025-05-01 15:57:21,413 - sql_pipeline - INFO - Executing SQL statement 17 of 19
      2025-05-01 15:57:21,414 - sql_pipeline - INFO - Executing SQL statement 18 of 19
      2025-05-01 15:57:21,416 - sql_pipeline - INFO - Executing SQL statement 19 of 19
      2025-05-01 15:57:21,417 - sql_pipeline - INFO - Successfully executed SQL file: ../../ddl\02-create-tables.sql
      2025-05-01 15:57:21,417 - sql_pipeline - WARNING - File not found: ../../ddl\countries.sql
      2025-05-01 15:57:21,418 - sql_pipeline - INFO - SQL Pipeline completed successfully
      ```
      - Abrir una conexión desde SQL-Shell y conectarse con el usuario `fc_admin` y la base de datos `fintech_cards` y validar si las tablas están creadas en el esquema con la siguiente consulta
  
        ```sql
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema = 'fintech';
        ```
        **Console Output**
          ```shell
            table_schema | table_name
            --------------+--------------------
            fintech      | regions
            fintech      | countries
            fintech      | issuers
            fintech      | franchises
            fintech      | merchant_locations
            fintech      | clients
            fintech      | credit_cards
            fintech      | transactions
            fintech      | payment_methods
            (9 filas)
          ```
   - Este paso se conecta directamente a la base `fintech_cards` y ejecuta:

     - `02-create-tables.sql` para crear las tablas.
---

## Opciones Disponibles

- `--host`: Host de PostgreSQL (predeterminado: localhost)
- `--port`: Puerto de PostgreSQL (predeterminado: 5432)
- `--user`: Usuario de PostgreSQL (obligatorio)
- `--password`: Contraseña del usuario (obligatorio)
- `--db-name`: Base de datos a usar o crear (predeterminado: fintech_cards)
- `--schema-name`: Esquema a crear o usar (predeterminado: fintech)
- `--sql-dir`: Ruta donde están los archivos SQL (predeterminado: búsqueda automática)
- `--use-sql-for-db-creation`: Ejecuta el archivo `01-create-database.sql` como parte del proceso

---

## Notas Importantes

- **No ejecutes ambos pasos con el mismo usuario**: el primer paso requiere privilegios administrativos (`postgres`) y el segundo, el usuario creado (`fc_admin`).
- Si `01-create-database.sql` no existe, el script puede crear la base de datos y el esquema directamente desde código (modo alternativo).
- Puedes omitir `countries.sql` si no deseas cargar datos en esta tabla.
- Para mayor seguridad, usa variables de entorno para las credenciales.
