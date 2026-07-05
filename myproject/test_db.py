import pg8000.native

try:
    con = pg8000.native.Connection(
        user="neondb_owner",
        password="npg_KZT2HEkbBl1P",
        host="ep-long-dew-amfc58va-pooler.c-5.us-east-1.aws.neon.tech",
        port=5432,
        database="flight",
        ssl_context=True
    )
    print("Connection successful!")
    con.close()
except Exception as e:
    print("Connection failed:", type(e), str(e))
