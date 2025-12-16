# 🧩 Programming Challenge: Data Cleaning

## 🌟 Context

As a **medior Data Engineer**, your task is to process a raw dataset of customer information coming from multiple sources. The goal is to create a **clean and consistent dataset** that is ready for downstream analytics. The input contains typical data quality issues.

---

## 📥 Input Dataset

You are working with a CSV file, `customers_raw.csv`, with the following columns:

| customer_id | first_name | last_name | email | phone | signup_date |
|------------:|------------|-----------|-------|-------|-------------|
| 1 | John | Doe | john.doe@example.com | 123-456-7890 | 2023-01-15 |
| 2 | Jane | Smith | jane.smith@example.com | | 2023-02-01 |
| 3 | John | Doe | john.doe@example.com | 1234567890 | 2023-01-15 |
| 4 | Bob | | bob@example.com | 987-654-3210 | 2023-03-01 |
| 5 | alice | jones | ALICE.JONES@example.com | 555-555-5555 | 2023-02-20 |

---

## ⚠️ Identified Issues

- **Duplicates:** `customer_id` 1 and 3 refer to the same person.
- **Inconsistent Formatting:** Emails (case sensitivity), phone numbers (different separators).
- **Missing Values:** `last_name` or `phone` may be empty.
- **Invalid Date Formats:** May occur in the `signup_date` field.

---

## 🎯 Objectives

### 1. Data Cleaning & Standardization

- Convert all **emails** to **lowercase**.
- Standardize **phone numbers** to a digits-only format (e.g. `1234567890`).
- Validate that `signup_date` is a valid **ISO-8601** date.  
  **Log** invalid dates and set the field to `NULL`.

### 2. Deduplication & Record Merge

- Identify duplicates based on one of the following unique keys:
  - **Email** (case-insensitive)
  - **OR** the combination of (**first_name** + **last_name** + **phone**)
- **Merge** duplicate records by filling missing fields in the primary record using values from the duplicate record.

---

## 📦 Output

- A clean CSV file: `customers_clean.csv` containing only unique records.
- A log file (`.txt`) containing detected duplicates (which IDs were merged) and invalid data.

---

## ⚙️ Technical Requirements

| Requirement | Description |
|------------|-------------|
| **Language / Version** | Python 3.10+ |
| **Data Modeling** | Use **dataclasses** and **type hints** for customer records |
| **Modularity** | Code must be testable and modular (e.g. separate functions for cleaning, merging, and the pipeline) |
| **Memory Efficiency** | Process large CSV files **line-by-line** (streaming) instead of loading everything into memory |
| **Logging** | Robust logging of all issues (duplicates, missing/invalid fields) |
| **ETL Mindset** | Demonstrate understanding of data flow and error handling |

---

## ⭐ Bonus Points (Optional)

1. **Unique Key**  
   Add a cryptographic **hash** of the customer data as a unique, deterministic key (`unique_hash`).

2. **Output Format**  
   Write the output to **JSON** or **Parquet** (instead of CSV) for improved efficiency in downstream analytics.

3. **Data Quality Metrics**  
   Add a final summary containing metrics such as:
   - Total number of raw records
   - Number of detected duplicates
   - Percentage of missing emails
   - Percentage of invalid `signup_dates`

---

## 🔧 Skills Tested

This challenge evaluates your skills in:

- Data cleaning and standardization (regex / string manipulation)
- Deduplication and merge logic (hash maps / dictionaries)
- Robust CSV and streaming processing (generators)
- Logging and error handling
- Python dataclasses and type hints
- ETL (Extract, Transform, Load) mindset
