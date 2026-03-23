from typing import List, Dict, Any

def paginate(items: List[Any], limit: int, offset: int) -> Dict[str, Any]:
   
    total = len(items)
    paginated = items[offset: offset + limit]
    return {
        "items": paginated,
        "total": total,
        "limit": limit,
        "offset": offset,
    }