# tests/test_aggregation.py
from datetime import datetime, timezone
from eventreader.challenge_eventreader import Event, aggregate_events

def test_aggregate_multiple_events():
    events = [
        Event(user_id=1, event_type="click", timestamp=datetime(2024,1,1,10,0, tzinfo=timezone.utc)),
        Event(user_id=1, event_type="purchase", timestamp=datetime(2024,1,1,11,0, tzinfo=timezone.utc), amount=20.0),
        Event(user_id=2, event_type="click", timestamp=datetime(2024,1,1,12,0, tzinfo=timezone.utc)),
        Event(user_id=1, event_type="purchase", timestamp=datetime(2024,1,2,9,0, tzinfo=timezone.utc), amount=15.0),
        Event(user_id=1, event_type="purchase", timestamp=datetime(2024,1,2,9,0, tzinfo=timezone.utc), amount=10.5)
    ]

    stats = aggregate_events(events)

    # Dag 2024-01-01, user 1
    daily1 = stats[("2024-01-01", 1)]
    assert daily1.event_count == 2
    assert daily1.purchase_count == 1
    assert daily1.total_revenue == 20.0

    # Dag 2024-01-02, user 1
    daily2 = stats[("2024-01-02", 1)]
    assert daily2.event_count == 2
    assert daily2.purchase_count == 2
    assert daily2.total_revenue == 25.5

    # Dag 2024-01-01, user 2
    daily3 = stats[("2024-01-01", 2)]
    assert daily3.event_count == 1
    assert daily3.purchase_count == 0
    assert daily3.total_revenue == 0.0
