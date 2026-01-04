import duckdb
import os

# Pad naar je gedownloade CSV (pas aan!)
CSV_PATH = "\rdw-postgres\data\bronze\raw\gekentekende_voertuigen_20260104.csv"

if not os.path.exists(CSV_PATH):
    print("CSV niet gevonden – download eerst!")
else:
    # Maak een in-memory connection (of persistent: duckdb.connect('rdw.duckdb'))
    con = duckdb.connect()

    # Query direct op de CSV – geen import nodig!
    result = con.execute(f"""
        SELECT 
            merk, 
            COUNT(*) AS aantal
        FROM '{CSV_PATH}'
        LIMIT 10
    """).fetchdf()

    print(result)