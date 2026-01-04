# RDW Data Platform

Een eenvoudig data-engineering project op Linux om te begrijpen hoe datapijplijnen in de praktijk werken.

In dit project wordt gebruikgemaakt van openbare RDW-data. Het doel is het opzetten van een kleine, gestructureerde data-omgeving met PostgreSQL, Bash en SQL, gebaseerd op een bronze/silver datamodel.

---

## 🚀 Tech stack
- Linux (Ubuntu via WSL2)
- PostgreSQL Of DuckDB (ik weet het nog niet)
- Bash
- SQL
- Git

---

## 🏗️ Architectuur
Het project volgt een vereenvoudigde medallion-architectuur:

- **Bronze-laag**
  - Ruwe data zoals aangeleverd door de bron
  - Minimale bewerkingen
  - Inclusief ingest-metadata

- **Silver-laag**
  - Opgeschoonde en gestandaardiseerde data
  - Geschikt voor verdere verwerking en analyse

Projectstructuur:
rdw-postgres-platform/
├── data/
│ ├── bronze/
│ └── silver/
├── scripts/
├── sql/
└── docs/


---

## 📊 Databron
Openbare RDW Open Data, bijvoorbeeld:
- Voertuigen (kenteken, merk, voertuigsoort, etc.)

De ruwe databestanden worden bewust **niet** opgenomen in versiebeheer.

---

## 🎯 Doel van het project
- Linux-vaardigheden toepassen in een data-engineering context
- Inzicht krijgen in database-services en file-based ingest
- Werken met bronze/silver datamodellering
- Een basis leggen voor toekomstige uitbreidingen zoals:
  - CI/CD
  - Cloud deployments
  - Infrastructure as Code

---

## 🔒 Data-afhandeling
Ruwe data wordt uitgesloten van Git via `.gitignore`.  
Alleen code en configuratie worden opgeslagen in de repository.

---

## 🔮 Mogelijke uitbreidingen
- Geautomatiseerde ingest via cron of CI/CD
- Containerisatie met Docker
- Cloud deployment met Terraform
- Uitbreiding naar cloud data platforms

---

## 👤 Auteur
Abdullah Ozisik
