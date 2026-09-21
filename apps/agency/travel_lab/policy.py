"""Deterministic travel calculations; never delegated to language-model guesses."""
from decimal import Decimal,ROUND_HALF_UP
from datetime import datetime
from zoneinfo import ZoneInfo

def per_person_total(amount,*,basis='per_person',people=1,rooms=1,tax_rate='0',fixed_fees='0',currency='EUR',budget_currency='EUR'):
    if currency!=budget_currency:raise ValueError('Currency conversion requires an explicit verified rate')
    if people<1 or rooms<1:raise ValueError('Party and room counts must be positive')
    value=Decimal(str(amount));tax=Decimal(str(tax_rate));fees=Decimal(str(fixed_fees))
    if min(value,tax,fees)<0:raise ValueError('Negative cost component')
    if basis=='per_person':subtotal=value*people
    elif basis=='per_room':subtotal=value*rooms
    elif basis=='group':subtotal=value
    else:raise ValueError('Unknown price basis')
    return ((subtotal*(1+tax)+fees)/people).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)

def arrives_before_deadline(arrival_iso,deadline_iso,property_zone):
    arrival=datetime.fromisoformat(arrival_iso);deadline=datetime.fromisoformat(deadline_iso)
    if arrival.tzinfo is None or deadline.tzinfo is None:raise ValueError('Explicit timezone offsets are required')
    zone=ZoneInfo(property_zone);return arrival.astimezone(zone)<=deadline.astimezone(zone)

def group_shortlist(statuses):
    if not statuses:return 'review'
    if 'decline' in statuses:return 'decline'
    if 'review' in statuses:return 'review'
    if all(x=='match' for x in statuses):return 'match'
    raise ValueError('Unknown decision state')
