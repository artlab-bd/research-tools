import csv
import tempfile
import unittest
from pathlib import Path

from csv_quality_check import inspect_csv, is_missing


class MissingValueTests(unittest.TestCase):
    def test_common_missing_markers(self):
        for value in (None, "", " ", "NA", "n/a", "null", "None", "."):
            with self.subTest(value=value):
                self.assertTrue(is_missing(value))

    def test_valid_zero_is_not_missing(self):
        self.assertFalse(is_missing("0"))


class InspectCsvTests(unittest.TestCase):
    def test_report_counts_duplicates_missing_and_empty_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.csv"
            with path.open("w", encoding="utf-8", newline="") as output:
                writer = csv.writer(output)
                writer.writerow(["id", "district", "score"])
                writer.writerow(["001", "Dhaka", "5"])
                writer.writerow(["002", "Khulna", "NA"])
                writer.writerow(["002", "Khulna", "NA"])
                writer.writerow(["", "", ""])

            report = inspect_csv(path, encoding="utf-8")

        self.assertEqual(report["rows"], 4)
        self.assertEqual(report["columns"], 3)
        self.assertEqual(report["duplicate_rows"], 1)
        self.assertEqual(report["empty_rows"], 1)
        self.assertEqual(report["missing_values"], {"id": 1, "district": 1, "score": 3})

    def test_header_is_required(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            path.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                inspect_csv(path, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
