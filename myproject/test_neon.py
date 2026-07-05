import psycopg2
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    conn = psycopg2.connect(
        host="ep-long-dew-amfc58va-pooler.c-5.us-east-1.aws.neon.tech",
        port=5432,
        dbname="flight",
        user="neondb_owner",
        password="npg_KZT2HEkbBl1P",
        sslmode="require"
    )
    print("Connected! PostgreSQL version:", conn.server_version)
    conn.close()
except Exception as e:
    print(f"Failed: {type(e).__name__}: {e}")
