"""Komut satırı arayüzü."""

from __future__ import annotations

import argparse
from pathlib import Path

from .processor import ASSESSMENT_COLUMNS, run_analysis


def _ask_percentage(label: str) -> float:
    while True:
        raw_value = input(f"{label} yüzdesi: ").strip().replace(",", ".")
        try:
            return float(raw_value)
        except ValueError:
            print("Lütfen sayısal bir değer girin. Örnek: 10 veya 10.5")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Excel dosyaları üzerinden ders çıktısı başarı analizi yapar."
    )
    parser.add_argument("--tablo2", default="data/tablo2.xlsx", help="Tablo 2 Excel dosyası yolu")
    parser.add_argument(
        "--not-tablosu", default="data/not_tablosu.xlsx", help="Öğrenci not tablosu Excel dosyası yolu"
    )
    parser.add_argument("--output-dir", default="outputs", help="Çıktı dosyalarının yazılacağı klasör")
    parser.add_argument("--od1", type=float, help="Öd1 yüzdesi")
    parser.add_argument("--od2", type=float, help="Öd2 yüzdesi")
    parser.add_argument("--quiz", type=float, help="Quiz yüzdesi")
    parser.add_argument("--vize", type=float, help="Vize yüzdesi")
    parser.add_argument("--fin", type=float, help="Final yüzdesi")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    raw_percentages = {
        "Öd1": args.od1,
        "Öd2": args.od2,
        "Quiz": args.quiz,
        "Vize": args.vize,
        "Fin": args.fin,
    }

    for column in ASSESSMENT_COLUMNS:
        if raw_percentages[column] is None:
            raw_percentages[column] = _ask_percentage(column)

    outputs = run_analysis(
        tablo2_path=Path(args.tablo2),
        not_tablosu_path=Path(args.not_tablosu),
        percentages=raw_percentages,
        output_dir=Path(args.output_dir),
    )

    print("Analiz tamamlandı.")
    print(f"Tablo 3: {outputs['tablo3']}")
    print(f"Tablo 4: {outputs['tablo4']}")


if __name__ == "__main__":
    main()
