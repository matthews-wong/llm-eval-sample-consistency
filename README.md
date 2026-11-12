# llm-eval-sample-consistency

A single run of an LLM eval hides how unstable a model is. This repo scores
**repeated samples** per case instead: how often at least one of k samples is
right (pass@k), how often all k are right (pass^k), and how much the samples
agree with each other.

Stdlib Python, offline. Samples are recorded fixtures; no model is called.

## Usage

```
python3 -m sample_eval data/samples.jsonl        # k defaults to 3
python3 -m sample_eval data/samples.jsonl -k 1
make validate                                    # tests + fixture eval
```

Input is JSONL, one case per line, with the same number of samples per case:

```json
{"id": "cap-fr", "expected": "Paris", "samples": ["Paris", "Paris.", "Lyon", "Paris", "Paris"]}
```

## Metrics

| metric      | meaning |
|-------------|---------|
| `pass@1`    | mean per-sample accuracy |
| `pass@k`    | unbiased chance that at least one of k samples drawn from the n recorded is correct: `1 - C(n-c, k) / C(n, k)` |
| `pass^k`    | chance that all k drawn samples are correct: `C(c, k) / C(n, k)` |
| `agreement` | share of samples matching the most common answer |
| `majority`  | share of cases where the majority answer is correct (self-consistency vote) |

Answers are compared after case, unicode, whitespace and edge-punctuation
normalization. `k` must not exceed the sample count.

## Reading the numbers

The gap between `pass@k` and `pass^k` is the point. A model can look strong on
pass@3 (a retry or best-of-n would find the answer) while pass^3 shows it is
not reliable enough to run once unattended. Agreement separates "confidently
wrong" cases (high agreement, wrong majority) from noisy ones.

## Fixture result

Run on `data/samples.jsonl`: 12 hand-written cases, 5 recorded samples each,
k=3. These numbers describe the fixture, not any real model.

```
pass@1    0.717
pass@k    0.975
pass^k    0.400
agreement 0.750
majority  0.833
```

## Layout

- `sample_eval/passk.py` estimators
- `sample_eval/consistency.py`, `normalize.py` majority vote and agreement
- `sample_eval/dataset.py` JSONL loader with validation
- `sample_eval/scoring.py`, `report.py` per-case scores and the CLI
- `tests/` run with `python3 -m unittest discover -s tests`
