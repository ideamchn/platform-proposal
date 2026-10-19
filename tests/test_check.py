import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from check import check, is_template  # noqa: E402

TODAY = date(2027, 1, 15)
NOW = "# Now\n\n**As of:** 2027-01-10 · **Review by:** 2027-01-31 · **Owner:** me\n\n## Header\n- lead named\n"
FILLED = "# File\n\nReal content with no placeholders.\n"


class Check(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        for d in ("context", "inputs", "outputs"):
            (self.root / d).mkdir()
        for rel in ("context/company.md", "context/research-goals.md", "inputs/brief.md", "inputs/gap-register.md"):
            (self.root / rel).write_text(FILLED)
        (self.root / "context/now.md").write_text(NOW)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_ready_first_phase(self):
        errors, notes, info = check(self.root, "phase-1", TODAY)
        self.assertEqual(errors, [])
        self.assertIsNone(info["previous"])
        self.assertEqual(info["output"], "outputs/proposal-phase-1-2027-01-15.md")
        self.assertTrue(any("competitive" in n for n in notes))

    def test_templates_shipped_in_repo_are_detected(self):
        for tpl in (ROOT / "context").glob("*.template.md"):
            self.assertTrue(is_template(tpl.read_text()), tpl.name)
        for tpl in (ROOT / "inputs").glob("*.template.md"):
            if tpl.name != "competitive.template.md":
                self.assertTrue(is_template(tpl.read_text()), tpl.name)

    def test_missing_unfilled_and_stale(self):
        (self.root / "inputs/brief.md").unlink()
        (self.root / "context/company.md").write_text((ROOT / "context/company.template.md").read_text())
        (self.root / "context/now.md").write_text(NOW.replace("2027-01-31", "2027-01-01"))
        errors, _, _ = check(self.root, "phase-1", TODAY)
        joined = "\n".join(errors)
        self.assertIn("inputs/brief.md is missing", joined)
        self.assertIn("still looks like the template", joined)
        self.assertIn("due for review", joined)

    def test_later_phase_finds_previous_and_never_overwrites(self):
        (self.root / "outputs/proposal-phase-1-2027-01-01.md").write_text("p1")
        (self.root / "outputs/proposal-phase-1-2027-01-02.md").write_text("p1 later")
        (self.root / "outputs/proposal-phase-2-2027-01-15.md").write_text("earlier run today")
        _, _, info = check(self.root, "phase-2", TODAY)
        self.assertEqual(info["previous"], "outputs/proposal-phase-1-2027-01-02.md")
        self.assertEqual(info["output"], "outputs/proposal-phase-2-2027-01-15-2.md")

    def test_bad_phase_name(self):
        errors, _, _ = check(self.root, "p1", TODAY)
        self.assertIn("phase must look like", errors[0])


if __name__ == "__main__":
    unittest.main()
