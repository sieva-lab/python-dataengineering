Absoluut\! Hier is de volledige programmeeruitdaging, vertaald naar het Engels en samengevoegd in één Markdown-document.

-----

# 🧠 Programming Challenge: Event Processing Pipeline

## 🌟 Context

You are working as a Data Engineer at a company that tracks user behavior through streams of events. These events arrive as **JSON Lines** (e.g., originating from Kafka or a log file). Your task is to build a **reliable and scalable pipeline** that processes, validates, and aggregates these events.

## 📥 Input Dataset

The input file is `events.jsonl` (JSON Lines format), where each line is one independent JSON object.

**Example Data:**

```jsonl
{"user_id": 123, "event_type": "click", "timestamp": "2024-01-01T10:00:00Z"}
{"user_id": 123, "event_type": "purchase", "timestamp": "2024-01-01T10:05:00Z", "amount": 19.99}
{"user_id": 456, "event_type": "click", "timestamp": "2024-01-01T11:00:00Z"}
{"user_id": 123, "event_type": "click", "timestamp": "INVALID_TIMESTAMP"}
{"user_id": 789, "event_type": "purchase", "timestamp": "2024-01-02T12:00:00Z", "amount": -5.00}
```

## 🎯 Objectives

### 1\. Event Validation & Error Handling

The program must validate each event according to the following rules:

  * **`user_id`**: Must be an **integer**.
  * **`event_type`**: Must be a **non-empty string**.
  * **`timestamp`**: Must be a **valid ISO-8601 UTC timestamp**.
  * **Additional rule for `purchase` events:**
      * The `amount` field must be present and have a **positive numeric value**.

**Handling Invalid Events:**

  * Invalid events must be **skipped** for aggregation.
  * **Log** each invalid event with a clear error message (use the standard Python `logging` module).

### 2\. Event Aggregation

Valid events must be aggregated **per unique user (`user_id`) and per day**.

The following statistics must be collected:

  * Total **number of events** (`event_count`)
  * Total **number of purchases** (`purchase_count`)
  * Total **revenue** (`total_revenue`)

### 3\. Output

The aggregated results must be written to a CSV file: `daily_user_stats.csv`.

**Output Columns:**

| date | user\_id | event\_count | purchase\_count | total\_revenue |
| :--- | :--- | :--- | :--- | :--- |

## ⚙️ Technical Requirements

  * **Language/Version:** Python 3.10+
  * **Data Modeling:** Use **dataclasses** (or Pydantic for advanced validation) and **type hints**.
  * **Scalability:** The file may be too large to load entirely into memory. The solution must use a **streaming-like approach** (e.g., generators).
  * **Code Quality:** Code must be readable, modular, and testable.
  * **Error Handling:** Robust use of the `logging` module.

## ⭐ Bonus Points (Optional)

Choose one or more of the following points to enhance the solution:

1.  **Unit Tests:** Provide a set of **Pytest** unit tests for the validation and aggregation logic.
2.  **Modular Architecture:** Separation between I/O (reading/writing), event validation, and the business logic (aggregation).
3.  **Operational Context:** Add a brief explanation of how this pipeline would run operationally (e.g., within **Airflow** or by integrating with **Kafka**).

## 🧪 Skills Tested

This challenge tests your skills in:

  * Data validation & error handling (critical for production code)
  * Efficient processing of large datasets (streaming/generators)
  * Python best practices (type hints, dataclasses/Pydantic)
  * Data modeling (how to design aggregation structures)
  * Production-mindedness (logging, scalability, operational context)