import sys
import psycopg2
import locale

def test_connection(host, port, user, password):
    """Test simple connection to PostgreSQL server"""
    print(f"=== Testing PostgreSQL Connection ===")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"User: {user}")
    print(f"Password: {'*' * len(password)}")
    print(f"System locale: {locale.getpreferredencoding()}")
    print(f"Python version: {sys.version}")
    
    # Método 1: Parámetros separados
    try:
        print("\nAttempting connection method 1 (keyword arguments)...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname="postgres"
        )
        print("✅ Connection successful (Method 1)!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed (Method 1): {e}")
        print(f"Error type: {type(e)}")
    
    # Método 2: Cadena de conexión
    try:
        print("\nAttempting connection method 2 (connection string)...")
        conn_string = f"host={host} port={port} user={user} password={password} dbname=postgres"
        conn = psycopg2.connect(conn_string)
        print("✅ Connection successful (Method 2)!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed (Method 2): {e}")
        print(f"Error type: {type(e)}")
    
    # Método 3: Con URI
    try:
        print("\nAttempting connection method 3 (URI)...")
        uri = f"postgresql://{user}:{password}@{host}:{port}/postgres"
        conn = psycopg2.connect(uri)
        print("✅ Connection successful (Method 3)!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed (Method 3): {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python test_postgres_connection.py <host> <port> <user> <password>")
        sys.exit(1)
    
    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    
    test_connection(host, port, user, password)