import psycopg2

try:
    conn = psycopg2.connect(
        dbname="bd_job_connect",
        user="postgres",
        password="noxcat48",  # Usa tu contraseña real
        host="localhost"
    )
    print("✅ ¡Conexión exitosa!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")