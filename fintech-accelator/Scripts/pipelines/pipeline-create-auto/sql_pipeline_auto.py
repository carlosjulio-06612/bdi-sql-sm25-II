#!/usr/bin/env python3
import os
import sys
import argparse
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('sql_pipeline')

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='PostgreSQL Database Pipeline')
    
    parser.add_argument('--host', default='localhost', 
                        help='PostgreSQL host (default: localhost)')
    parser.add_argument('--port', default=5433, type=int,
                        help='PostgreSQL port (default: 5433)')
    parser.add_argument('--user', required=True,
                        help='PostgreSQL username')
    parser.add_argument('--password', required=True,
                        help='PostgreSQL password')
    parser.add_argument('--db-name', default='fintech_cards',
                        help='Database name to create (default: fintech_cards)')
    parser.add_argument('--schema-name', default='fintech',
                        help='Schema name to create (default: fintech)')
    parser.add_argument('--sql-dir', default='.',
                        help='Directory containing SQL files (default: current directory)')
    parser.add_argument('--use-sql-for-db-creation', action='store_true',
                        help='Use SQL files to create database and schema instead of doing it in code')
    
    return parser.parse_args()

def connect_postgres(host, port, user, password, dbname=None, autocommit=False):
    """Create a connection to PostgreSQL"""
    try:
        # Codificación explícita para evitar problemas con caracteres especiales
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname if dbname else "postgres",
            client_encoding='utf8'
        )
        conn.autocommit = autocommit
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        logger.info(f"Connected to PostgreSQL{' - ' + dbname if dbname else ''}")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
        sys.exit(1)

def database_exists(conn, db_name):
    """Check if database exists"""
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        return cur.fetchone() is not None

def create_database(conn, db_name):
    """Create database if it doesn't exist"""
    if database_exists(conn, db_name):
        logger.info(f"Database '{db_name}' already exists")
        return
    
    try:
        with conn.cursor() as cur:
            # Uso de sql.Identifier para evitar inyección SQL
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        logger.info(f"Database '{db_name}' created successfully")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        sys.exit(1)

def schema_exists(conn, schema_name):
    """Check if schema exists"""
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_namespace WHERE nspname = %s", (schema_name,))
        return cur.fetchone() is not None

def create_schema(conn, schema_name):
    """Create schema if it doesn't exist"""
    if schema_exists(conn, schema_name):
        logger.info(f"Schema '{schema_name}' already exists")
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema_name)))
        logger.info(f"Schema '{schema_name}' created successfully")
    except Exception as e:
        logger.error(f"Error creating schema: {e}")
        sys.exit(1)

def execute_sql_file_old(conn, file_path):
    """Execute SQL commands from file"""
    try:
        # Especificamos la codificación UTF-8 al abrir el archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
        
        # Si el archivo contiene CREATE DATABASE, lo saltamos si ya estamos conectados a la BD
        if "CREATE DATABASE" in sql_commands.upper() and conn.info.dbname != "postgres":
            logger.warning(f"Skipping CREATE DATABASE commands in {file_path} - already connected to a database")
            return
        
        with conn.cursor() as cur:
            cur.execute(sql_commands)
        
        logger.info(f"Successfully executed SQL file: {file_path}")
    except UnicodeDecodeError:
        # Si falla con UTF-8, intentamos con otra codificación
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                sql_commands = f.read()
            
            # Si el archivo contiene CREATE DATABASE, lo saltamos si ya estamos conectados a la BD
            if "CREATE DATABASE" in sql_commands.upper() and conn.info.dbname != "postgres":
                logger.warning(f"Skipping CREATE DATABASE commands in {file_path} - already connected to a database")
                return
                
            with conn.cursor() as cur:
                cur.execute(sql_commands)
            
            logger.info(f"Successfully executed SQL file (using latin-1 encoding): {file_path}")
        except Exception as e:
            logger.error(f"Error executing SQL file {file_path}: {e}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error executing SQL file {file_path}: {e}")
        sys.exit(1)

def execute_sql_file(conn, file_path):
    """Execute SQL commands from file one by one, with clean logging."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            sql_commands = f.read()

    # Separar comandos SQL por ;
    statements = []
    buffer = ""
    for line in sql_commands.splitlines():
        line = line.strip()
        if not line or line.startswith('--'):
            continue
        buffer += " " + line
        if line.endswith(";"):
            statements.append(buffer.strip())
            buffer = ""

    try:
        with conn.cursor() as cur:
            for i, statement in enumerate(statements):
                logger.info(f"Executing SQL statement {i + 1} of {len(statements)}")
                cur.execute(statement)
        logger.info(f"Successfully executed SQL file: {file_path}")
    except Exception as e:
        logger.error(f"Error executing SQL file {file_path}: {e}")
        sys.exit(1)


def get_project_root():
    """
    Intenta determinar el directorio raíz del proyecto.
    Busca subiendo en los directorios hasta encontrar uno que tenga 'scripts'
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Sube en la jerarquía de directorios buscando la carpeta 'scripts'
    while True:
        parent_dir = os.path.dirname(current_dir)
        if os.path.basename(current_dir) == 'scripts' or parent_dir == current_dir:
            # Encontramos la carpeta 'scripts' o llegamos a la raíz
            break
        current_dir = parent_dir
    
    # Si encontramos la carpeta 'scripts', la raíz está un nivel arriba
    if os.path.basename(current_dir) == 'scripts':
        return os.path.dirname(current_dir)
    
    # Si no encontramos 'scripts', usamos el directorio actual
    return os.path.dirname(os.path.abspath(__file__))

def find_sql_files(base_dir, filename):
    """
    Busca recursivamente un archivo SQL específico partiendo desde base_dir
    """
    for root, _, files in os.walk(base_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None

def main():
    """Main function to run the SQL pipeline"""
    args = parse_arguments()
    
    # Imprimir información de depuración
    logger.info(f"Connecting to PostgreSQL at {args.host}:{args.port} with user {args.user}")
    logger.info(f"Using database: {args.db_name}, schema: {args.schema_name}")
    logger.info(f"SQL directory: {args.sql_dir}")
    
    # Determinar ubicación de los archivos SQL
    sql_dir = args.sql_dir
    
    # Si sql_dir es el valor por defecto (.), intentemos ubicar automáticamente los archivos
    if sql_dir == '.':
        # Primero intentamos encontrar la raíz del proyecto
        project_root = get_project_root()
        logger.info(f"Project root determined as: {project_root}")
        
        # Intentamos encontrar los archivos SQL en scripts/ddl
        potential_sql_dir = os.path.join(project_root, 'scripts', 'ddl')
        if os.path.exists(potential_sql_dir):
            sql_dir = potential_sql_dir
            logger.info(f"Found SQL directory at: {sql_dir}")
    
    logger.info(f"Using SQL directory: {sql_dir}")
    
    # Lista de archivos SQL a ejecutar en orden
    creation_file = '01-create-database.sql'
    tables_file = '02-create-tables.sql'
    
    if args.use_sql_for_db_creation:
        # PASO 1: Crear la base de datos, el usuario y esquema desde el script
        # 01-create-database.sql
         
        # Conectar al servidor PostgreSQL
        conn = connect_postgres(args.host, args.port, args.user, args.password,  autocommit=True)
        
        # Verificar si debemos ejecutar el archivo de creación de BD
        db_creation_file = os.path.join(sql_dir, creation_file)
        if os.path.exists(db_creation_file):
            logger.info(f"Executing database creation script: {db_creation_file}")
            execute_sql_file(conn, db_creation_file)
        else:
            logger.warning(f"Database creation script not found: {db_creation_file}")
            # Si no existe el archivo, creamos la BD mediante código
            create_database(conn, args.db_name)
        
        conn.close()
        logger.info("Database created!")
    
    else:
        # PASO 2: Crear las tablas dentro del esquema fintech de la base de datos
        # utiliza el script 02-create-tables.sql
        
        # Conectar a la base de datos creada
        conn = connect_postgres(args.host, args.port, args.user, args.password, args.db_name)
        
        # Crear esquema
        create_schema(conn, args.schema_name)
        
        # Ejecutar archivo de creacion de tablas
        db_tables_file = os.path.join(sql_dir, tables_file)
        
        if not os.path.exists(db_tables_file):
            logger.warning(f"File not found: {db_tables_file}")
        
        logger.info(f"Executing {db_tables_file}")
        execute_sql_file(conn, db_tables_file)
        
        # Cerrar conexión  
        conn.close()
        logger.info("SQL Pipeline completed successfully")

if __name__ == "__main__":
    main()