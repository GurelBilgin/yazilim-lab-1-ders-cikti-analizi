# Yazılım Lab 1 Proje 2 - Ders Çıktısı Başarı Analizi

Bu proje, Excel dosyaları üzerinden ders çıktısı bazında öğrenci başarı analizi yapmak için geliştirilmiştir. Kullanıcıdan değerlendirme yüzdeleri alınır, Tablo 2'deki ders çıktısı-katsayı ilişkileri bu yüzdelerle çarpılarak Tablo 3 oluşturulur. Ardından öğrenci not tablosu kullanılarak her öğrenci için ders çıktısı başarı yüzdeleri hesaplanır ve Tablo 4 çıktısı üretilir.

## Özellikler

- `tablo2.xlsx` dosyasından ders çıktısı ve değerlendirme katsayılarını okuma
- `not_tablosu.xlsx` dosyasından öğrenci notlarını okuma
- Öd1, Öd2, Quiz, Vize ve Final yüzdelerini kullanıcıdan alma
- Tablo 3 ağırlıklı katsayı tablosunu oluşturma
- Tüm öğrenciler için ders çıktısı bazında başarı hesaplama
- Tablo 4 öğrenci başarı çıktısını Excel olarak üretme
- Komut satırından parametreli veya etkileşimli çalıştırma
- Test edilebilir modüler Python yapısı

## Proje Yapısı

```text
yazilim-lab-1-ders-cikti-analizi/
├── README.md
├── pyproject.toml
├── .gitignore
├── data/
│   ├── not_tablosu.xlsx
│   ├── tablo1.xlsx
│   └── tablo2.xlsx
├── src/
│   └── ders_cikti_analizi/
│       ├── __init__.py
│       ├── cli.py
│       └── processor.py
└── tests/
    └── test_processor.py
```

## Kurulum

Python 3.10 veya üzeri önerilir.

```bash
python -m pip install -e .
```

Bu komut proje bağımlılıklarını kurar ve komut satırı aracını kullanılabilir hâle getirir.

## Kullanılan Kütüphaneler

- `pandas`
- `openpyxl`
- `xlsxwriter`

## Çalıştırma

Komut satırından yüzdeleri parametre olarak vererek çalıştırabilirsiniz:

```bash
ders-cikti-analizi --od1 10 --od2 10 --quiz 10 --vize 30 --fin 40
```

Alternatif olarak Python modülü üzerinden çalıştırabilirsiniz:

```bash
python -m ders_cikti_analizi.cli --od1 10 --od2 10 --quiz 10 --vize 30 --fin 40
```

Yüzde parametreleri verilmezse program değerleri kullanıcıdan ister.

## Giriş Dosyaları

Varsayılan giriş dosyaları `data/` klasöründe bulunur:

```text
data/tablo2.xlsx
data/not_tablosu.xlsx
```

İsterseniz farklı dosya yolları da verebilirsiniz:

```bash
python -m ders_cikti_analizi.cli --tablo2 data/tablo2.xlsx --not-tablosu data/not_tablosu.xlsx --output-dir outputs --od1 10 --od2 10 --quiz 10 --vize 30 --fin 40
```

## Çıktı Dosyaları

Program çalıştıktan sonra `outputs/` klasöründe şu dosyalar oluşturulur:

```text
outputs/Tablo3_Output.xlsx
outputs/Tablo4_Output.xlsx
```

`Tablo3_Output.xlsx` dosyası tek sayfada, ödevdeki örnek çıktı formatına uygun olarak oluşturulur.

`Tablo4_Output.xlsx` dosyası da tek sayfada oluşturulur. Her öğrenci için şu blok düzeni kullanılır:

```text
Öğrenci : öğrenci_no
Ders Çıktı | Öd1 | Öd2 | Quiz | Vize | Fin | Toplam | Max | %Başarı
...ders çıktısı satırları...
```

Öğrenciler arasında bir boş satır bırakılır. Bu yapı, özgün ödev çıktısındaki `Tablo4_Output.xlsx` düzeniyle uyumludur.

## Testler

```bash
python -m unittest discover -s tests -v
```

## Geliştirme Notları

Önceki tek dosyalı yapı yerine veri okuma, hesaplama ve komut satırı arayüzü ayrı modüllere ayrılmıştır. Böylece hesaplama fonksiyonları arayüzden bağımsız olarak test edilebilir ve proje GitHub üzerinde daha düzenli bir yapıyla sunulabilir.

## Hazırlayan

- Gürel Bilgin

Bu proje, Yazılım Lab 1 dersi Proje 2 kapsamında geliştirilmiştir.
