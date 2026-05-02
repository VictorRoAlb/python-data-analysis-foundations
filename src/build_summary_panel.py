from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


def main() -> None:
    image_paths = {
        "Sleep cleaning": FIGURES / "sleep_missingness_profile.png",
        "Sleep contrasts": FIGURES / "sleep_statistical_summary.png",
        "Toyota examples": FIGURES / "toyota_transformations_and_tests.png",
    }

    missing = [name for name, path in image_paths.items() if not path.exists()]
    if missing:
        raise SystemExit(f"Generate the component figures first. Missing: {', '.join(missing)}")

    fig = plt.figure(figsize=(14.0, 10.2), facecolor="white")
    grid = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], width_ratios=[1, 1], hspace=0.18, wspace=0.12)

    ax1 = fig.add_subplot(grid[0, 0])
    ax2 = fig.add_subplot(grid[0, 1])
    ax3 = fig.add_subplot(grid[1, 0])
    ax4 = fig.add_subplot(grid[1, 1])

    for axis, (title, path) in zip((ax1, ax2, ax3), image_paths.items()):
        axis.imshow(plt.imread(path))
        axis.set_title(title, fontsize=12.5, fontweight="bold", pad=10)
        axis.axis("off")

    ax4.axis("off")
    ax4.text(0.0, 0.95, "Portfolio summary", fontsize=16, fontweight="bold", va="top", color="#102033")
    ax4.text(
        0.0,
        0.78,
        "This public Python version keeps the structure of the original coursework while translating it into a cleaner portfolio format.",
        fontsize=11.5,
        color="#52647b",
        va="top",
        wrap=True,
    )
    bullets = [
        "Data cleaning and missing-value profiling.",
        "Simple imputation and variable transformation.",
        "Exploratory figures that support interpretation.",
        "Statistical contrasts for correlation and group comparisons.",
    ]
    y = 0.60
    for bullet in bullets:
        ax4.text(0.02, y, f"- {bullet}", fontsize=11.2, color="#213243", va="top")
        y -= 0.12

    ax4.text(
        0.0,
        0.12,
        "The original coursework was produced in R. The public repository reworks the main ideas into Python so the portfolio stays technically consistent.",
        fontsize=10.8,
        color="#52647b",
        va="top",
        wrap=True,
    )

    fig.suptitle("Python data analysis foundations", fontsize=20, fontweight="bold", y=0.98)
    out_path = FIGURES / "python_data_analysis_summary.png"
    fig.savefig(out_path, dpi=260)
    plt.close(fig)
    print(out_path)


if __name__ == "__main__":
    main()
