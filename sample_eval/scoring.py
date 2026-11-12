from dataclasses import dataclass

from .consistency import agreement, majority_correct
from .dataset import Case
from .normalize import normalize
from .passk import pass_at_k, pass_pow_k


@dataclass(frozen=True)
class CaseScore:
    id: str
    n: int
    correct: int
    pass_at_k: float
    pass_pow_k: float
    agreement: float
    majority_correct: bool


def score_case(case: Case, k: int) -> CaseScore:
    expected = normalize(case.expected)
    n = len(case.samples)
    correct = sum(normalize(s) == expected for s in case.samples)
    return CaseScore(
        id=case.id,
        n=n,
        correct=correct,
        pass_at_k=pass_at_k(n, correct, k),
        pass_pow_k=pass_pow_k(n, correct, k),
        agreement=agreement(case.samples),
        majority_correct=majority_correct(case.expected, case.samples),
    )


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def summarize(scores: list[CaseScore]) -> dict[str, float]:
    return {
        "pass@1": mean([s.correct / s.n for s in scores]),
        "pass@k": mean([s.pass_at_k for s in scores]),
        "pass^k": mean([s.pass_pow_k for s in scores]),
        "agreement": mean([s.agreement for s in scores]),
        "majority": mean([float(s.majority_correct) for s in scores]),
    }
