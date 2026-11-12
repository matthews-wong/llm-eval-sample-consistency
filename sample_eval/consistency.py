from collections import Counter

from .normalize import normalize


def majority(samples: list[str]) -> tuple[str, int]:
    """Most common normalized answer and its count; ties go to the first seen."""
    if not samples:
        raise ValueError("majority needs at least one sample")
    counts = Counter(normalize(s) for s in samples)
    # Counter keeps insertion order, and max() returns the first maximum.
    answer = max(counts, key=counts.__getitem__)
    return answer, counts[answer]


def agreement(samples: list[str]) -> float:
    """Share of samples that match the majority answer, in (0, 1]."""
    _, count = majority(samples)
    return count / len(samples)


def majority_correct(expected: str, samples: list[str]) -> bool:
    """Majority vote (self-consistency) matches the expected answer."""
    answer, _ = majority(samples)
    return answer == normalize(expected)
