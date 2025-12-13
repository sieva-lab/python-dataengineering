import csv
from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Dict, Iterable, Optional, Set

@dataclass()
class Customer:
    customer_id: int
    first_name: str
    last_name: Optional[str]
    email: str
    phone: Optional[str]
    signup_date: Optional[str]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

def parse_customer(parts: Dict[str, str], line_number: int, line: str) -> Customer:

    if len(parts) != 6:
        logger.warning("Ongeldige regel %s: %s", line_number, line.strip())
        return
       
    try:
        customer = Customer(
            customer_id=int(parts["customer_id"]),
            first_name=parts["first_name"].strip(),
            last_name=parts["last_name"].strip() if raw["last_name"].strip() else None,
            email=parts["email"].strip(),
            phone=parts["phone"].strip() if parts["phone"].strip() else None,
            signup_date=parts["signup_date"].strip() if parts["signup_date"].strip() else None,
            raw_line_number=line_number,
        )
        return customer
    except Exception as exc:
        logger.warning("Fout bij parsen van regel %s: %s", line_number, exc)
        raise


def read_customers(path: Path) -> Iterable[Customer]:
    logger.info("Lezen van klantenbestand uit %s", path)
    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            parts = line.strip().split(",") 
            try:
                yield parse_customer(parts, line_number, line)
            except Exception as exc:
                logger.warning("Fout bij parsen van regel %s: %s", line_number, exc)

# -----------------
# CSV Writer
# -----------------
def write_clean_customers(customers: Dict[str, Customer], output_path: Path) -> None:
    logger.info("Schrijven van %s unieke klanten naar %s", len(customers), output_path)
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
# Deduplicatie en merge
# -----------------
def deduplicate_customers(customers: Iterable[Customer]) -> Dict[str, Customer]:
    """
    Dedupliceer klanten op basis van email (primary) of first+last+phone.
    Houd het eerste record als “master” en vul ontbrekende velden aan.
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
            # Merge ontbrekende velden
            if not master.phone and cust.phone:
                master.phone = cust.phone
            if not master.last_name and cust.last_name:
                master.last_name = cust.last_name
            if not master.signup_date and cust.signup_date:
                master.signup_date = cust.signup_date
            logger.info("Duplicate email gevonden: %s (regel %s)", cust.email, cust.raw_line_number)
        elif composite_key in seen_composite_keys:
            logger.info(
                "Duplicate via composite key gevonden: %s %s %s (regel %s)",
                cust.first_name,
                cust.last_name,
                cust.phone,
                cust.raw_line_number
            )
        else:
            unique_customers[primary_key] = cust
            seen_composite_keys.add(composite_key)

    return unique_customers


def main() -> None: 
    logger.info("Start datacleaning proces")
    input_path = Path("Challenges/Datacleaning/customers_raw.csv")
    output_path = Path("Challenges/Datacleaning/customers_candidate_clean.csv")

    customers = read_customers(input_path)
    clean_customers = deduplicate_customers(customers)
    write_clean_customers(clean_customers, output_path)
    logger.info("Klaar!")




if (__name__) == "__main__":
    main()
