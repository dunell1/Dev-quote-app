import random
import requests
from dataclasses import dataclass
from typing import Dict, List, Optional

_DEFAULT_TIMEOUT = 4

@dataclass(frozen=True)
class Quote:
    text: str
    author: str

class QuoteError(RuntimeError):
    pass

_FALLBACK_QUOTES: List[Quote] = [
    Quote("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    Quote("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    Quote("Talk is cheap. Show me the code.", "Linus Torvalds"),
    Quote("The only way to go fast, is to go well.", "Robert C. Martin"),
    Quote("First, solve the problem. Then, write the code.", "John Johnson"),
]

def _from_quotable(topic: str) -> Optional[Quote]:
    tag_map = {
        "Any": None,
        "Programming": "technology",
        "Technology": "technology",
        "Inspiration": "inspirational",
    }
    tag = tag_map.get(topic or "Any")
    params = {}
    if tag:
        params["tags"] = tag
    r = requests.get("https://api.quotable.io/random", params=params, timeout=_DEFAULT_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    content = data.get("content")
    author = data.get("author") or "Unknown"
    if content:
        return Quote(text=content, author=author)
    return None

def _from_progquotes(topic: str) -> Optional[Quote]:
    r = requests.get("https://programming-quotes-api.vercel.app/api/random", timeout=_DEFAULT_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    text = data.get("en") or data.get("quote") or data.get("text")
    author = data.get("author") or "Unknown"
    if text:
        return Quote(text=text, author=author)
    return None

_PROVIDERS = [_from_quotable, _from_progquotes]

def _pick_fallback() -> Quote:
    return random.choice(_FALLBACK_QUOTES)

def get_random_quote(topic: str = "Any") -> Dict[str, str]:
    errors = []
    for provider in _PROVIDERS:
        try:
            q = provider(topic)
            if q:
                return {"text": q.text, "author": q.author}
        except requests.RequestException as e:
            errors.append(str(e))
            continue
    q = _pick_fallback()
    if q:
        return {"text": q.text, "author": q.author}
    raise QuoteError("; ".join(errors) or "No quote available")
