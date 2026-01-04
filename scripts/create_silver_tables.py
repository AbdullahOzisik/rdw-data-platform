import duckdb

con = duckdb.connect('data/rdw.duckdb')

print("Silver-tabellen aanmaken...")

# Silver tabel 1: Schone personenauto's met juiste datumconversie
con.execute("""
CREATE OR REPLACE TABLE silver_personenautos AS
SELECT
    kenteken,
    merk,
    handelsbenaming AS model,
    eerste_kleur,
    tweede_kleur,
    
    -- Conversie van bijv. 20200101 (integer) naar echte DATE
    TRY_CAST(
        substr(datum_eerste_toelating::VARCHAR, 1, 4) || '-' ||
        substr(datum_eerste_toelating::VARCHAR, 5, 2) || '-' ||
        substr(datum_eerste_toelating::VARCHAR, 7, 2)
    AS DATE) AS eerste_toelating_datum,
    
    TRY_CAST(
        substr(datum_eerste_tenaamstelling_in_nederland::VARCHAR, 1, 4) || '-' ||
        substr(datum_eerste_tenaamstelling_in_nederland::VARCHAR, 5, 2) || '-' ||
        substr(datum_eerste_tenaamstelling_in_nederland::VARCHAR, 7, 2)
    AS DATE) AS eerste_tenaamstelling_nl,
    
    catalogusprijs,
    cilinderinhoud AS cilinderinhoud_ccm,
    vermogen_massarijklaar AS vermogen_kw,
    aantal_deuren,
    aantal_zitplaatsen,
    zuinigheidsclassificatie,
    type_gasinstallatie AS brandstof_type,
    massa_ledig_voertuig AS gewicht_kg
FROM voertuigen
WHERE voertuigsoort = 'Personenauto'
  AND merk IS NOT NULL
""")

# Silver tabel 2: Elektrische + hybride (geen datumprobleem hier)
con.execute("""
CREATE OR REPLACE TABLE silver_ev_hybride AS
SELECT *
FROM voertuigen
WHERE LOWER(handelsbenaming) LIKE '%electric%' 
   OR LOWER(handelsbenaming) LIKE '%ev%'
   OR type_gasinstallatie IN ('E', 'H')
""")

# Controle
personen_count = con.execute("SELECT COUNT(*) FROM silver_personenautos").fetchone()[0]
ev_count = con.execute("SELECT COUNT(*) FROM silver_ev_hybride").fetchone()[0]

print(f"Silver_personenautos: {personen_count:,} rijen")
print(f"Silver_ev_hybride: {ev_count:,} rijen")

# Bonus: voorbeeld van een paar datums om te checken
print("\nVoorbeeld datums na conversie:")
print(con.execute("""
SELECT kenteken, eerste_toelating_datum, eerste_tenaamstelling_nl 
FROM silver_personenautos 
LIMIT 10
""").df())

con.close()
print("\nKlaar! Silver-tabellen zijn nu aangemaakt zonder fouten.")