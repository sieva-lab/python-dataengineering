# 🐍 Python Data Engineering Challenges

This repository contains a set of **Data Engineering programming challenges** implemented in Python.

The challenges are designed to assess practical skills in **data cleaning**, **event processing**, and **ETL-style pipeline design**, with an emphasis on **scalability**, **data quality**, and **production-ready thinking**.

The project is structured to work seamlessly in **VS Code**.

---

## 📁 Project Structure

```

python/
└── challenges/
├── datacleaning/
│   ├── customers\_raw.csv
│   ├── customers\_clean.csv
│   ├── challenge\_datacleaning.py
│   └── challenge\_datacleaning.md
│
├── eventreader/
│   ├── events.jsonl
│   ├── daily\_user\_stats.csv
│   ├── challenge\_eventreader.py
│   └── challenge\_eventreader.md
│
└── README.md

````

> 📌 **Each challenge is self-contained and includes:**
> * An input dataset
> * A challenge description
> * Expected output files
> * Logging for data quality and error handling

---

## 🧩 Available Challenges

### 1️⃣ Datacleaning: Data Cleaning & Deduplication

**Focus areas:**
* Data standardization (emails, phone numbers, dates)
* Deduplication and record merging
* Streaming CSV processing
* Logging and data quality metrics

**Key concepts tested:**
* Dataclasses & type hints
* Hash-based deduplication
* ETL-style data pipelines 

---

### 2️⃣ Eventreader: Event Processing Pipeline

**Focus areas:**
* Streaming JSON Lines processing
* Event validation and error handling
* Per-user, per-day aggregation
* Scalable pipeline design

**Key concepts tested:**
* Generators and memory-efficient processing
* Validation logic
* Aggregation data modeling
* Production-grade logging

---

## ⚙️ Requirements

* **Python:** 3.10 or higher
* **Recommended Tools:**
    * VS Code
    * Python extension for VS Code
    * Pytest (optional, for bonus unit tests)

---

## ▶️ How to Run

1. Open the project folder in **VS Code**.
2. Create and activate a virtual environment (optional but recommended).
3. Navigate to a challenge directory.
4. Run the corresponding Python script, for example:

```bash
python pipeline.py
````

Output files and logs will be generated in the same challenge folder.

-----

## 🧪 Testing (Optional)

Some challenges include optional unit testing tasks.

To run tests (if provided):

```bash
python -m pytest
```