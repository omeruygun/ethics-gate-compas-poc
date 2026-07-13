# PRISMA-ScR Arama / Eleme Kanıt Paketi

Danışman istenen teslim öğesi: arama tarihi, sorgular, dışa aktarım, yinelenenler, dahil/dışla kararları, kodlama.

Kaynak makale: `Sorumlu Yapay Zeka - Ömer UYGUN v6.docx`  
Oluşturma: makaledeki Tablo 2–5 ve §3 metninden **yeniden üretilebilir paket**.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `01_search_protocol.md` | Tarih, platform, ana dize, kriterler |
| `02_search_queries.csv` | Veritabanı bazlı dizgeler |
| `03_database_hit_counts.csv` | Piri hit sayıları |
| `04_prisma_flow.csv` | Akış sayıları (153→…→21) |
| `05_included_studies_coding.csv` | 21 kayıtkodlama (+ örneklem rolü) |
| `06_included_studies.bib` | BibTeX iskeleti |
| `07_fulltext_exclusion_categories.csv` | Tam metin dışlama kategorileri |
| `08_duplicates_log.md` | n=13; bireysel liste eksik uyarısı |
| `09_screening_summary.csv` | Eleme özeti |
| `10_coding_scheme.md` | Kodlama kuralları |
| `11_excluded_fulltext_titles_TEMPLATE.csv` | Dışlanan başlıklar için şablon |

## Bilinçli boşluklar (öğrenci tamamlamalı)

1. **Piri ekran görüntüsü / ham RIS-CSV** — orijinal Haziran 2026 dışa aktarımı depoda yoksa buraya eklenmeli.  
2. **13 yinelenenin künye listesi** — `08_duplicates_log.md`.  
3. **22+2 dışlanan çalışmanın başlıkları** — `11_…TEMPLATE.csv`.

Sayısal akış ve dahil kodlama makale ile tutarlıdır; yukarıdaki üç madde olmadan “tam arşiv” iddiası kurulmamalıdır.


## Canlı Piri dışa aktarım (VPN, 14 Temmuz 2026)

| Dosya | Açıklama |
|---|---|
| `12_piri_live_session.md` | Oturum kaydı |
| `12_piri_live_export_fullscan.csv` / `.ris` | Canlı arama sonuçları (~88 kayıt) |
| `12_piri_live_export_2019_2026.*` | Yıl parametreli scrape |

**Önemli:** Makaledeki Haziran 2026 oturumu n=138 idi; Piri endeksi değiştiği için canlı tekrar n≈88 verdi. Bu dosyalar aramanın **yapılabilirliğini ve künye arşivini** kanıtlar; orijinal 138’lik RIS yoksa yöntem notunda endeks farkı belirtilmelidir.

- `14_piri_live_url_*` — öğrenci Piri URL doğrulaması (canlı `ec`≈132–134; HTML gzip arşivi)
- `15_piri_search_export_142.pdf` — Piri PDF dışa aktarımı (**142 sonuç**; 38 sayfa)
