from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

# -----------------
# Logging configuratie
# -----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


# -----------------
# Datamodel
# -----------------
@dataclass(frozen=True)
class Event:
    user_id: int
    event_type: str
    timestamp: datetime
    amount: Optional[float] = None


# -----------------
# Validatie & parsing
# -----------------
def parse_iso_timestamp(value: str) -> datetime:
    """
    Parse ISO-8601 UTC timestamp.
    Verwacht format: 2024-01-01T10:00:00Z
    """
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc)
    except Exception as exc:
        raise ValueError(f"Ongeldige timestamp: {value}") from exc


def parse_event(raw: dict) -> Event:
    if not isinstance(raw.get("user_id"), int):
        raise ValueError("user_id moet een integer zijn")

    event_type = raw.get("event_type")
    if not isinstance(event_type, str) or not event_type:
        raise ValueError("event_type moet een niet-lege string zijn")

    timestamp_raw = raw.get("timestamp")
    if not isinstance(timestamp_raw, str):
        raise ValueError("timestamp ontbreekt of is geen string")

    timestamp = parse_iso_timestamp(timestamp_raw)

    amount = raw.get("amount")
    if event_type == "purchase":
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("purchase event moet een positief amount hebben")
        amount = float(amount)
    else:
        amount = None

    return Event(
        user_id=raw["user_id"],
        event_type=event_type,
        timestamp=timestamp,
        amount=amount,
    )


# -----------------
# Input reader (streaming)
# -----------------
def read_events(path: Path) -> Iterable[Event]:
    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                raw = json.loads(line)
                yield parse_event(raw)
            except Exception as exc:
                logger.warning(
                    "Ongeldig event overgeslagen (regel %s): %s",
                    line_number,
                    exc,
                )


# -----------------
# Aggregatie
# -----------------
AggregationKey = Tuple[str, int]  # (date, user_id)


@dataclass
class DailyStats:
    event_count: int = 0
    purchase_count: int = 0
    total_revenue: float = 0.0


def aggregate_events(events: Iterable[Event]) -> Dict[AggregationKey, DailyStats]:
    stats: Dict[AggregationKey, DailyStats] = {}

    for event in events:
        date_str = event.timestamp.date().isoformat()
        key = (date_str, event.user_id)

        if key not in stats:
            stats[key] = DailyStats()

        daily = stats[key]
        daily.event_count += 1

        if event.event_type == "purchase":
            daily.purchase_count += 1
            daily.total_revenue += event.amount or 0.0

    return stats


# -----------------
# Output writer
# -----------------
def write_csv(
    stats: Dict[AggregationKey, DailyStats],
    output_path: Path,
) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        f.write("date,user_id,event_count,purchase_count,total_revenue\n")

        for (date, user_id), daily in sorted(stats.items()):
            f.write(
                f"{date},{user_id},{daily.event_count},"
                f"{daily.purchase_count},{daily.total_revenue:.2f}\n"
            )


# -----------------
# Main
# -----------------
def main() -> None:
    input_path = Path("Challenges/Eventreader/events.jsonl")
    output_path = Path("Challenges/Eventreader/daily_user_stats.csv")

    logger.info("Start verwerken van events")
    events = read_events(input_path)
    stats = aggregate_events(events)
    write_csv(stats, output_path)
    logger.info("Klaar. Output geschreven naar %s", output_path)


if __name__ == "__main__":
    main()
