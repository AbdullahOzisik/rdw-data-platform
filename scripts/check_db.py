import duckdb

# Verbind met je database
con = duckdb.connect('data/rdw.duckdb')

# Toon alle tabellen en views
print("Tabellen en views in je database:")
print(con.execute("SHOW TABLES;").df())

# Tel rijen in voertuigen
count = con.execute("SELECT COUNT(*) FROM voertuigen").fetchone()[0]
print(f"\nAantal rijen in voertuigen: {count:,}")

# Test een view
print("\nTop 5 merken uit v_personenautos:")
print(con.execute("SELECT merk, COUNT(*) AS aantal FROM v_personenautos GROUP BY merk ORDER BY aantal DESC LIMIT 5;").df())

con.close()