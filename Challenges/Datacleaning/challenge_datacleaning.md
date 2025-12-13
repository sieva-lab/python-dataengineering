# 🧩 Programmeeruitdaging: Data Cleaning

## 🌟 Context

Als medior Data Engineer is het uw taak om een ruwe dataset van klantinformatie uit verschillende bronnen te verwerken. Het doel is om een **schone en consistente dataset** te creëren die klaar is voor downstream analytics. De invoer bevat typische 'data quality' problemen.

## 📥 Input Dataset

U werkt met een CSV-bestand, `customers_raw.csv`, met de volgende kolommen:

| customer\_id | first\_name | last\_name | email | phone | signup\_date |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | John | Doe | john.doe@example.com | 123-456-7890 | 2023-01-15 |
| 2 | Jane | Smith | jane.smith@example.com | | 2023-02-01 |
| 3 | John | Doe | john.doe@example.com | 1234567890 | 2023-01-15 |
| 4 | Bob | | bob@example.com | 987-654-3210 | 2023-03-01 |
| 5 | alice | jones | ALICE.JONES@example.com | 555-555-5555 | 2023-02-20 |

### ⚠️ Geïdentificeerde Problemen

* **Duplicaten:** `customer_id` 1 en 3 refereren dezelfde persoon.
* **Inconsistente Formatting:** E-mail (case-sensitief), Telefoonnummers (verschillende scheidingstekens).
* **Ontbrekende Waarden:** `last_name` of `phone` kunnen leeg zijn.
* **Ongeldige Datumformaten:** Kan voorkomen in de `signup_date`.

## 🎯 Doelstellingen

### 1. Data Cleaning & Standaardisatie

* Alle **e-mails** converteren naar **lowercase**.
* **Telefoonnummers** standaardiseren naar een formaat met alleen cijfers (bijv., `1234567890`).
* Controleren of `signup_date` een geldige **ISO-8601** datum is. **Log** ongeldige datums en zet het veld op `NULL`.

### 2. Deduplicatie & Record Merge

* Identificeer duplicaten op basis van één van de volgende unieke sleutels:
    * **Email** (case-insensitive)
    * **OF** de combinatie van (**first\_name** + **last\_name** + **phone**)
* **Combineer** dubbele records: vul ontbrekende velden in de primaire record aan met waarden uit het duplicaat.

## 📦 Output

* Een schone CSV: `customers_clean.csv` met uitsluitend unieke records.
* Een logbestand (`.txt`) met gedetecteerde duplicaten (welke ID's zijn samengevoegd) en ongeldige data.

## ⚙️ Technische Vereisten

| Vereiste | Beschrijving |
| :--- | :--- |
| **Taal/Versie** | Python 3.10+ |
| **Datamodellering** | Gebruik **dataclasses** en **Type Hints** voor klantrecords. |
| **Modulariteit** | Code moet testbaar en modulair zijn (bijv. aparte functies voor cleaning, merging, en de pipeline). |
| **Geheugenefficiëntie** | Verwerk grote CSV's **line-by-line** (streaming) in plaats van alles in het geheugen te laden. |
| **Logging** | Robuuste logging van alle issues (duplicaten, ontbrekende/invalide velden). |
| **ETL Mindset** | Toon inzicht in data flow en foutafhandeling. |

## ⭐ Bonuspunten (Optioneel)

1.  **Unique Key:** Voeg een cryptografische **hash** van de klantdata toe als unieke, deterministische sleutel (`unique_hash`).
2.  **Output Format:** Schrijf de output weg naar **JSON** of **Parquet** (in plaats van CSV) voor efficiëntie in downstream analytics.
3.  **Data Quality Metrics:** Voeg aan het einde een samenvatting toe met metrics zoals:
    * Totaal aantal ruwe records
    * Aantal gedetecteerde duplicaten
    * Percentage ontbrekende e-mails
    * Percentage ongeldige `signup_dates`

---

## 🔧 Geteste Vaardigheden

Deze uitdaging test uw vaardigheden in:

* Data cleaning / standardization (RegEx/string manipulatie)
* Deduplicatie & merge logica (Hash Map/Dictionary gebruik)
* Robust CSV/streaming processing (Generators)
* Logging & error handling
* Python dataclasses & type hints
* ETL (Extract, Transform, Load) mindset