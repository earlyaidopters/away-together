from decimal import Decimal
import pytest
from travel_lab.policy import per_person_total,arrives_before_deadline,group_shortlist

def test_room_tax_fee_arithmetic():
    assert per_person_total(1000,basis='per_room',people=4,rooms=2,tax_rate='.1',fixed_fees=40)==Decimal('560.00')
    assert per_person_total(1200,basis='group',people=3)==Decimal('400.00')
    with pytest.raises(ValueError):per_person_total(100,currency='JPY')
def test_midnight_and_timezones():
    assert arrives_before_deadline('2026-09-20T21:00:00-04:00','2026-09-21T02:00:00+01:00','Europe/Lisbon')
    assert not arrives_before_deadline('2026-09-20T21:01:00-04:00','2026-09-21T02:00:00+01:00','Europe/Lisbon')
    with pytest.raises(ValueError):arrives_before_deadline('2026-09-20T21:00:00','2026-09-21T02:00:00+01:00','Europe/Lisbon')
def test_group_acceptance_requires_all():
    assert group_shortlist(['match','match'])=='match'
    assert group_shortlist(['match','review'])=='review'
    assert group_shortlist(['match','decline'])=='decline'
    assert group_shortlist([])=='review'
