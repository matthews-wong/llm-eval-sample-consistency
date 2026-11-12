import argparse
import sys
from pathlib import Path

from .dataset import load_cases
from .scoring import CaseScore, score_case, summarize

DEFAULT_K = 3


def format_table(scores: list[CaseScore], k: int) -> str:
    lines = [f"{'case':<14}{'ok/n':>6}{'pass@'+str(k):>9}{'pass^'+str(k):>9}{'agree':>7}  majority"]
    for s in scores:
        lines.append(
            f"{s.id:<14}{f'{s.correct}/{s.n}':>6}{s.pass_at_k:>9.2f}"
            f"{s.pass_pow_k:>9.2f}{s.agreement:>7.2f}  {'yes' if s.majority_correct else 'no'}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sample_eval", description="Score repeated samples per eval case."
    )
    parser.add_argument("cases", type=Path, help="JSONL file of recorded samples")
    parser.add_argument("-k", type=int, default=DEFAULT_K, help="samples drawn for pass@k / pass^k")
    args = parser.parse_args(argv)

    try:
        cases = load_cases(args.cases)
        scores = [score_case(c, args.k) for c in cases]
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(format_table(scores, args.k))
    print()
    summary = summarize(scores)
    print(f"cases={len(scores)} samples_per_case={scores[0].n} k={args.k} (recorded fixture)")
    for name, value in summary.items():
        print(f"{name:<10}{value:.3f}")
    return 0
