from typing import Dict, Any
from app.repositories.statistics_repo import load_all_orders

def get_average_delivery_times() -> Dict[str, Any]:
    """
    Computes average delivery delay per restaurant and system-wide average.
    """
    orders = load_all_orders()

    if not orders:
        #safe default value for empty order list 
        return {"per_restaurant": {}, "system_wide_average_minutes": None}

    restaurant_delays = {}
    all_delays = []

    for order in orders:
        try:
            restaurant_id = order["restaurant_id"]
            delay = float(order["delivery_delay"])

            if restaurant_id not in restaurant_delays:
                restaurant_delays[restaurant_id] = []

            restaurant_delays[restaurant_id].append(delay)
            all_delays.append(delay)
        except (ValueError, KeyError):
            continue

    per_restaurant = {
        rid: round(sum(delays) / len(delays), 2)
        for rid, delays in restaurant_delays.items()
    }

    system_wide = round(sum(all_delays) / len(all_delays), 2) if all_delays else None

    return {
        "per_restaurant": per_restaurant,
        "system_wide_average_minutes": system_wide
    }