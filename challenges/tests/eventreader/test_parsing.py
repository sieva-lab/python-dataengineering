from datetime import datetime, timezone
from eventreader.challenge_eventreader import Event, parse_event
import pytest

# -----------------
# Tests for event parsing           
# -----------------

# Test valid events
def test_valid_click_event():
    raw = {
        "user_id": 123,
        "event_type": "click",
        "timestamp": "2024-01-01T10:00:00Z",
    }
    event = parse_event(raw)
    assert isinstance(event, Event)
    assert event.user_id == 123
    assert event.event_type == "click"
    assert event.amount is None
    assert event.timestamp == datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)

def test_valid_purchase_event():
    raw = {
        "user_id": 456,
        "event_type": "purchase",
        "timestamp": "2024-01-01T12:00:00Z",
        "amount": 25.5
    }
    event = parse_event(raw)
    assert event.user_id == 456
    assert event.event_type == "purchase"
    assert event.amount == 25.5
    assert event.timestamp == datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)

def test_invalid_user_id():
    raw = {"user_id": "abc", "event_type": "click", "timestamp": "2024-01-01T10:00:00Z"}
    with pytest.raises(ValueError):
        parse_event(raw)

def test_invalid_timestamp():
    raw = {"user_id": 1, "event_type": "click", "timestamp": "INVALID"}
    with pytest.raises(ValueError):
        parse_event(raw)

def test_purchase_negative_amount():
    raw = {"user_id": 1, "event_type": "purchase", "timestamp": "2024-01-01T10:00:00Z", "amount": -5}
    with pytest.raises(ValueError):
        parse_event(raw)