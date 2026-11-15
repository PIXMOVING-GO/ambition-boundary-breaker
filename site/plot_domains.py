"""Draw primary outcome counts from the broad evaluation."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import font_manager
from broad import groups

data = Path(__file__).resolve().parents[1] / "benchmark/broad"
rows = json.loads((data / "results.json").read_text())
for zh in (False, True):
    if zh:
        path = Path("/System/Library/Fonts/STHeiti Medium.ttc")
        if path.exists():
            font_manager.fontManager.addfont(path)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name()
        else:
            plt.rcParams["font.family"] = "Noto Sans CJK SC"
    fig, ax = plt.subplots(figsize=(7.2, 4.1), layout="constrained", facecolor="#f7f6ee")
    ax.set_facecolor("#f7f6ee")
    for cond, shift, color, label in [
        ("direct",-.18,"#697974","直接提问" if zh else "Direct"),
        ("skill",.18,"#12654e","加载 Skill" if zh else "With skill")]:
        values = [sum(r[cond]["scores"][0] for r in rows if r["group"]==g) for g in groups]
        bars = ax.barh([i+shift for i in range(len(groups))], values, .30, color=color, label=label)
        ax.bar_label(bars, padding=4)
    ax.set_yticks(range(len(groups)), [labels[0 if zh else 1] for labels in groups.values()])
    ax.invert_yaxis()
    ax.set_xlim(0,11)
    ax.set_xticks(range(0,11,2))
    ax.set_xlabel("提出新目标的题数（每个领域大类 10 题）" if zh else "Scenarios with a new goal (10 per family)")
    ax.legend(loc="lower right",bbox_to_anchor=(1,1),ncol=2,frameon=False)
    ax.spines[["right","top","left"]].set_visible(False)
    output = data / ("domain-zh.svg" if zh else "domain-en.svg")
    fig.savefig(output)
    output.write_text("\n".join(line.rstrip() for line in output.read_text().splitlines())+"\n")
    plt.close(fig)
