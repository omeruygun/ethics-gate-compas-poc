# Değişiklik Yanıt Tablosu (v6)

Kaynak geri bildirim: `ömer_son_surum_degerlendirme_ve_revizyon_raporu.pdf`  
Revize belge: `Sorumlu Yapay Zeka - Ömer UYGUN v6.docx`  
Deney çıktıları: `ethics_gate_prototype/run_artifacts/`

| # | Danışman bulgusu | Yapılan düzeltme | Kanıt |
|---|---|---|---|
| P0 | Veri gerçek/sentetik çelişkisi | Tek kaynak: gerçek ProPublica COMPAS; sentetik üretim kaldırıldı | `DATA_PROVENANCE.md`, Bölüm 6 metni |
| P0 | n / matrix / JSON tutarsız | Aynı run: n_clean=6172, n_test=1852; Tablo 8–9 ve JSON senkron | `fairness_results.json`, Tablo 8–9 |
| P0 | DPD/EOD uyuşmazlığı | Fairlearn + manuel doğrulama eşleşiyor (DPD≈0.286, EOD≈0.294) | `validation` alanı JSON |
| P0 | Tekrarlanabilir script yok | `compas_ethics_gate.py` tüm çıktıları üretiyor | `ethics_gate_prototype/` |
| P1 | Gate kapsamı aşırı | Öz/Abstract/Sonuç: yalnızca Gate 3–5 PoC | v6 Öz, Abstract, §8 |
| P1 | AI Act 61/72/73 | Gate 6: 72=pazar sonrası izleme, 73=ciddi olay; 61 çıkarıldı | Tablo 7 |
| P1 | Madde 13 ifadesi | Şeffaflık / deployer’a bilgi sağlama olarak daraltıldı | Tablo 7 Gate1/4 |
| P1 | NIST RMF checklist dili | Yinelemeli risk yönetimi işlevleri olarak yazıldı | §5 Tablo 7 öncesi |
| P1 | 0.10 evrensel eşik | Deneysel operasyonel eşik; evrensel standart değil | §6 Gate 5 paragrafı |
| P1 | PRISMA erişilemeyen | Akış: 45 aranan; 2 erişilemeyen; 43 değerlendirilen; 22 dışlama | §3.3 + Şekil 1 başlığı |
| P1 | 2019 öncesi örneklem | Angwin 2016 vaka/arka plan olarak işaretlendi; sistematik n=20 | Tablo 5 |
| P1 | Kaynak türü sayıları | n=20 için 11 dergi / 4 konferans / 3 teknik / 1 resmi / 1 preprint | §4.1 metni |
| P2 | Chouldechova ampirik doğrulama | “Ampirik doğrulama değil; literatürle uyumlu” | §7 |
| P2 | Proxy nedensellik / FPR→DPD | Olası proxy göstergesi; FPR≠DPD doğrulaması | §6 |
| P2 | Başlık-özet-sonuç | EN: PRISMA-ScR-informed mapping; TR yapılandırılmış haritalama; PoC sınırı | Öz, Abstract, Sonuç |
| P1 | CI/CD gerçek log | Repo + failing Actions run (Gate 5 BLOCKED) | https://github.com/omeruygun/ethics-gate-compas-poc/actions/runs/29284962713 ; `ethics_gate_prototype/ci_evidence/` |
| P1 | Arama kanıt dosyaları | `prisma_evidence/` + canlı Piri CSV/RIS (~88 kayıt, VPN); n=138 Haziran oturumu endeks farkı not edildi | `12_piri_live_export_fullscan.*` |
| P3 | Dil/biçim | Aptos (gövde) / Aptos Display (başlık) docDefaults+stiller sabitlendi | v6 styles / apa7-v5-format skill |
| P3 | Son dil/tutarlılık geçişi | Ondalık virgül (0,286/0,294/0,10); YAML canlı workflow’a yaklaştırıldı; Gate 6/proxy dil sadeleştirildi | v6 §6–§7, Tablo 8–9 |
| P3 | Gate 3/4 hizası + EOD terimi | PoC’te adalet→Gate 3, XAI→Gate 4; “fırsatlar”→equalized odds | §5.3–5.4, §6 |
| P3 | Tablo 3 / Piri dalgalanma / PDF | Birleşik dağıtım notu; 138/142/~132–134; PDF 142 kanıtı | §3.1 not; `15_piri_*` |
| P3 | OA facet / eşik duyarlılığı / COMPAS etik / Şekil 1 | 84–54 yumuşatıldı; 0,05/0,10/0,15; etik sınır; diyagram yenilendi | §3, §6, Şekil 1 |
