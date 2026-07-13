# Arama Protokolü (PRISMA-ScR kanıt)

## Oturum

| Alan | Değer |
|---|---|
| Platform | Süleyman Demirel Üniversitesi **Piri Keşif Aracı** |
| Tarih | **Haziran 2026** (makale oturum kaydı; saat dilimi: TRT) |
| Saat | Orijinal ekran görüntüsü yoksa `YYYY-MM-DD HH:MM` Piri dışa aktarımından doldurulmalı |
| Tarih aralığı filtresi | 2019–2026 |
| Dil | İngilizce / Türkçe |

## Ana arama dizesi

```
("responsible AI" OR "ethical AI" OR "AI ethics" OR "algorithmic fairness")
AND
("software engineering" OR "SDLC" OR "MLOps" OR "machine learning lifecycle" OR "CI/CD")
```

## Resmi Piri arama linki (yeniden üretilebilir)

Aşağıdaki URL, çalışmada kullanılan boolean sorgunun Piri Keşif Aracı üzerindeki **arama linkidir** (`fields=all`, `pageorder=50`):

https://kesifaraci.com/index.jsp?modul=advantage-search&operator=or&searchword=%28%22responsible+AI%22+OR+%22ethical+AI%22+OR+%22AI+ethics%22+OR+%22algorithmic+fairness%22%29+AND+%28%22software+engineering%22+OR+%22SDLC%22+OR+%22MLOps%22+OR+%22machine+learning+lifecycle%22+OR+%22CI%2FCD%22%29&fields=all&pageorder=50&p=1

SDÜ kurumsal eşdeğer (`uid=sdu.edu.tr`):

https://kesifaraci.com/index.jsp?uid=sdu.edu.tr&modul=advantage-search&operator=or&searchword=%28%22responsible+AI%22+OR+%22ethical+AI%22+OR+%22AI+ethics%22+OR+%22algorithmic+fairness%22%29+AND+%28%22software+engineering%22+OR+%22SDLC%22+OR+%22MLOps%22+OR+%22machine+learning+lifecycle%22+OR+%22CI%2FCD%22%29&fields=all&pageorder=50&p=1

Doğrulama notları: `13_piri_screenshot_note.md` (n=142), `14_piri_live_url_note.md` (canlı yeniden koşum). Hit sayısı Piri endeksine göre oturumdan oturuma hafifçe değişebilir; haritalama tabanı **Haziran 2026, n=138**.

Veritabanına uyarlanmış dizgeler: `02_search_queries.csv`

## Veritabanları

Scopus, Web of Science, IEEE Xplore, ACM Digital Library, SpringerLink, ScienceDirect, arXiv (+ gri literatür n=15).

Hit sayıları: `03_database_hit_counts.csv`

## Dahil etme

1. 2019–2026 yayımlanmış  
2. Responsible AI / ethical AI / algorithmic fairness  
3. Yazılım geliştirme / MLOps / SDLC / CI/CD teknik ilişki  
4. Hakemli makale, konferans, teknik rapor veya resmi belge  

## Dışlama

1. Yalnızca felsefi/soyut, teknik bileşen yok  
2. Doğrulanamayan / erişilemeyen kaynak  
3. Yinelenen kayıt  
4. EN/TR dışı dil  

## Kodlayıcı

Tek kodlayıcı (makalede yöntemsel sınırlılık olarak belirtilmiştir). İkinci kodlayıcı doğrulaması yapılmamıştır.

PDF dışa aktarım kanıtı: `15_piri_search_export_142.pdf` (Piri arayüzü: **142 sonuç bulundu**).
