from typing import List, Dict, Any

def paginate(items: List[Any], limit: int, offset: int) -> Dict[str, Any]:
    """
    Paginates a list of items.
    Args:
        items (List[Any]): The full list of items to paginate.
        limit (int): The maximum number of items to return.
        offset (int): The number of items to skip.
    Returns:
        Dict[str, Any]: Paginated results with total count, limit, and offset.
    """
    total = len(items)
    paginated_items = items[offset: offset + limit]
    return {
        "items": paginated_items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }