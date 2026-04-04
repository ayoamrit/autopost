from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from autopost.models.quote import Quote

@dataclass
class Post:
    quote: Quote
    image_path: Optional[Path]
    caption: str
    post_id: Optional[str] = None