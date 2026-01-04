import duckdb

# Verbind met je database
con = duckdb.connect(database='data/rdw.duckdb')

print("Views aan het aanmaken...")

# View 1: Alleen personenauto's (meest gebruikte categorie)
con.execute("""
CREATE OR REPLACE VIEW v_personenautos AS
SELECT *
FROM voertuigen
WHERE voertuigsoort = 'Personenauto'
""")

# View 2: Elektrische en hybride voertuigen
con.execute("""
CREATE OR REPLACE VIEW v_elektrisch_hybride AS
SELECT *
FROM voertuigen
WHERE LOWER(handelsbenaming) LIKE '%electric%' 
   OR LOWER(handelsbenaming) LIKE '%ev%'
   OR type_gasinstallatie IN ('E', 'H')  -- E = elektrisch, H = hybride
""")

# View 3: Schone basisview met alleen veelgebruikte kolommen
con.execute("""
CREATE OR REPLACE VIEW v_voertuigen_basis AS
SELECT
    kenteken,
    merk,
    handelsbenaming AS model,
    eerste_kleur,
    tweede_kleur,
    datum_eerste_toelating AS eerste_toelating,
    datum_eerste_tenaamstelling_in_nederland AS eerste_tenaamstelling_nl,
    catalogusprijs,
    cilinderinhoud,
    vermogen_massarijklaar AS vermogen_kw,
    massa_ledig_voertuig,
    aantal_deuren,
    aantal_zitplaatsen,
    zuinigheidsclassificatie
FROM voertuigen
""")

# View 4: Voertuigen per jaar (handig voor trends)
con.execute("""
CREATE OR REPLACE VIEW v_voertuigen_per_jaar AS
SELECT
    strftime('%Y', datum_eerste_toelating) AS jaar,
    COUNT(*) AS aantal_nieuw_toegelaten,
    AVG(catalogusprijs) AS avg_catalogusprijs,
    COUNT(CASE WHEN type_gasinstallatie = 'E' THEN 1 END) AS aantal_elektrisch
FROM voertuigen
WHERE datum_eerste_toelating IS NOT NULL
GROUP BY strftime('%Y', datum_eerste_toelating)
ORDER BY jaar
""")

print("Klaar! Views aangemaakt:")
print("- v_personenautos")
print("- v_elektrisch_hybride")
print("- v_voertuigen_basis")
print("- v_voertuigen_per_jaar")

# Test één view
print("\nVoorbeeld: top 10 merken bij personenauto's")
con.execute("""
SELECT merk, COUNT(*) AS aantal
FROM v_personenautos
GROUP BY merk
ORDER BY aantal DESC
LIMIT 10
""").df()

con.close()