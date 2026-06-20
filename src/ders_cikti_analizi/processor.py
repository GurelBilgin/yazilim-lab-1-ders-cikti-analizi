"""Excel tabanlı ders çıktısı başarı analizi işlemleri."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

import pandas as pd

ASSESSMENT_COLUMNS = ["Öd1", "Öd2", "Quiz", "Vize", "Fin"]
TABLE2_COLUMNS = ["Ders Çıktı", *ASSESSMENT_COLUMNS]
STUDENT_ID_COLUMN = "Öğrenci_No"
STUDENT_ORDER_COLUMN = "_ogrenci_sira"


def normalize_percentages(percentages: Mapping[str, float]) -> dict[str, float]:
    """Yüzdelik değerleri 0-1 aralığına dönüştürür ve doğrular.

    Fonksiyon hem `10` gibi yüzde formatını hem de `0.10` gibi oran
    formatını kabul eder. Tüm değerlendirme yüzdelerinin toplamı 1 olmalıdır.
    """

    missing = [column for column in ASSESSMENT_COLUMNS if column not in percentages]
    if missing:
        raise ValueError(f"Eksik yüzde bilgisi: {', '.join(missing)}")

    normalized: dict[str, float] = {}
    for column in ASSESSMENT_COLUMNS:
        value = float(percentages[column])
        if value < 0:
            raise ValueError(f"{column} yüzdesi negatif olamaz.")
        normalized[column] = value / 100 if value > 1 else value

    total = sum(normalized.values())
    if abs(total - 1.0) > 0.001:
        raise ValueError(
            "Değerlendirme yüzdelerinin toplamı 100 olmalıdır. "
            f"Mevcut toplam: {total * 100:.2f}"
        )

    return normalized


def read_table2(path: str | Path) -> pd.DataFrame:
    """Tablo 2 dosyasını okur ve beklenen kolon yapısına getirir."""

    df = pd.read_excel(path)

    if all(column in df.columns for column in TABLE2_COLUMNS):
        df = df[TABLE2_COLUMNS].copy()
    elif len(df.columns) >= len(TABLE2_COLUMNS):
        df = df.iloc[:, : len(TABLE2_COLUMNS)].copy()
        df.columns = TABLE2_COLUMNS
    else:
        raise ValueError(
            "Tablo 2 dosyasında beklenen kolonlar bulunamadı. "
            f"Beklenen kolonlar: {TABLE2_COLUMNS}"
        )

    df["Ders Çıktı"] = df["Ders Çıktı"].astype(str)
    for column in ASSESSMENT_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def read_grade_table(path: str | Path) -> pd.DataFrame:
    """Öğrenci not tablosunu okur ve temel kolonları doğrular."""

    df = pd.read_excel(path)
    expected = [STUDENT_ID_COLUMN, *ASSESSMENT_COLUMNS]
    missing = [column for column in expected if column not in df.columns]
    if missing:
        raise ValueError(f"Not tablosunda eksik kolon var: {', '.join(missing)}")

    df = df.copy()
    for column in ASSESSMENT_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def generate_tablo3(table2: pd.DataFrame, percentages: Mapping[str, float]) -> pd.DataFrame:
    """Tablo 2 katsayılarını değerlendirme yüzdeleriyle çarparak Tablo 3 üretir."""

    percentages = normalize_percentages(percentages)
    source = table2.copy()

    if not all(column in source.columns for column in TABLE2_COLUMNS):
        source = source.iloc[:, : len(TABLE2_COLUMNS)].copy()
        source.columns = TABLE2_COLUMNS

    result = pd.DataFrame()
    result["Ders Çıktı"] = source["Ders Çıktı"].astype(str)

    for column in ASSESSMENT_COLUMNS:
        result[column] = pd.to_numeric(source[column], errors="coerce").fillna(0) * percentages[column]

    result["Toplam"] = result[ASSESSMENT_COLUMNS].sum(axis=1)
    return result


def calculate_student_scores(tablo3: pd.DataFrame, grades: pd.DataFrame) -> pd.DataFrame:
    """Her öğrenci için ders çıktısı bazında toplam ve başarı yüzdesi hesaplar.

    Hesaplama, ödevde istenen özgün çıktı düzeniyle uyumludur:
    her öğrencinin notu Tablo 3 katsayısı ile çarpılır, toplam değer
    hesaplanır, maksimum değer ise ilgili ders çıktısının toplam katsayısının
    100 ile çarpılmasıyla bulunur. ``%Başarı`` değeri bir ondalık basamağa
    yuvarlanır.
    """

    rows: list[dict[str, object]] = []

    for student_order, (_, student) in enumerate(grades.iterrows()):
        student_id = student[STUDENT_ID_COLUMN]

        for _, outcome in tablo3.iterrows():
            detail_values = {
                column: float(student[column]) * float(outcome[column])
                for column in ASSESSMENT_COLUMNS
            }
            total = sum(detail_values.values())
            max_value = float(outcome[ASSESSMENT_COLUMNS].sum()) * 100
            success_rate = (total / max_value * 100) if max_value else 0

            rows.append(
                {
                    STUDENT_ORDER_COLUMN: student_order,
                    STUDENT_ID_COLUMN: student_id,
                    "Ders Çıktı": outcome["Ders Çıktı"],
                    **detail_values,
                    "Toplam": total,
                    "Max": max_value,
                    "%Başarı": round(success_rate, 1),
                }
            )

    return pd.DataFrame(rows)


def build_tablo4_rows(scores: pd.DataFrame) -> list[list[object]]:
    """Tablo 4 dosyasını ödevdeki bloklu öğrenci formatına dönüştürür.

    Çıktı dosyasında her öğrenci için önce ``Öğrenci : ...`` satırı,
    ardından başlık satırı ve ders çıktısı başarı satırları yer alır.
    Öğrenciler arasında bir boş satır bırakılır.
    """

    output_columns = ["Ders Çıktı", *ASSESSMENT_COLUMNS, "Toplam", "Max", "%Başarı"]
    rows: list[list[object]] = []

    group_column = STUDENT_ORDER_COLUMN if STUDENT_ORDER_COLUMN in scores.columns else STUDENT_ID_COLUMN

    for _, group in scores.groupby(group_column, sort=False):
        student_id = group.iloc[0][STUDENT_ID_COLUMN]
        rows.append([f"Öğrenci : {student_id}", "", "", "", "", "", "", "", ""])
        rows.append(output_columns)

        for _, score in group.iterrows():
            rows.append([score[column] for column in output_columns])

        rows.append(["", "", "", "", "", "", "", "", ""])

    if rows:
        rows.pop()  # Son öğrenciden sonra fazladan boş satır bırakma.

    return rows


def summarize_scores(scores: pd.DataFrame) -> pd.DataFrame:
    """Ders çıktısı bazında ortalama başarı özeti üretir."""

    return (
        scores.groupby("Ders Çıktı", as_index=False)
        .agg(
            Ortalama_Basari=("%Başarı", "mean"),
            En_Dusuk_Basari=("%Başarı", "min"),
            En_Yuksek_Basari=("%Başarı", "max"),
            Ogrenci_Sayisi=(STUDENT_ID_COLUMN, "count"),
        )
        .round(2)
    )


def _format_excel_sheet(writer: pd.ExcelWriter, sheet_name: str, df: pd.DataFrame) -> None:
    """Excel çıktısı için temel sütun genişliklerini ve tablo stilini uygular."""

    worksheet = writer.sheets[sheet_name]
    workbook = writer.book
    header_format = workbook.add_format(
        {"bold": True, "bg_color": "#1F4E78", "font_color": "white", "border": 1}
    )

    for col_num, column_name in enumerate(df.columns):
        worksheet.write(0, col_num, column_name, header_format)
        width = max(12, min(55, max(len(str(column_name)), int(df[column_name].astype(str).str.len().max() if not df.empty else 0)) + 2))
        worksheet.set_column(col_num, col_num, width)

    worksheet.freeze_panes(1, 0)
    if not df.empty:
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)


def write_outputs(tablo3: pd.DataFrame, scores: pd.DataFrame, output_dir: str | Path) -> dict[str, Path]:
    """Tablo 3 ve Tablo 4 çıktılarını ödevdeki Excel düzeniyle yazar.

    ``Tablo3_Output.xlsx`` tek sayfada ağırlıklı ders çıktısı tablosunu içerir.
    ``Tablo4_Output.xlsx`` ise tek sayfada her öğrenciyi ayrı blok halinde
    gösterir. Bu yapı, özgün ödev çıktısındaki formatla uyumludur.
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    tablo3_file = output_path / "Tablo3_Output.xlsx"
    tablo4_file = output_path / "Tablo4_Output.xlsx"

    # Pandas varsayılan Excel çıktısı Sheet1 adıyla ve sade başlık biçimiyle
    # ödevdeki Tablo 3 formatını üretir.
    tablo3.to_excel(tablo3_file, index=False)

    # Tablo 4, her öğrenci için bloklu yapıdadır. Bu nedenle DataFrame olarak
    # doğrudan yazmak yerine satırlar tek tek aktarılır.
    rows = build_tablo4_rows(scores)
    with pd.ExcelWriter(tablo4_file, engine="xlsxwriter") as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet()
        for row_index, row in enumerate(rows):
            worksheet.write_row(row_index, 0, row)

    return {"tablo3": tablo3_file, "tablo4": tablo4_file}


def run_analysis(
    tablo2_path: str | Path,
    not_tablosu_path: str | Path,
    percentages: Mapping[str, float],
    output_dir: str | Path = "outputs",
) -> dict[str, Path]:
    """Tüm analiz akışını çalıştırır ve üretilen dosya yollarını döndürür."""

    table2 = read_table2(tablo2_path)
    grades = read_grade_table(not_tablosu_path)
    tablo3 = generate_tablo3(table2, percentages)
    scores = calculate_student_scores(tablo3, grades)
    return write_outputs(tablo3, scores, output_dir)
