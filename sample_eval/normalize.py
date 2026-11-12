import re
import unicodedata

_SPACE = re.compile(r"\s+")
_EDGE_PUNCT = ".,;:!?\"'`"


def normalize(text: str) -> str:
    """Casefold, unify unicode and whitespace, strip edge punctuation."""
    text = unicodedata.normalize("NFKC", text).casefold()
    text = _SPACE.sub(" ", text).strip()
    return text.strip(_EDGE_PUNCT).strip()
