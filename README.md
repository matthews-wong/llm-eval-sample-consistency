# llm-eval-sample-consistency

A single run of an LLM eval hides how unstable a model is. This repo scores
**repeated samples** per case instead: how often at least one of k samples is
right (pass@k), how often all k are right (pass^k), and how much the samples
agree with each other.

Stdlib Python, offline. Samples are recorded fixtures; no model is called.

Work in progress: metrics and CLI land in the following commits.
