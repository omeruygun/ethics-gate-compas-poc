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
