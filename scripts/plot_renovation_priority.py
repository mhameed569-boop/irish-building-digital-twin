import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


PROJECT_FOLDER = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "renovation_priority_by_county_2024.csv"
)

OUTPUT_FOLDER = PROJECT_FOLDER / "outputs" / "figures"
PNG_FILE = OUTPUT_FOLDER / "renovation_priority_top10.png"
SVG_FILE = OUTPUT_FOLDER / "renovation_priority_top10.svg"

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "Priority data not found. "
        "Run build_renovation_priority.py first."
    )

with INPUT_FILE.open(
    mode="r",
    encoding="utf-8-sig",
    newline="",
) as file:
    records = list(csv.DictReader(file))

records.sort(
    key=lambda row: int(row["Priority Rank"])
)

top_ten = records[:10]

counties = [row["County"] for row in top_ten]
scores = [
    float(row["Renovation Priority Score"])
    for row in top_ten
]

normalizer = Normalize(
    vmin=min(scores),
    vmax=max(scores),
)

colors = plt.cm.RdYlGn_r(normalizer(scores))

plt.style.use("seaborn-v0_8-whitegrid")

figure, axis = plt.subplots(figsize=(10, 6))

bars = axis.barh(
    counties,
    scores,
    color=colors,
    edgecolor="#444444",
    linewidth=0.5,
)

axis.invert_yaxis()

axis.set_title(
    "Top 10 Renovation Priority Counties in Ireland",
    fontsize=15,
    pad=16,
)

axis.set_xlabel(
    "Renovation Priority Score (0-100)",
    fontsize=11,
)

axis.set_ylabel("")

axis.set_xlim(0, max(scores) * 1.15)

axis.grid(
    axis="x",
    linestyle="--",
    alpha=0.35,
)

axis.grid(
    axis="y",
    visible=False,
)

axis.spines["top"].set_visible(False)
axis.spines["right"].set_visible(False)
axis.spines["left"].set_visible(False)

for bar, score in zip(bars, scores):
    axis.text(
        score + 1,
        bar.get_y() + bar.get_height() / 2,
        f"{score:.2f}",
        va="center",
        fontsize=10,
    )

figure.tight_layout()

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)

figure.savefig(
    PNG_FILE,
    dpi=200,
    bbox_inches="tight",
)

figure.savefig(
    SVG_FILE,
    bbox_inches="tight",
)

plt.close(figure)

print(f"PNG chart created: {PNG_FILE}")
print(f"SVG chart created: {SVG_FILE}")