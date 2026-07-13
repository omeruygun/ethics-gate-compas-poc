# Ethics Gate Prototype (Gate 3–5 PoC)

ProPublica COMPAS üzerinde tekrarlanabilir adalet / CI/CD eşik kontrolü.

## Hızlı çalıştırma

```bash
pip install -r requirements.txt
python compas_ethics_gate.py
```

Eşik aşılırsa çıkış kodu `1` (Gate 5 BLOCKED).

## CI

GitHub Actions: `.github/workflows/ethics_gate.yml`  
Provenans: `DATA_PROVENANCE.md`

## Veri

`compas-scores-two-years.csv` — gerçek ProPublica COMPAS (sentetik değil).


## Kanıt paketleri (v6)

| Yol | İçerik |
|---|---|
| `run_artifacts/` | Aynı run: Tablo 8–9, şekiller, `fairness_results.json` |
| `ci_evidence/` | GitHub Actions Gate 5 FAIL log + artifact kopyaları |
| `prisma_evidence/` | Piri arama URL/PDF/ekran, PRISMA akış kanıtları |
| `docs_Sorumlu_YZ_v6.docx` | Makale v6 anlık kopyası |
| `degisiklik_yanit_tablosu.md` | Danışman bulgusu → düzeltme tablosu |

Tek çalıştırma: `python compas_ethics_gate.py` (eşitlik eşiği aşılınca exit 1 = beklenen Gate 5).
