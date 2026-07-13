# GitHub Actions — Gate 5 Kanıt Paketi

## Çalıştırma

| Alan | Değer |
|---|---|
| Repo | https://github.com/omeruygun/ethics-gate-compas-poc |
| Workflow | Ethics Gate — Fairness & Deployment Check |
| Run URL | https://github.com/omeruygun/ethics-gate-compas-poc/actions/runs/29284962713 |
| Commit | `247252400b2849b5c29744d1368ef4375154ac3d` |
| Sonuç | **failure** (beklenen — Gate 5 BLOCKED) |
| Tarih (UTC) | 2026-07-13T21:05:02Z |

## Neden “başarısız”?

`compas_ethics_gate.py` DPD=0.2857 ve EOD=0.2945 ile deneysel eşiği (0.10) aştığı için çıkış kodu 1 döndürdü. Bu, makaledeki “önceden tanımlı adalet eşiğini ihlal eden dağıtımı durdurma” iddiasının CI kanıtıdır.

## Yerel kopyalar

- `ci_evidence/actions_full.log` — tam job logu
- `ci_evidence/run_metadata.json` — run meta
- `ci_evidence/artifacts/` — CI’dan indirilen `fairness_results.json` + `run_artifacts/`
