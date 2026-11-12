.PHONY: validate test eval

validate: test eval

test:
	python3 -m unittest discover -s tests

eval:
	python3 -m sample_eval data/samples.jsonl
