import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from sample_eval.report import main

FIXTURE = Path(__file__).parent.parent / "data" / "samples.jsonl"


def run(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class CliTest(unittest.TestCase):
    def test_fixture_report(self):
        code, out, _ = run(str(FIXTURE))
        self.assertEqual(code, 0)
        self.assertIn("cases=12 samples_per_case=5 k=3", out)
        self.assertIn("pass^k    0.400", out)

    def test_k_is_configurable(self):
        _, out, _ = run(str(FIXTURE), "-k", "1")
        self.assertIn("k=1", out)
        self.assertIn("pass@k    0.717", out)

    def test_k_above_sample_count_fails_cleanly(self):
        code, _, err = run(str(FIXTURE), "-k", "9")
        self.assertEqual(code, 2)
        self.assertIn("k=9", err)

    def test_bad_file_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.jsonl"
            bad.write_text("{oops\n")
            code, _, err = run(str(bad))
        self.assertEqual(code, 2)
        self.assertIn("bad case", err)


if __name__ == "__main__":
    unittest.main()
