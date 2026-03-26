from typing import Dict, Any
from app.repositories.order_repo import load_all_orders

def get_average_delivery_times() -> Dict[str, Any]:
    """
    Computes average delivery delay per restaurant and system-wide average.
    """
    orders = load_all_orders()

    if not orders:
        #safe default value for empty order list 
        return {"per_restaurant": {}, "system_wide_average_minutes": None}

    restaurant_times = {}
    all_times = []

    for order in orders:
        try:
            restaurant_id = order["restaurant_id"]
            delivery_time = order.get("delivery_time")
            if delivery_time is None:
                continue
            delivery_time = float(delivery_time)
            if restaurant_id not in restaurant_times:
                restaurant_times[restaurant_id] = []
            restaurant_times[restaurant_id].append(delivery_time)
            all_times.append(delivery_time)
        except (ValueError, KeyError):
            continue

    per_restaurant = {
        rid: round(sum(times) / len(times), 2)
        for rid, times in restaurant_times.items()
    }

    system_wide = round(sum(all_times) / len(all_times), 2) if all_times else None

    return {
        "per_restaurant": per_restaurant,
        "system_wide_average_minutes": system_wide
    }