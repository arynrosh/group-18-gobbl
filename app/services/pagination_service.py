from typing import List, Dict, Any

def paginate(items: List[Any], limit: int, offset: int) -> Dict[str, Any]:
   
    total = len(items)
    page = items[offset: offset + limit]
    return {
        "items": page,
        "total": total,
        "limit": limit,
        "offset": offset,
    }