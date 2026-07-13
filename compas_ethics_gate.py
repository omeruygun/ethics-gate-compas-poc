"""
compas_ethics_gate.py
Ethics Gate — Gate 3–5 proof-of-concept (tek tekrarlanabilir hat)

Veri: Gerçek ProPublica COMPAS (compas-scores-two-years.csv) + standart filtreler.
Provenans: DATA_PROVENANCE.md

Sabitler:
  RANDOM_SEED = 42
  TEST_SIZE   = 0.30
  THRESHOLD   = 0.10   # deneysel operasyonel eşik
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fairlearn.metrics import (
    MetricFrame,
    demographic_parity_difference,
    equalized_odds_difference,
    false_positive_rate,
    selection_rate,
    true_positive_rate,
)
from scipy.stats import mannwhitneyu, pointbiserialr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ── Sabitler ──────────────────────────────────────────────────────────────────
RANDOM_SEED = 42
TEST_SIZE = 0.30
THRESHOLD = 0.10
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "compas-scores-two-years.csv"
OUT_DIR = ROOT / "run_artifacts"
FEATURES = [
    "age",
    "sex_enc",
    "juv_fel_count",
    "juv_misd_count",
    "priors_count",
    "charge_enc",
]
RACE_ORDER = ["African-American", "Caucasian", "Hispanic", "Other"]


def file_md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def load_and_filter(path: Path) -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(path)
    n_raw = len(raw)
    df = raw.copy()
    df = df[
        (df["days_b_screening_arrest"] <= 30)
        & (df["days_b_screening_arrest"] >= -30)
    ]
    n_after_days = len(df)
    df = df[df["is_recid"] != -1]
    n_after_recid = len(df)
    df = df[df["c_charge_degree"] != "O"]
    n_after_charge = len(df)
    df = df[df["score_text"].notna()]
    n_clean = len(df)

    race = df["race"].replace(
        {"Asian": "Other", "Native American": "Other"}
    )
    df = df.copy()
    df["race_group"] = race

    meta = {
        "source_file": path.name,
        "source_md5": file_md5(path),
        "n_raw": int(n_raw),
        "n_after_days_filter": int(n_after_days),
        "n_after_is_recid": int(n_after_recid),
        "n_after_charge_degree": int(n_after_charge),
        "n_clean": int(n_clean),
        "filters": [
            "-30 <= days_b_screening_arrest <= 30",
            "is_recid != -1",
            "c_charge_degree != 'O'",
            "score_text notna",
            "race: Asian/Native American -> Other",
        ],
        "provenance": "Real ProPublica COMPAS (Angwin et al., 2016); not synthetic",
    }
    return df, meta


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    le_sex = LabelEncoder()
    le_charge = LabelEncoder()
    out["sex_enc"] = le_sex.fit_transform(out["sex"])
    out["charge_enc"] = le_charge.fit_transform(out["c_charge_degree"])
    return out


def group_confusion(y_true, y_pred, sensitive) -> dict:
    y_true = pd.Series(y_true).reset_index(drop=True)
    y_pred = pd.Series(y_pred).reset_index(drop=True)
    sensitive = pd.Series(sensitive).reset_index(drop=True)
    group_metrics = {}
    for g in RACE_ORDER:
        mask = sensitive == g
        if mask.sum() == 0:
            continue
        yt = y_true[mask]
        yp = y_pred[mask]
        tn, fp, fn, tp = confusion_matrix(yt, yp, labels=[0, 1]).ravel()
        fpr = fp / (fp + tn) if (fp + tn) else 0.0
        tpr = tp / (tp + fn) if (tp + fn) else 0.0
        sel = float((yp == 1).mean())
        group_metrics[g] = {
            "TP": int(tp),
            "FP": int(fp),
            "TN": int(tn),
            "FN": int(fn),
            "FPR": round(float(fpr), 4),
            "TPR": round(float(tpr), 4),
            "selection_rate": round(sel, 4),
            "n": int(mask.sum()),
        }
    return group_metrics


def validate_fairness(group_metrics: dict, dpd: float, eod: float) -> dict:
    """Manuel hücre kontrolü ile Fairlearn değerlerinin uyumunu doğrula."""
    sels = [m["selection_rate"] for m in group_metrics.values()]
    fprs = [m["FPR"] for m in group_metrics.values()]
    tprs = [m["TPR"] for m in group_metrics.values()]
    manual_dpd = max(sels) - min(sels)
    manual_eod = max(max(tprs) - min(tprs), max(fprs) - min(fprs))
    return {
        "manual_dpd": round(manual_dpd, 4),
        "manual_eod": round(manual_eod, 4),
        "fairlearn_dpd": round(float(dpd), 4),
        "fairlearn_eod": round(float(eod), 4),
        "dpd_match": abs(manual_dpd - abs(float(dpd))) < 1e-3,
        "eod_match": abs(manual_eod - abs(float(eod))) < 1e-3,
        "n_test_sum_groups": int(sum(m["n"] for m in group_metrics.values())),
    }


def plot_group_rates(group_metrics: dict, out_path: Path) -> None:
    groups = [g for g in RACE_ORDER if g in group_metrics]
    fpr = [group_metrics[g]["FPR"] for g in groups]
    tpr = [group_metrics[g]["TPR"] for g in groups]
    x = np.arange(len(groups))
    w = 0.35
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x - w / 2, fpr, w, label="FPR")
    ax.bar(x + w / 2, tpr, w, label="TPR")
    ax.set_xticks(x)
    ax.set_xticklabels(groups, rotation=15, ha="right")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Oran")
    ax.set_title(
        "Şekil — Grup Bazlı FPR ve TPR "
        "(Gerçek COMPAS, ırk özellik dışı)"
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_proxy(df_test: pd.DataFrame, out_path: Path) -> None:
    aa = df_test[df_test["race_group"] == "African-American"]
    cau = df_test[df_test["race_group"] == "Caucasian"]
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    axes[0].boxplot(
        [aa["age"], cau["age"]],
        tick_labels=["African-American", "Caucasian"],
    )
    axes[0].set_title("Yaş dağılımı (test)")
    axes[1].boxplot(
        [aa["priors_count"], cau["priors_count"]],
        tick_labels=["African-American", "Caucasian"],
    )
    axes[1].set_title("Önceki suç sayısı (test)")
    fig.suptitle(
        "Şekil — Vekil aday değişken dağılımı (Gerçek COMPAS verisi)"
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def try_shap(model, X_train, X_test, out_path: Path) -> dict | None:
    try:
        import shap
    except ImportError:
        return None
    explainer = shap.LinearExplainer(model, X_train, feature_perturbation="interventional")
    sv = explainer.shap_values(X_test)
    if isinstance(sv, list):
        sv = sv[1]
    mean_abs = np.abs(sv).mean(axis=0)
    importance = {
        f: round(float(v), 4) for f, v in zip(FEATURES, mean_abs)
    }
    order = np.argsort(mean_abs)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(range(len(FEATURES)), mean_abs[order])
    ax.set_yticks(range(len(FEATURES)))
    ax.set_yticklabels([FEATURES[i] for i in order])
    ax.set_xlabel("Ortalama |SHAP|")
    ax.set_title("Şekil — SHAP özellik önemleri (Gerçek COMPAS)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return importance


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    df, meta = load_and_filter(DATA_PATH)
    df = encode_features(df)

    X = df[FEATURES]
    y = df["two_year_recid"].astype(int)
    sensitive = df["race_group"]

    X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(
        X,
        y,
        sensitive,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    model = LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    dpd = demographic_parity_difference(
        y_test, y_pred, sensitive_features=s_test
    )
    eod = equalized_odds_difference(
        y_test, y_pred, sensitive_features=s_test
    )

    mf = MetricFrame(
        metrics={
            "selection_rate": selection_rate,
            "false_positive_rate": false_positive_rate,
            "true_positive_rate": true_positive_rate,
        },
        y_true=y_test,
        y_pred=y_pred,
        sensitive_features=s_test,
    )

    group_metrics = group_confusion(y_test, y_pred, s_test)
    validation = validate_fairness(group_metrics, dpd, eod)
    assert validation["n_test_sum_groups"] == len(X_test), (
        f"Grup n toplamı ({validation['n_test_sum_groups']}) "
        f"test n ({len(X_test)}) ile uyuşmuyor"
    )
    assert validation["dpd_match"], f"DPD uyuşmazlığı: {validation}"
    assert validation["eod_match"], f"EOD uyuşmazlığı: {validation}"

    # Proxy göstergeleri (nedensellik iddiası yok)
    df_test = X_test.copy()
    df_test["race_group"] = s_test.values
    df_test["two_year_recid"] = y_test.values
    df_test["age"] = X_test["age"].values
    df_test["priors_count"] = X_test["priors_count"].values
    aa = df_test["race_group"] == "African-American"
    cau = df_test["race_group"] == "Caucasian"
    r_age, p_age = pointbiserialr(aa.astype(int), df_test["age"])
    r_pri, p_pri = pointbiserialr(aa.astype(int), df_test["priors_count"])
    u_age, pu_age = mannwhitneyu(
        df_test.loc[aa, "age"], df_test.loc[cau, "age"], alternative="two-sided"
    )
    u_pri, pu_pri = mannwhitneyu(
        df_test.loc[aa, "priors_count"],
        df_test.loc[cau, "priors_count"],
        alternative="two-sided",
    )

    fig_fpr_tpr = OUT_DIR / "figure_fpr_tpr.png"
    fig_proxy = OUT_DIR / "figure_proxy_distributions.png"
    fig_shap = OUT_DIR / "figure_shap_importance.png"
    plot_group_rates(group_metrics, fig_fpr_tpr)
    plot_proxy(df_test, fig_proxy)
    shap_importance = try_shap(model, X_train, X_test, fig_shap)

    blocked = bool(abs(dpd) > THRESHOLD or abs(eod) > THRESHOLD)

    aa_m = group_metrics.get("African-American", {})
    cau_m = group_metrics.get("Caucasian", {})

    # Makale tabloları için düz metin özet
    table8_lines = [
        "Tablo 8. Demografik gruba göre grup bazlı sınıflandırma matrisi "
        f"(test seti, n={len(X_test)}; Gerçek COMPAS)",
        "Grup | TP | FP | TN | FN | n | FPR | TPR | selection_rate",
    ]
    for g in RACE_ORDER:
        m = group_metrics[g]
        table8_lines.append(
            f"{g} | {m['TP']} | {m['FP']} | {m['TN']} | {m['FN']} | "
            f"{m['n']} | {m['FPR']:.4f} | {m['TPR']:.4f} | {m['selection_rate']:.4f}"
        )

    table9_lines = [
        "Tablo 9. COMPAS Prototip — Grup Bazlı Adalet Metrikleri ve Gate 5 Kararı "
        "(Gerçek COMPAS, aynı run)",
        f"AA selection_rate={aa_m.get('selection_rate')}",
        f"CAU selection_rate={cau_m.get('selection_rate')}",
        f"selection_rate farkı (AA-CAU)="
        f"{abs(aa_m.get('selection_rate', 0) - cau_m.get('selection_rate', 0)):.4f}",
        f"DPD (Fairlearn, tüm gruplar)={float(dpd):.4f}",
        f"EOD (Fairlearn, tüm gruplar)={float(eod):.4f}",
        f"Gate 5 eşiği={THRESHOLD} (deneysel operasyonel)",
        f"Karar={'BLOCKED' if blocked else 'APPROVED'}",
    ]

    out = {
        "run_id": run_id,
        "model": "LogisticRegression",
        "dataset": meta,
        "random_seed": RANDOM_SEED,
        "test_size": TEST_SIZE,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "features": FEATURES,
        "sensitive_feature": "race_group (excluded from model features)",
        "performance": {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
        },
        "fairness_metrics": {
            "demographic_parity_difference": round(float(dpd), 4),
            "equalized_odds_difference": round(float(eod), 4),
        },
        "metricframe_by_group": json.loads(mf.by_group.round(4).to_json()),
        "group_metrics": group_metrics,
        "validation": validation,
        "proxy_indicators": {
            "note": "Olası proxy göstergesi; nedensel sızma kanıtı değildir.",
            "age_pointbiserial_r": round(float(r_age), 4),
            "age_p": float(p_age),
            "priors_pointbiserial_r": round(float(r_pri), 4),
            "priors_p": float(p_pri),
            "age_mannwhitney_p": float(pu_age),
            "priors_mannwhitney_p": float(pu_pri),
            "age_mean_AA": round(float(df_test.loc[aa, "age"].mean()), 2),
            "age_mean_CAU": round(float(df_test.loc[cau, "age"].mean()), 2),
            "priors_mean_AA": round(float(df_test.loc[aa, "priors_count"].mean()), 2),
            "priors_mean_CAU": round(float(df_test.loc[cau, "priors_count"].mean()), 2),
        },
        "shap_mean_abs": shap_importance,
        "threshold": THRESHOLD,
        "threshold_note": "Deneysel operasyonel eşik; evrensel standart değildir.",
        "gate_decision": "BLOCKED" if blocked else "APPROVED",
        "reason": (
            f"DPD={dpd:.4f} ve/veya EOD={eod:.4f} eşiği ({THRESHOLD}) aşıyor."
            if blocked
            else "Tüm eşikler karşılandı."
        ),
        "artifacts": {
            "figure_fpr_tpr": str(fig_fpr_tpr.name),
            "figure_proxy": str(fig_proxy.name),
            "figure_shap": str(fig_shap.name) if shap_importance else None,
            "table8_txt": "table8.txt",
            "table9_txt": "table9.txt",
        },
    }

    json_path = OUT_DIR / "fairness_results.json"
    json_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT_DIR / "table8.txt").write_text("\n".join(table8_lines), encoding="utf-8")
    (OUT_DIR / "table9.txt").write_text("\n".join(table9_lines), encoding="utf-8")
    # Kökte de kopya (CI bekliyorsa)
    (ROOT / "fairness_results.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("=== GATE 3: PERFORMANS ===")
    print(f"  n_raw={meta['n_raw']}  n_clean={meta['n_clean']}")
    print(f"  n_train={len(X_train)}  n_test={len(X_test)}")
    print(f"  acc={acc:.4f}  prec={prec:.4f}  rec={rec:.4f}  f1={f1:.4f}")
    print("\n=== GATE 4: ADALET ===")
    print(mf.by_group.round(4).to_string())
    print(f"  DPD={dpd:.4f}  EOD={eod:.4f}")
    print(f"  validation={validation}")
    print("\n=== GATE 5 ===")
    print(f"  decision={out['gate_decision']}  threshold={THRESHOLD}")
    print(f"\nArtifacts -> {OUT_DIR}  run_id={run_id}")

    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
