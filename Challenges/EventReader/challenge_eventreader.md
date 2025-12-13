# 🧠 Programmeeruitdaging: Event Processing Pipeline

## 🌟 Context

U werkt als Data Engineer bij een bedrijf dat gebruikersgedrag volgt via streams van events. Deze events komen binnen als **JSON Lines** (bijv. afkomstig uit Kafka of een logbestand). Uw taak is het bouwen van een **betrouwbare en schaalbare pipeline** die deze events verwerkt, valideert en aggregeert.

## 📥 Input Dataset

Het invoerbestand is `events.jsonl` (JSON Lines-formaat), waarbij elke regel één onafhankelijk JSON-object is.

**Voorbeeld data:**

```jsonl
{"user_id": 123, "event_type": "click", "timestamp": "2024-01-01T10:00:00Z"}
{"user_id": 123, "event_type": "purchase", "timestamp": "2024-01-01T10:05:00Z", "amount": 19.99}
{"user_id": 456, "event_type": "click", "timestamp": "2024-01-01T11:00:00Z"}
{"user_id": 123, "event_type": "click", "timestamp": "INVALID_TIMESTAMP"}
{"user_id": 789, "event_type": "purchase", "timestamp": "2024-01-02T12:00:00Z", "amount": -5.00}
```

## 🎯 Doelstellingen

### 1\. Events Validatie & Foutafhandeling

Het programma moet elk event valideren volgens de volgende regels:

  * **`user_id`**: Moet een **integer** zijn.
  * **`event_type`**: Moet een **niet-lege string** zijn.
  * **`timestamp`**: Moet een **geldige ISO-8601 UTC timestamp** zijn.
  * **Aanvullende regel voor `purchase` events:**
      * Het veld `amount` moet aanwezig zijn en een **positieve numerieke waarde** hebben.

**Afhandeling van Ongeldige Events:**

  * Ongeldige events moeten **overgeslagen** worden voor aggregatie.
  * **Log** elk ongeldig event met een duidelijke foutmelding (gebruik de standaard Python `logging` module).

### 2\. Events Aggregatie

Valide events moeten geaggregeerd worden **per unieke gebruiker (`user_id`) en per dag**.

De volgende statistieken moeten verzameld worden:

  * Totaal **aantal events** (`event_count`)
  * Totaal **aantal purchases** (`purchase_count`)
  * Totale **omzet** (`total_revenue`)

### 3\. Output

De geaggregeerde resultaten moeten worden weggeschreven naar een CSV-bestand: `daily_user_stats.csv`.

**Output Kolommen:**

| date | user\_id | event\_count | purchase\_count | total\_revenue |
| :--- | :--- | :--- | :--- | :--- |

## ⚙️ Technische Vereisten

  * **Taal/Versie:** Python 3.10+
  * **Datamodellering:** Gebruik **dataclasses** (of Pydantic voor geavanceerde validatie) en **type hints**.
  * **Schaalbaarheid:** Het bestand is te groot om volledig in het geheugen te laden. De oplossing moet gebruik maken van een **streaming-achtige aanpak** (bijv. generatoren).
  * **Codekwaliteit:** Code moet leesbaar, modulair en testbaar zijn.
  * **Foutafhandeling:** Robuust gebruik van de `logging` module.

## ⭐ Bonuspunten (Optioneel)

Kies één of meer van de volgende punten om de oplossing te verbeteren:

1.  **Unit Tests:** Lever een setje **Pytest** unit tests aan voor de validatie- en aggregatielogica.
2.  **Modulaire Architectuur:** Scheiding tussen I/O (lezen/schrijven), event validatie en de business logic (aggregatie).
3.  **Operationele Context:** Voeg een korte uitleg toe over hoe deze pipeline operationeel zou draaien (bijv. binnen **Airflow** of door integratie met **Kafka**).

## 🧪 Geteste Vaardigheden

Deze uitdaging test uw vaardigheden in:

  * Data validatie & error handling (kritiek voor productiecode)
  * Efficiënt verwerken van grote datasets (streaming/generatoren)
  * Python best practices (type hints, dataclasses/Pydantic)
  * Data modeling (hoe aggregatiestructuren te ontwerpen)
  * Productie-denkwerk (logging, schaalbaarheid, operationele context)