from pydantic import BaseModel
from typing import List, Optional

class diet_restrictions(BaseModel):
    username: str
    diet_restrictions: Optional[List[str]] = None
