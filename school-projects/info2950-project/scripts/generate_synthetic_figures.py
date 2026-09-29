"""
Generate portfolio preview figures from fully synthetic sports-style aggregates.

These plots illustrate the INFO 2950 analysis workflow (EDA, OLS, bootstrap
comparisons). They are NOT reproduced from course CSVs and contain no PII.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

RNG = np.random.default_rng(2950)
FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"


def _team_season_win_rates(
    n_teams: int,
    n_seasons: int,
    mean: float,
    spread: float,
    persistence: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Synthetic first/second-half win rates with league-specific means."""
    first: list[float] = []
    second: list[float] = []
    for _ in range(n_seasons):
        base = RNG.normal(mean, spread, size=n_teams)
        base = np.clip(base, 0.15, 0.85)
        noise = RNG.normal(0, 0.06, size=n_teams)
        first.extend(base.tolist())
        second.extend(np.clip(persistence * base + (1 - persistence) * mean + noise, 0.1, 0.9).tolist())
    return np.array(first), np.array(second)


def plot_pooled_regression(out: Path) -> None:
    leagues = [
        ("NBA", 0.52, 0.08, 0.55),
        ("NFL", 0.50, 0.12, 0.35),
        ("MLB", 0.50, 0.06, 0.45),
        ("NHL", 0.50, 0.10, 0.40),
    ]
    xs: list[float] = []
    ys: list[float] = []
    labels: list[str] = []
    for name, mean, spread, persistence in leagues:
        x, y = _team_season_win_rates(30, 8, mean, spread, persistence)
        xs.extend(x.tolist())
        ys.extend(y.tolist())
        labels.extend([name] * len(x))

    fig, ax = plt.subplots(figsize=(7, 5))
    palette = {"NBA": "#1d428a", "NFL": "#013369", "MLB": "#c41e3a", "NHL": "#111111"}
    for name in palette:
        mask = [label == name for label in labels]
        ax.scatter(
            np.array(xs)[mask],
            np.array(ys)[mask],
            alpha=0.35,
            s=18,
            label=name,
            color=palette[name],
        )
    coef = np.polyfit(xs, ys, 1)
    line_x = np.linspace(0.15, 0.85, 100)
    ax.plot(line_x, coef[0] * line_x + coef[1], color="#444444", linewidth=2, label="OLS fit (synthetic)")
    ax.set_xlabel("First-half win rate (synthetic)")
    ax.set_ylabel("Second-half win rate (synthetic)")
    ax.set_title("Multi-league regular season persistence\n(synthetic demo — not course CSV output)")
    ax.legend(loc="lower right", fontsize=8)
    fig.text(0.99, 0.01, "SYNTHETIC DATA", ha="right", va="bottom", fontsize=8, color="#666666")
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)


def plot_league_means(out: Path) -> None:
    leagues = ["NBA", "NFL", "MLB", "NHL"]
    means_first = [0.502, 0.498, 0.501, 0.499]
    means_second = [0.504, 0.497, 0.500, 0.501]
    x = np.arange(len(leagues))
    width = 0.35

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.bar(x - width / 2, means_first, width, label="First half", color="#4c78a8")
    ax.bar(x + width / 2, means_second, width, label="Second half", color="#f58518")
    ax.set_xticks(x, leagues)
    ax.set_ylabel("Mean win rate (synthetic)")
    ax.set_title("League-level season splits (illustrative aggregates)")
    ax.set_ylim(0.45, 0.55)
    ax.legend()
    fig.text(0.99, 0.01, "SYNTHETIC DATA", ha="right", va="bottom", fontsize=8, color="#666666")
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)


def plot_bootstrap_diff(out: Path) -> None:
    nba = RNG.normal(0.52, 0.08, size=120)
    mlb = RNG.normal(0.50, 0.06, size=120)
    observed = nba.mean() - mlb.mean()
    boot = np.empty(2000)
    for i in range(2000):
        boot[i] = RNG.choice(nba, size=len(nba), replace=True).mean() - RNG.choice(
            mlb, size=len(mlb), replace=True
        ).mean()

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    sns.histplot(boot, kde=True, ax=ax, color="#72b7b2", edgecolor="white")
    ax.axvline(observed, color="#e45756", linestyle="--", linewidth=2, label=f"Observed Δ = {observed:.3f}")
    ax.set_xlabel("Bootstrap mean difference (NBA − MLB, synthetic)")
    ax.set_title("Pairwise league comparison via bootstrap resampling")
    ax.legend()
    fig.text(0.99, 0.01, "SYNTHETIC DATA", ha="right", va="bottom", fontsize=8, color="#666666")
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)


def main() -> None:
    sns.set_theme(style="whitegrid", font_scale=0.95)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plot_pooled_regression(FIGURES_DIR / "synthetic_win_rate_regression.png")
    plot_league_means(FIGURES_DIR / "synthetic_league_season_splits.png")
    plot_bootstrap_diff(FIGURES_DIR / "synthetic_bootstrap_league_diff.png")
    print(f"Wrote figures to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
