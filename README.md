# Yazılım Lab 1 Proje 2 - Ders Çıktısı Başarı Analizi

Bu proje, **Yazılım Lab 1 dersi Proje 2** kapsamında geliştirilmiş bir ders çıktısı ve öğrenci başarı analizi uygulamasıdır. Projede Excel dosyaları üzerinden ders çıktıları, değerlendirme türleri ve öğrenci notları işlenerek çıktı tabloları oluşturulur.

Uygulama; `tablo2.xlsx` dosyasındaki ders çıktısı ve katsayı bilgilerini, kullanıcıdan alınan değerlendirme yüzdeleriyle birlikte işler. Daha sonra `not_tablosu.xlsx` dosyasındaki öğrenci notlarını kullanarak her öğrenci için ders çıktısı bazında başarı yüzdesi hesaplar.

## Özellikler

* Excel dosyalarından veri okuma
* Ders çıktısı katsayılarını değerlendirme yüzdeleriyle çarpma
* `Tablo3_Output.xlsx` çıktısını oluşturma
* Öğrenci notlarına göre ders çıktısı başarı oranlarını hesaplama
* `Tablo4_Output.xlsx` çıktısını ödev formatına uygun şekilde üretme
* Her öğrenci için ayrı blok yapısında başarı tablosu oluşturma
* Komut satırından parametreli veya etkileşimli çalıştırma
* Modüler ve test edilebilir Python proje yapısı
* Birim testleri ile hesaplama mantığını doğrulama

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

## Kullanılan Teknolojiler

* Python
* pandas
* openpyxl
* xlsxwriter
* unittest

## Kurulum

Python 3.10 veya üzeri önerilir.

Proje klasöründe aşağıdaki komut çalıştırılır:

```bash
python -m pip install -e .
```

Bu komut proje bağımlılıklarını kurar ve komut satırı aracını kullanılabilir hâle getirir.

## Çalıştırma

Program, değerlendirme yüzdeleri parametre olarak verilerek çalıştırılabilir:

```bash
ders-cikti-analizi --od1 10 --od2 10 --quiz 10 --vize 30 --fin 40
```

Alternatif olarak Python modülü üzerinden çalıştırılabilir:

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

Farklı dosya yolları kullanılmak istenirse aşağıdaki gibi parametre verilebilir:

```bash
python -m ders_cikti_analizi.cli --tablo2 data/tablo2.xlsx --not-tablosu data/not_tablosu.xlsx --output-dir outputs --od1 10 --od2 10 --quiz 10 --vize 30 --fin 40
```

## Çıktı Dosyaları

Program çalıştırıldıktan sonra `outputs/` klasöründe şu dosyalar oluşturulur:

```text
outputs/Tablo3_Output.xlsx
outputs/Tablo4_Output.xlsx
```

### Tablo3_Output.xlsx

`Tablo3_Output.xlsx`, ders çıktısı ve değerlendirme türleri arasındaki katsayıların kullanıcı tarafından girilen yüzdelerle çarpılması sonucunda oluşturulur.

Bu dosya tek sayfa olarak hazırlanır ve ödevde istenen çıktı formatına uygun şekilde üretilir.

### Tablo4_Output.xlsx

`Tablo4_Output.xlsx`, her öğrenci için ders çıktısı bazında başarı yüzdesini gösterir.

Çıktı dosyasında her öğrenci ayrı bir blok olarak yer alır:

```text
Öğrenci : öğrenci_no
Ders Çıktı | Öd1 | Öd2 | Quiz | Vize | Fin | Toplam | Max | %Başarı
...ders çıktısı satırları...
```

Her öğrenci bloğu arasında boş satır bırakılır. Bu yapı, ödevde verilen özgün çıktı formatıyla uyumludur.

## Testler

Projedeki testleri çalıştırmak için:

```bash
python -m unittest discover -s tests -v
```

Testler, ders çıktısı hesaplama, yüzde hesaplama ve çıktı formatına yönelik temel işlevlerin doğru çalıştığını kontrol eder.

## Geliştirme Notları

Proje ilk hâlinde tek dosyalı bir yapıdaydı. Güncel sürümde veri okuma, hesaplama ve komut satırı arayüzü ayrı modüllere ayrılmıştır. Böylece proje hem daha okunabilir hâle getirilmiş hem de GitHub üzerinde daha düzenli bir şekilde sunulmuştur.

Çıktı dosyaları doğrudan repoya eklenmez. Program çalıştırıldığında `outputs/` klasörü içinde yeniden oluşturulur.

## Hazırlayanlar

* Gürel BİLGİN
* Gizem YALÇIN
* Yerdinat ALİKHAN
* Berkay ARAS
