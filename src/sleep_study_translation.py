from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
SOURCE_ENV = "SLEEP_STUDY_SOURCE"


def load_sleep_study() -> pd.DataFrame:
    source = os.environ.get(SOURCE_ENV)
    if not source:
        raise SystemExit(f"Set the environment variable {SOURCE_ENV} to the source text file path.")

    df = pd.read_csv(source, sep=r"\s+", engine="python")
    if "id" in df.columns:
        df = df.set_index("id", drop=True)
    return df


def prepare_sleep_study(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    clean = df.copy()
    clean.loc[clean["AverageSleep"] > 24, "AverageSleep"] = np.nan

    missing = (
        clean.isna()
        .mean()
        .mul(100)
        .rename("missing_pct")
        .rename_axis("variable")
        .reset_index()
        .query("missing_pct > 0")
        .sort_values("missing_pct", ascending=False)
    )

    numeric_cols = clean.select_dtypes(include=[np.number]).columns
    for column in numeric_cols:
        clean[column] = clean[column].fillna(clean[column].median())

    for column in clean.columns.difference(numeric_cols):
        clean[column] = clean[column].fillna(clean[column].mode().iloc[0])

    return clean, missing


def build_missingness_figure(original: pd.DataFrame, clean: pd.DataFrame, missing: pd.DataFrame) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.9), facecolor="white")

    if missing.empty:
        axes[0].text(0.5, 0.5, "No missing values detected", ha="center", va="center", fontsize=12)
        axes[0].axis("off")
    else:
        axes[0].barh(missing["variable"], missing["missing_pct"], color="#5f8f66")
        axes[0].invert_yaxis()
        axes[0].set_xlabel("Missing values (%)")
        axes[0].set_title("Variables with missing data", fontsize=13, weight="bold")
        axes[0].grid(axis="x", linestyle="--", alpha=0.25)
        axes[0].set_axisbelow(True)

    before = original["AverageSleep"].dropna()
    after = clean["AverageSleep"].dropna()
    bins = np.linspace(min(before.min(), after.min()), max(before.max(), after.max()), 22)
    axes[1].hist(before, bins=bins, alpha=0.58, color="#245a86", label="Before cleaning")
    axes[1].hist(after, bins=bins, alpha=0.42, color="#c8744a", label="After median imputation")
    axes[1].set_title("AverageSleep before and after imputation", fontsize=13, weight="bold")
    axes[1].set_xlabel("AverageSleep")
    axes[1].set_ylabel("Count")
    axes[1].legend(frameon=False)
    axes[1].grid(axis="y", linestyle="--", alpha=0.25)
    axes[1].set_axisbelow(True)

    fig.suptitle("Sleep-study cleaning and imputation workflow", fontsize=16, fontweight="bold", y=0.98)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.84, bottom=0.16, wspace=0.28)

    out_path = FIGURES / "sleep_missingness_profile.png"
    fig.savefig(out_path, dpi=260)
    plt.close(fig)
    return out_path


def build_statistics_figure(clean: pd.DataFrame) -> tuple[Path, dict[str, float]]:
    corr_df = clean[["AverageSleep", "GPA"]].dropna()
    pearson_r, pearson_p = stats.pearsonr(corr_df["AverageSleep"], corr_df["GPA"])
    slope, intercept, *_ = stats.linregress(corr_df["AverageSleep"], corr_df["GPA"])

    chrono_groups = [
        clean.loc[clean["LarkOwl"] == label, "PoorSleepQuality"].dropna().to_numpy()
        for label in ["Lark", "Neither", "Owl"]
    ]
    kruskal_stat, kruskal_p = stats.kruskal(*chrono_groups)

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.9), facecolor="white")

    axes[0].scatter(corr_df["AverageSleep"], corr_df["GPA"], s=28, alpha=0.55, color="#245a86", edgecolors="none")
    xs = np.linspace(corr_df["AverageSleep"].min(), corr_df["AverageSleep"].max(), 100)
    axes[0].plot(xs, intercept + slope * xs, color="#c8744a", linewidth=2.2)
    axes[0].set_title("Average sleep vs academic performance", fontsize=13, weight="bold")
    axes[0].set_xlabel("AverageSleep")
    axes[0].set_ylabel("GPA")
    axes[0].grid(linestyle="--", alpha=0.25)
    axes[0].text(
        0.03,
        0.95,
        f"Pearson r = {pearson_r:.3f}\np-value = {pearson_p:.3f}",
        transform=axes[0].transAxes,
        ha="left",
        va="top",
        fontsize=10.2,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#D4DEE8"},
    )

    axes[1].boxplot(
        chrono_groups,
        tick_labels=["Lark", "Neither", "Owl"],
        patch_artist=True,
        boxprops={"facecolor": "#dfeaf3", "edgecolor": "#245a86"},
        medianprops={"color": "#0f5a8c", "linewidth": 2},
    )
    axes[1].set_title("Poor sleep quality by chronotype", fontsize=13, weight="bold")
    axes[1].set_xlabel("Chronotype")
    axes[1].set_ylabel("PoorSleepQuality")
    axes[1].grid(axis="y", linestyle="--", alpha=0.25)
    axes[1].text(
        0.03,
        0.95,
        f"Kruskal p = {kruskal_p:.3f}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=10.2,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#D4DEE8"},
    )

    fig.suptitle("Sleep-study statistical contrasts", fontsize=16, fontweight="bold", y=0.98)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.83, bottom=0.16, wspace=0.28)

    out_path = FIGURES / "sleep_statistical_summary.png"
    fig.savefig(out_path, dpi=260)
    plt.close(fig)
    return out_path, {"pearson_p": pearson_p, "kruskal_p": kruskal_p}


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    original = load_sleep_study()
    clean, missing = prepare_sleep_study(original)
    fig1 = build_missingness_figure(original, clean, missing)
    fig2, stats_summary = build_statistics_figure(clean)
    print(fig1)
    print(fig2)
    print(stats_summary)


if __name__ == "__main__":
    main()
