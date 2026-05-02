from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
SOURCE_ENV = "TOYOTA_SOURCE"


def load_toyota() -> pd.DataFrame:
    source = os.environ.get(SOURCE_ENV)
    if not source:
        raise SystemExit(f"Set the environment variable {SOURCE_ENV} to the Toyota CSV path.")

    df = pd.read_csv(source)
    if "Id" in df.columns:
        df = df.set_index("Id", drop=True)
    return df


def prepare_toyota(df: pd.DataFrame) -> pd.DataFrame:
    clean = df.drop(columns=["Model", "Mfg_Month", "Mfg_Year"], errors="ignore").copy()
    if "CC" in clean.columns:
        clean.loc[clean["CC"] == clean["CC"].max(), "CC"] = np.nan
    if "Guarantee_Period" in clean.columns:
        clean.loc[clean["Guarantee_Period"] > 5, "Guarantee_Period"] = np.nan
    return clean


def build_toyota_figure(clean: pd.DataFrame) -> tuple[Path, dict[str, float]]:
    price = clean["Price"].dropna()
    price_log = np.log(price)
    price_boxcox, _ = stats.boxcox(price)

    airco_yes = clean.loc[clean["Airco"] == 1, "Price"].dropna()
    airco_no = clean.loc[clean["Airco"] == 0, "Price"].dropna()
    t_stat, t_p = stats.ttest_ind(airco_yes, airco_no, equal_var=False, alternative="greater")

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.9), facecolor="white")

    standardized = {
        "Original price": stats.zscore(price.to_numpy(), nan_policy="omit"),
        "Log price": stats.zscore(price_log.to_numpy(), nan_policy="omit"),
        "Box-Cox price": stats.zscore(np.asarray(price_boxcox), nan_policy="omit"),
    }
    colors = {"Original price": "#245a86", "Log price": "#c8744a", "Box-Cox price": "#5f8f66"}
    grid = np.linspace(-3.4, 3.4, 300)
    for label, values in standardized.items():
        density = stats.gaussian_kde(values)
        axes[0].plot(grid, density(grid), linewidth=2.2, color=colors[label], label=label)
    axes[0].set_title("Distribution checks and transformations", fontsize=13, weight="bold")
    axes[0].set_xlabel("Standardized scale")
    axes[0].set_ylabel("Density")
    axes[0].legend(frameon=False, fontsize=9)
    axes[0].grid(axis="y", linestyle="--", alpha=0.25)
    axes[0].set_axisbelow(True)

    axes[1].boxplot(
        [airco_no, airco_yes],
        tick_labels=["No Airco", "Airco"],
        patch_artist=True,
        boxprops={"facecolor": "#dfeaf3", "edgecolor": "#245a86"},
        medianprops={"color": "#0f5a8c", "linewidth": 2},
    )
    axes[1].set_title("Price comparison by air-conditioning status", fontsize=13, weight="bold")
    axes[1].set_ylabel("Price")
    axes[1].grid(axis="y", linestyle="--", alpha=0.25)
    axes[1].text(
        0.03,
        0.95,
        f"Welch t-test p = {t_p:.3e}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=10.2,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#D4DEE8"},
    )

    fig.suptitle("Toyota data-analysis foundations", fontsize=16, fontweight="bold", y=0.98)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.83, bottom=0.16, wspace=0.28)

    out_path = FIGURES / "toyota_transformations_and_tests.png"
    fig.savefig(out_path, dpi=260)
    plt.close(fig)
    return out_path, {"airco_ttest_p": t_p, "price_mean_airco": airco_yes.mean(), "price_mean_no_airco": airco_no.mean()}


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    clean = prepare_toyota(load_toyota())
    fig_path, summary = build_toyota_figure(clean)
    print(fig_path)
    print(summary)


if __name__ == "__main__":
    main()
