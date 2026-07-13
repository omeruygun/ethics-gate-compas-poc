# Veri Provenansı ve Sözlüğü

## Karar (P0)

| Madde | Değer |
|---|---|
| Tek kaynak | **Gerçek** ProPublica COMPAS `compas-scores-two-years.csv` |
| Sentetik üretim | Kullanılmıyor (`compas_ethics_gate.py` içindeki sentetik üretim kaldırıldı) |
| Yanlış adlandırma | `compas_synthetic.csv`, gerçek dosyanın birebir kopyasıydı (aynı MD5); makalede “sentetik” ifadesi kullanılmamalı |
| Referans | Angwin, J., Larson, J., Mattu, S., & Kirchner, L. (2016). Machine bias. ProPublica. |

## İndirme / dosya

- Yerel yol: `ethics_gate_prototype/compas-scores-two-years.csv`
- Ham satır: **7214** (+ başlık)
- Checksum (MD5): `9165d40c400bba93a8cffece2b74622b`

## ProPublica temizlik filtreleri

Aşağıdaki filtreler ProPublica analizinde yaygın kullanılan eşikleri uygular; filtre sonrası **n = 6172**:

1. `-30 ≤ days_b_screening_arrest ≤ 30`
2. `is_recid != -1`
3. `c_charge_degree != 'O'`
4. `score_text` boş değil

## Irk grupları (analiz)

Model özelliklerinde **ırk yok**. Adalet analizi için hassas öznitelik:

| Grup | Tanım |
|---|---|
| African-American | olduğu gibi |
| Caucasian | olduğu gibi |
| Hispanic | olduğu gibi |
| Other | Other + Asian + Native American |

## Model özellikleri

| Özellik | Kaynak sütun | Not |
|---|---|---|
| age | age | sayısal |
| sex_enc | sex | LabelEncoder (Male/Female) |
| juv_fel_count | juv_fel_count | |
| juv_misd_count | juv_misd_count | |
| priors_count | priors_count | |
| charge_enc | c_charge_degree | F/M |

Hedef: `two_year_recid` (0/1)

## Deney parametreleri (sabit)

| Parametre | Değer |
|---|---|
| RANDOM_SEED | 42 |
| TEST_SIZE | 0.30 |
| Stratify | `y` (`two_year_recid`) |
| Model | `LogisticRegression(max_iter=1000, random_state=42)` |
| Gate 5 eşiği | 0.10 (deneysel operasyonel; evrensel standart değil) |

## Çıktı kuralı

Tüm tablo sayıları, şekiller ve `fairness_results.json` **aynı script çalıştırmasından** (`compas_ethics_gate.py`) üretilir. Makaleye elle sayı taşınmaz.
