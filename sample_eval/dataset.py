import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Case:
    id: str
    expected: str
    samples: list[str]


def load_cases(path: Path) -> list[Case]:
    """Read JSONL cases; every case must carry the same number of samples."""
    cases: list[Case] = []
    seen: set[str] = set()
    for lineno, line in enumerate(Path(path).read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            case = Case(row["id"], row["expected"], list(row["samples"]))
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise ValueError(f"{path}:{lineno}: bad case ({exc!r})") from exc
        if case.id in seen:
            raise ValueError(f"{path}:{lineno}: duplicate id {case.id!r}")
        if not case.samples:
            raise ValueError(f"{path}:{lineno}: case {case.id!r} has no samples")
        seen.add(case.id)
        cases.append(case)
    if not cases:
        raise ValueError(f"{path}: no cases")
    sizes = {len(c.samples) for c in cases}
    if len(sizes) > 1:
        raise ValueError(f"{path}: cases have differing sample counts {sorted(sizes)}")
    return cases
