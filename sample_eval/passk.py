from math import comb


def _check(n: int, c: int, k: int) -> None:
    if not 0 <= c <= n:
        raise ValueError(f"correct count {c} must be between 0 and n={n}")
    if not 1 <= k <= n:
        raise ValueError(f"k={k} must be between 1 and n={n}")


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased estimate that at least one of k samples drawn from n is correct.

    Uses 1 - C(n-c, k) / C(n, k) rather than (c/n) ** k style shortcuts, which
    are biased when n is small.
    """
    _check(n, c, k)
    return 1.0 - comb(n - c, k) / comb(n, k)


def pass_pow_k(n: int, c: int, k: int) -> float:
    """Estimate that all k samples drawn from n are correct (reliability)."""
    _check(n, c, k)
    return comb(c, k) / comb(n, k)
