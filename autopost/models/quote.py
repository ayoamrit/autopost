from dataclasses import dataclass
from typing import Optional

@dataclass
class Quote:
    doc_id: str
    text: str
    author: str
    
    # This field might have a value, might be empty (either string or nothing)
    category: Optional[str]
    used: bool