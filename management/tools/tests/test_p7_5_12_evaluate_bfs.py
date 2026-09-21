"""GPU 없이 강도별 결과 식별과 재개 보호를 확인한다."""
import argparse
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "evaluator", ROOT / "docs/assets/part-07/chapter-05/sec-12/p7_5_12_evaluate_bfs.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class EvaluationTests(unittest.TestCase):
    def test_invalid_scales(self):
        for value in ("nan", "inf", "-0.1", "1.1"):
            with self.assertRaises(argparse.ArgumentTypeError):
                m.parse_scale(value)
        self.assertEqual(m.parse_scale("0.50"), 0.5)

    def test_names_do_not_collide(self):
        c = {"id": "sample"}
        keys = [m.output_key(c, m.parse_scale(x)) for x in ("0", "0.5", "0.75", "1")]
        self.assertEqual(len(set(keys)), 4)
        self.assertEqual(keys[0], "sample-base")
        self.assertEqual(keys[-1], "sample-lora")
        self.assertEqual(m.output_key(c, m.parse_scale("0.50")), keys[1])

    def test_case_selection(self):
        cases = [{"id": "a", "management_code": "001"}, {"id": "b", "management_code": "002"}]
        self.assertEqual(m.select_cases(cases, ["002"]), cases[1:])
        for selection in (["missing"], ["a", "001"]):
            with self.assertRaises(ValueError):
                m.select_cases(cases, selection)

    def test_resume_and_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            case = {"id": "a", "management_code": "001"}
            plan = {"cases": [case], "scales": [0.5], "checkpoint_sha256": "checkpoint", "code_sha256": "code"}
            self.assertEqual(m.completed_outputs(out, plan), [])
            m.write(out / "plan.json", plan)
            key = m.output_key(case, 0.5)
            png = out / (key + ".png")
            png.write_bytes(b"test-output")
            with self.assertRaises(ValueError):
                m.completed_outputs(out, plan)
            record = {"case": case, "scale": 0.5, "checkpoint_sha256": "checkpoint",
                      "plan_sha256": m.sha256(out / "plan.json"), "output_sha256": m.sha256(png)}
            m.write(out / (key + "-result.json"), record)
            self.assertEqual(m.completed_outputs(out, plan), [key])
            for field, value in (("code_sha256", "new"), ("checkpoint_sha256", "new"), ("scales", [0.75])):
                with self.assertRaises(ValueError):
                    m.completed_outputs(out, {**plan, field: value})
            png.write_bytes(b"corrupt")
            with self.assertRaises(ValueError):
                m.completed_outputs(out, plan)


if __name__ == "__main__":
    unittest.main()
