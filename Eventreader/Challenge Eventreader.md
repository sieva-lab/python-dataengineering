🧠 Programmeeruitdaging: Event Processing Pipeline
Context

Je werkt bij een bedrijf dat gebruikersactiviteit bijhoudt via events. Deze events komen binnen als JSON-regels (bijvoorbeeld uit Kafka of een logbestand). Jij moet een betrouwbare en schaalbare data-processing pipeline bouwen.

📥 Input

Een bestand events.jsonl (JSON Lines), waarbij elke regel één event is:

{"user_id": 123, "event_type": "click", "timestamp": "2024-01-01T10:00:00Z"}
{"user_id": 123, "event_type": "purchase", "timestamp": "2024-01-01T10:05:00Z", "amount": 19.99}
{"user_id": 456, "event_type": "click", "timestamp": "2024-01-01T11:00:00Z"}
{"user_id": 123, "event_type": "click", "timestamp": "INVALID_TIMESTAMP"}

🎯 Doel

Schrijf een Python-programma dat:

Events valideert

user_id moet een integer zijn

event_type moet een niet-lege string zijn

timestamp moet een geldige ISO-8601 UTC timestamp zijn

purchase events moeten een positief amount veld hebben

Ongeldige events afvangt

Sla ze over

Log ze met een duidelijke foutmelding (gebruik logging)

Events aggregeert per user per dag

Aantal events

Aantal purchases

Totale omzet

Output schrijft

Naar een CSV-bestand daily_user_stats.csv

Met kolommen:

date,user_id,event_count,purchase_count,total_revenue

⚙️ Technische eisen

Python 3.10+

Gebruik type hints

Gebruik dataclasses of pydantic voor validatie

Code moet leesbaar en testbaar zijn

Ga ervan uit dat het bestand te groot is om volledig in memory te laden

⭐ Bonus (optioneel)

Kies één of meer:

Unit tests (pytest)

Parallel processing (bijv. concurrent.futures)

Streaming-achtige aanpak (generatoren)

Scheiding tussen I/O, validatie en business logic

Uitleg hoe dit zou draaien in Airflow of met Kafka

🧪 Verwachte skills die dit test

Data validatie & error handling

Efficiënt verwerken van grote datasets

Python best practices

Data modeling

Productie-denkwerk (logging, schaalbaarheid)