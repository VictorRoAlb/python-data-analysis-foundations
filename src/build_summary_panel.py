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

    fig = plt.figure(figsize=(14.2, 8.1), facecolor="white")
    grid = fig.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1], hspace=0.10, wspace=0.08)

    ax1 = fig.add_subplot(grid[0, 0])
    ax2 = fig.add_subplot(grid[0, 1])
    ax3 = fig.add_subplot(grid[1, 0])
    ax4 = fig.add_subplot(grid[1, 1])

    for axis, (title, path) in zip((ax1, ax2, ax3), image_paths.items()):
        axis.imshow(plt.imread(path))
        axis.set_title(title, fontsize=13.5, fontweight="bold", pad=8)
        axis.axis("off")

    ax4.axis("off")
    ax4.text(0.0, 0.96, "Coursework overview", fontsize=17, fontweight="bold", va="top", color="#102033")
    ax4.text(
        0.0,
        0.82,
        "Python version of the core coursework workflow, centered on cleaning, transformation, exploratory analysis and statistical contrasts.",
        fontsize=12.2,
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
    y = 0.64
    for bullet in bullets:
        ax4.text(0.02, y, f"- {bullet}", fontsize=11.7, color="#213243", va="top")
        y -= 0.11

    ax4.text(
        0.0,
        0.17,
        "The repository combines the sleep-study exercises with the Toyota examples used in the course so the analytical workflow can be followed from start to finish in Python.",
        fontsize=11.1,
        color="#52647b",
        va="top",
        wrap=True,
    )

    fig.suptitle("Python data analysis foundations", fontsize=20, fontweight="bold", y=0.985)
    out_path = FIGURES / "python_data_analysis_summary.png"
    fig.savefig(out_path, dpi=260, bbox_inches="tight")
    plt.close(fig)
    print(out_path)


if __name__ == "__main__":
    main()
