from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from ders_cikti_analizi.processor import (
    calculate_student_scores,
    generate_tablo3,
    normalize_percentages,
    run_analysis,
)


class PercentageTests(unittest.TestCase):
    def test_normalize_percentages_accepts_100_scale(self):
        result = normalize_percentages({"Öd1": 10, "Öd2": 10, "Quiz": 10, "Vize": 30, "Fin": 40})
        self.assertAlmostEqual(result["Öd1"], 0.10)
        self.assertAlmostEqual(sum(result.values()), 1.0)

    def test_normalize_percentages_rejects_invalid_total(self):
        with self.assertRaises(ValueError):
            normalize_percentages({"Öd1": 10, "Öd2": 10, "Quiz": 10, "Vize": 10, "Fin": 10})


class ProcessorTests(unittest.TestCase):
    def setUp(self):
        self.table2 = pd.DataFrame(
            {
                "Ders Çıktı": ["DÇ1", "DÇ2"],
                "Öd1": [1, 0],
                "Öd2": [0, 1],
                "Quiz": [1, 1],
                "Vize": [0, 1],
                "Fin": [1, 0],
            }
        )
        self.percentages = {"Öd1": 20, "Öd2": 10, "Quiz": 20, "Vize": 20, "Fin": 30}

    def test_generate_tablo3_calculates_weighted_coefficients(self):
        tablo3 = generate_tablo3(self.table2, self.percentages)
        self.assertEqual(list(tablo3.columns), ["Ders Çıktı", "Öd1", "Öd2", "Quiz", "Vize", "Fin", "Toplam"])
        self.assertAlmostEqual(tablo3.loc[0, "Öd1"], 0.20)
        self.assertAlmostEqual(tablo3.loc[0, "Quiz"], 0.20)
        self.assertAlmostEqual(tablo3.loc[0, "Fin"], 0.30)
        self.assertAlmostEqual(tablo3.loc[0, "Toplam"], 0.70)

    def test_calculate_student_scores_calculates_success_rate(self):
        tablo3 = generate_tablo3(self.table2, self.percentages)
        grades = pd.DataFrame(
            {
                "Öğrenci_No": ["220500001"],
                "Öd1": [100],
                "Öd2": [50],
                "Quiz": [80],
                "Vize": [70],
                "Fin": [60],
            }
        )
        scores = calculate_student_scores(tablo3, grades)
        first = scores.iloc[0]
        self.assertEqual(len(scores), 2)
        self.assertEqual(first["Öğrenci_No"], "220500001")
        self.assertAlmostEqual(first["Toplam"], 54.0)
        self.assertAlmostEqual(first["Max"], 70.0)
        self.assertAlmostEqual(first["%Başarı"], 77.1)

    def test_run_analysis_creates_excel_outputs(self):
        grades = pd.DataFrame(
            {
                "Öğrenci_No": ["220500001", "220500002"],
                "Öd1": [100, 70],
                "Öd2": [50, 80],
                "Quiz": [80, 90],
                "Vize": [70, 60],
                "Fin": [60, 75],
            }
        )
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            table2_path = tmp_path / "tablo2.xlsx"
            grades_path = tmp_path / "not_tablosu.xlsx"
            output_dir = tmp_path / "outputs"
            self.table2.to_excel(table2_path, index=False)
            grades.to_excel(grades_path, index=False)

            outputs = run_analysis(table2_path, grades_path, self.percentages, output_dir)

            self.assertTrue(outputs["tablo3"].exists())
            self.assertTrue(outputs["tablo4"].exists())
            tablo4 = pd.read_excel(outputs["tablo4"], sheet_name="Ogrenci_Basarilari")
            self.assertEqual(len(tablo4), 4)


if __name__ == "__main__":
    unittest.main()
