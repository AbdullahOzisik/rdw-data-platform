import duckdb
import pathlib

# Pad naar je project en bestanden
project_dir = pathlib.Path("C:/Users/aozis/rdw-data-platform")  # Windows pad
raw_csv = project_dir / "data" / "raw" / "rdw_data.csv"
db_path = project_dir / "data" / "rdw.duckdb"

print(f"Raw CSV: {raw_csv}")
print(f"Database: {db_path}")

# Verbind met DuckDB (maakt bestand aan als het niet bestaat)
con = duckdb.connect(database=str(db_path))

# Optie 1: Maak een permanente tabel 'voertuigen' door alles in te lezen
print("Laden van CSV naar tabel 'voertuigen'...")
con.execute("""
CREATE OR REPLACE TABLE voertuigen AS 
SELECT * FROM read_csv_auto(
    'data/raw/rdw_data.csv',
    header=true,
    delim=',',
    quote='"',
    escape='"'
)
""")

# Tel hoeveel rijen er zijn geladen
row_count = con.execute("SELECT COUNT(*) FROM voertuigen").fetchone()[0]
print(f"\nGelukt! {row_count:,} rijen geladen in tabel 'voertuigen'")

# Toon een paar voorbeeldrijen
print("\nVoorbeeld van de data:")
df_preview = con.execute("""
SELECT 
    kenteken, 
    merk, 
    handelsbenaming, 
    eerste_kleur, 
    datum_eerste_toelating,
    catalogusprijs
FROM voertuigen 
LIMIT 10
""").df()
print(df_preview)

con.close()
print("\nKlaar! Je kunt nu razendsnel queryen op de tabel 'voertuigen'")