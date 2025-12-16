from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import csv
import logging
import re
from typing import Optional, Iterable, Dict, Set

# -----------------
# Logging configuration
# -----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------
# Dataclass customer
# -----------------
@dataclass
class Customer:
    customer_id: int
    first_name: str
    last_name: Optional[str]
    email: str
    phone: Optional[str]
    signup_date: Optional[datetime] = None
    raw_line_number: Optional[int] = None  # handig voor logging/debug

    def clean_email(self):
        self.email = self.email.strip().lower()

    def clean_phone(self):
        if self.phone:
            # verwijder alles behalve cijfers
            self.phone = re.sub(r"\D", "", self.phone)
            if not self.phone:
                self.phone = None

    def parse_signup_date(self):
        if self.signup_date:
            try:
                # Probeer ISO-8601 parsing
                if isinstance(self.signup_date, str):
                    self.signup_date = datetime.fromisoformat(self.signup_date)
            except Exception:
                logger.warning(
                    "Invalid signup_date line %s: %s",
                    self.raw_line_number,
                    self.signup_date,
                )
                self.signup_date = None

# -----------------
# Input reader (streaming CSV)
# -----------------
def read_customers(path: Path) -> Iterable[Customer]:
    logger.info("Reading customer file %s", path)
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_number, row in enumerate(reader, start=2):  # start=2 voor header
            try:
                customer = Customer(
                    customer_id=int(row["customer_id"]),
                    first_name=row["first_name"].strip(),
                    last_name=row.get("last_name", "").strip() or None,
                    email=row["email"].strip(),
                    phone=row.get("phone", "").strip() or None,
                    signup_date=row.get("signup_date"),
                    raw_line_number=line_number,
                )
                # Cleaning
                customer.clean_email()
                customer.clean_phone()
                customer.parse_signup_date()
                yield customer
            except Exception as exc:
                logger.warning("Invalid line %s: %s", line_number, exc)

# -----------------
# Deduplication and merge
# -----------------
def deduplicate_customers(customers: Iterable[Customer]) -> Dict[str, Customer]:
    """
    Deduplicate customers based on email (primary) or first+last+phone.
    Keep the first record as "master" and fill in missing fields.
    """
    unique_customers: Dict[str, Customer] = {}
    seen_composite_keys: Set[str] = set()

    for cust in customers:
        # primary key = email
        primary_key = cust.email

        # fallback composite key
        composite_key = f"{cust.first_name.lower()}|{(cust.last_name or '').lower()}|{cust.phone or ''}"

        if primary_key in unique_customers:
            master = unique_customers[primary_key]
            # Merge missing fields
            if not master.phone and cust.phone:
                master.phone = cust.phone
            if not master.last_name and cust.last_name:
                master.last_name = cust.last_name
            if not master.signup_date and cust.signup_date:
                master.signup_date = cust.signup_date
            logger.info("Duplicate email found: %s (line %s)", cust.email, cust.raw_line_number)
        elif composite_key in seen_composite_keys:
            logger.info(
                "Duplicate via composite key found: %s %s %s (line %s)",
                cust.first_name,
                cust.last_name,
                cust.phone,
                cust.raw_line_number
            )
        else:
            unique_customers[primary_key] = cust
            seen_composite_keys.add(composite_key)

    return unique_customers

# -----------------
# CSV Writer
# -----------------
def write_clean_customers(customers: Dict[str, Customer], output_path: Path) -> None:
    logger.info("Writing %s unique customers to %s", len(customers), output_path)
    fieldnames = ["customer_id", "first_name", "last_name", "email", "phone", "signup_date"]
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for cust in customers.values():
            writer.writerow({
                "customer_id": cust.customer_id,
                "first_name": cust.first_name,
                "last_name": cust.last_name or "",
                "email": cust.email,
                "phone": cust.phone or "",
                "signup_date": cust.signup_date.isoformat() if cust.signup_date else "",
            })

# -----------------
# Main
# -----------------
def main() -> None:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent  # root = python/ 
    input_path = BASE_DIR / "challenges" / "datacleaning" / "customers_raw.csv"
    output_path = BASE_DIR / "challenges" / "datacleaning" / "customers_clean.csv"

    customers_gen = read_customers(input_path)
    clean_customers = deduplicate_customers(customers_gen)
    write_clean_customers(clean_customers, output_path)
    logger.info("Finished!")

if __name__ == "__main__":
    main()
