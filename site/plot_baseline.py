"""Regenerate the published descriptive charts using Matplotlib."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import font_manager

data = Path(__file__).resolve().parents[1] / "benchmark"
pairs = json.loads((data / "results.json").read_text())["pairs"]
for zh in (False, True):
    if zh:
        path = Path("/System/Library/Fonts/STHeiti Medium.ttc")
        if path.exists():
            font_manager.fontManager.addfont(path)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name()
        else:
            plt.rcParams["font.family"] = "Noto Sans CJK SC"
    fig, ax = plt.subplots(figsize=(7, 2.9), layout="constrained", facecolor="#f7f6ee")
    ax.set_facecolor("#f7f6ee")
    labels = ["提出新目标", "解释历史限制", "反馈改变决策"] if zh else ["New goal", "Historical constraint", "Feedback guides decision"]
    for condition, offset, color, label in [
        ("direct", -.18, "#6b7975", "直接提问" if zh else "Direct"),
        ("skill", .18, "#12654e", "加载 Skill" if zh else "With skill")]:
        counts = [sum(row[condition]["scores"][i] for row in pairs.values()) for i in range(3)]
        bars = ax.barh([i+offset for i in range(3)], counts, .29, color=color, label=label)
        ax.bar_label(bars, labels=[f"{n}/4" for n in counts], padding=4)
    ax.set_yticks(range(3), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 4.65)
    ax.set_xticks(range(5))
    ax.set_xlabel("达到标准的题数" if zh else "Scenarios meeting criterion")
    ax.spines[["right", "top", "left"]].set_visible(False)
    ax.legend(loc="lower right", bbox_to_anchor=(1,1), ncol=2, frameon=False)
    fig.savefig(data / ("chart-zh.svg" if zh else "chart-en.svg"))
    plt.close(fig)
