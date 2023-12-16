from typing import Dict
from datetime import timedelta, datetime

def choose_one(obj: Dict[str, bool]):
    for k, v in obj.items():
        if v:
            return k
        
def get_period(plan_period: str):
    tm_delta = timedelta(days=0)
    monthly = 30
    yearly = 365
    now = datetime.now()
    if plan_period == 'monthly':
        tm_delta = timedelta(days=monthly)
    if plan_period == 'yearly':
        tm_delta = timedelta(days=yearly)
    return now, now + tm_delta