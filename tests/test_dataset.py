import tempfile
import unittest
from pathlib import Path

from sample_eval.dataset import load_cases


def load(text: str):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "cases.jsonl"
        path.write_text(text)
        return load_cases(path)


class LoadCasesTest(unittest.TestCase):
    def test_loads_cases_and_skips_blank_lines(self):
        cases = load('{"id":"a","expected":"1","samples":["1","2"]}\n\n')
        self.assertEqual(cases[0].id, "a")
        self.assertEqual(cases[0].samples, ["1", "2"])

    def test_missing_field_names_the_line(self):
        with self.assertRaisesRegex(ValueError, ":1: bad case"):
            load('{"id":"a","samples":["1"]}\n')

    def test_invalid_json_names_the_line(self):
        with self.assertRaisesRegex(ValueError, ":2: bad case"):
            load('{"id":"a","expected":"1","samples":["1"]}\n{oops\n')

    def test_duplicate_id(self):
        row = '{"id":"a","expected":"1","samples":["1"]}\n'
        with self.assertRaisesRegex(ValueError, "duplicate id 'a'"):
            load(row + row)

    def test_empty_samples(self):
        with self.assertRaisesRegex(ValueError, "no samples"):
            load('{"id":"a","expected":"1","samples":[]}\n')

    def test_uneven_sample_counts(self):
        text = (
            '{"id":"a","expected":"1","samples":["1","1"]}\n'
            '{"id":"b","expected":"1","samples":["1"]}\n'
        )
        with self.assertRaisesRegex(ValueError, r"differing sample counts \[1, 2\]"):
            load(text)

    def test_empty_file(self):
        with self.assertRaisesRegex(ValueError, "no cases"):
            load("")

    def test_shipped_fixture_loads(self):
        cases = load_cases(Path(__file__).parent.parent / "data" / "samples.jsonl")
        self.assertEqual(len(cases), 12)
        self.assertEqual({len(c.samples) for c in cases}, {5})


if __name__ == "__main__":
    unittest.main()
