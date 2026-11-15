"""Render the broad evaluation from its paired records."""
import json
from html import escape
from pathlib import Path

groups = {
    "business": ("商业", "Business"), "science": ("科学", "Science"),
    "engineering": ("工程", "Engineering"), "life": ("人生", "Life"),
    "learning": ("学习", "Learning"), "health": ("健康", "Health"),
}

def report(zh, out):
    rows = json.loads((out/"benchmark/broad/results.json").read_text())
    lang = "zh" if zh else "en"
    names = ["直接提问", "加载 Skill"] if zh else ["Direct", "With skill"]
    def counts(group):
        return [[sum(r[cond]["scores"][i] for r in group) for i in range(3)] for cond in ("direct","skill")]
    def changes(group):
        diffs = [r["skill"]["scores"][0]-r["direct"]["scores"][0] for r in group]
        return [diffs.count(i) for i in (1,0,-1)]
    totals = counts(rows)
    up, same, down = changes(rows)
    title = "60 个细分主题的配对测试" if zh else "Paired test across 60 topics"
    intro = (f"在六大类、60 道自拟中文题中，直接提问有 {totals[0][0]} 道提出了新的受益结果、能力或研究问题，加载 v1.1 后有 {totals[1][0]} 道。逐题看，{up} 道仅 Skill 组达到此项，{same} 道同分，{down} 道仅直接回答达到。" if zh else
             f"In 60 constructed Chinese scenarios across six families, {totals[0][0]} direct answers proposed a new outcome, capability or research question, compared with {totals[1][0]} with v1.1. The skill alone met the criterion in {up} pairs, both sides tied in {same}, and the direct answer alone met it in {down}.")
    limits = ("每个细分主题一道题，每种条件生成一次。两组以相同顺序每批回答五道题，可能受同批上下文影响。生成与匿名判分均请求 gpt-6-astra。指标贴近 Skill 的设计，评分有主观性。两组都要求约 100–160 字，本轮无法评估自然对话长度。健康类只考察服务与习惯规划。结果衡量文字回答，实际成效以及预训练或对齐的因果作用仍需另测。" if zh else
              "One constructed case per topic and one answer per condition. Sessions contained five matched prompts, so batch context may influence answers. Generation and label-masked grading requested the same model, gpt-6-astra. The rubric reflects the skill’s aims and requires judgment. Both arms requested about 100–160 Chinese characters; spontaneous answer length was untested. Health cases cover services and habits. Project outcomes and causes related to training were unmeasured.")
    case_url = f"cases-{lang}.html"
    table = []
    sections = []
    for key, labels in groups.items():
        label = labels[0 if zh else 1]
        group = [r for r in rows if r["group"] == key]
        metrics = counts(group)
        table.append('<tr><th>'+label+'</th>'+''.join(f'<td>{a} / {b}</td>' for a,b in zip(*metrics))+'</tr>')
        items = []
        for row in group:
            sides = []
            for cond,name in zip(["direct","skill"],names):
                val=row[cond]
                scores=" / ".join(map(str,val["scores"]))
                sides.append(f'<h3>{name} · {scores}</h3><p>{escape(val["answer"])}</p><p><small>{escape(val["reason"])}</small></p>')
            g_direct=row["direct"]["scores"][0]
            g_skill=row["skill"]["scores"][0]
            transition=f"{g_direct} → {g_skill}"
            items.append(f'<details><summary>{row["id"]} · {escape(row["field"])} · {transition}</summary><p><strong>{escape(row["question"])}</strong></p>{"".join(sides)}</details>')
        sections.append(f'<section id="{key}"><h2>{label}</h2>{"".join(items)}</section>')
    index = ''.join(f'<a href="#{key}">{names_[0 if zh else 1]}</a> ' for key,names_ in groups.items())
    assets = '<a href="benchmark/broad/results.json">JSON</a> · <a href="benchmark/broad/cases.tsv">TSV</a> · <a href="https://github.com/PIXMOVING-GO/ambition-boundary-breaker/blob/main/benchmark/broad/protocol.md">'+('评分规则' if zh else 'Protocol')+'</a>'
    metrics_labels = ["新目标","历史限制","反馈决策"] if zh else ["New goal","Historical constraint","Feedback"]
    (out/case_url).write_text(f'<!doctype html><html lang="{lang}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="style.css"><main><a href="{("./" if zh else "en.html")}#baseline">← {title}</a><h1>{("逐题核对" if zh else "Inspect every pair")}</h1><p>{intro}</p><nav>{index}</nav><p>{" / ".join(metrics_labels)} · {assets}</p>{"".join(sections)}</main></html>')
    head=''.join(f'<th>{l}</th>' for l in metrics_labels)
    total_row = '<tr><th>'+('合计（60 题）' if zh else 'All 60 cases')+'</th>'+''.join(f'<td>{a} / {b}</td>' for a,b in zip(*totals))+'</tr>'
    caption="每格为直接提问 / 加载 Skill 的达标题数，各组 10 题" if zh else "Direct / with-skill counts, ten cases per family"
    return f'<section id="baseline"><h2>{title}</h2><p>{intro}</p><img class="plot" src="benchmark/broad/domain-{lang}.svg" alt="{intro}"><table><caption>{caption}</caption><thead><tr><th>{("领域" if zh else "Family")}</th>{head}</tr></thead><tbody>{"".join(table)}</tbody><tfoot>{total_row}</tfoot></table><p>{limits}</p><p><a href="{case_url}">{("查看全部 120 份答复与评分依据" if zh else "Inspect all 120 answers and scores (Chinese)")}</a> · {assets}</p></section>'
