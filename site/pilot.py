"""Render the paired evaluation, including each answer and its scoring rationale."""
import json
from html import escape
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "benchmark"

def section(zh):
    protocol = json.loads((DATA / "protocol.json").read_text())
    results = json.loads((DATA / "results.json").read_text())
    labels = ["新目标", "历史限制", "反馈决策"] if zh else ["New goal", "Historical constraint", "Feedback"]
    scenarios = ["县档案馆", "材料研究", "城市公交", "学校用水"] if zh else ["Archives", "Materials", "Bus service", "School water"]
    conditions = ["直接提问", "加载 Skill"] if zh else ["Direct", "With skill"]
    table = []
    details = []
    for (key, prompt), title in zip(protocol["questions"], scenarios):
        rows = results["pairs"][key]
        cells = []
        for condition, label in zip(["direct", "skill"], conditions):
            row = rows[condition]
            cells.append(" / ".join(str(n) for n in row["scores"]))
            details.append(f'<details><summary>{title} · {label}</summary><p>{escape(prompt)}</p><pre>{escape(row["answer"])}</pre><p>{escape(row["rationale"])}</p></details>')
        table.append(f'<tr><th scope="row">{title}</th><td>{cells[0]}</td><td>{cells[1]}</td></tr>')
    lang = "zh" if zh else "en"
    summary = results["summary"][lang]
    note = ("四道自拟中文题。每题每种条件各生成一次，Codex CLI 请求 gpt-6-astra，推理强度中等。项目方用一个 AI 评审按预先固定的规则判分，评审先看打乱编号的回答，再揭晓条件。每格按上列顺序列出三项分值，1 表示达到标准。"
            if zh else "Four constructed Chinese prompts, one generation per prompt and condition. Codex CLI requested gpt-6-astra with medium reasoning. One project-side AI reviewer scored shuffled answers against the prespecified criteria before revealing conditions. The three values in each cell follow the order below; 1 means the criterion was met.")
    limits = ("样本只覆盖一种模型和四个情境。题目主动邀请模型给建议，指标也贴近 Skill 的设计。实际项目成效、不同模型的普遍倾向，以及预训练或对齐的因果作用均待检验。"
              if zh else "One model, four scenarios. The questions invite advice and the rubric reflects the skill’s design. Real project outcomes, generalization across models and the causal roles of pretraining and alignment remain open.")
    return f'''<section id="baseline"><h2>{'模型会主动改写目标吗？' if zh else 'Does the model propose a different goal?'}</h2>
<p>{summary}</p><img class="plot" src="benchmark/chart-{lang}.svg" alt="{escape(summary)}"><p>{note}</p>
<table><caption>{" · ".join(labels)}</caption><thead><tr><th>{'情境' if zh else 'Scenario'}</th><th>{conditions[0]}</th><th>{conditions[1]}</th></tr></thead><tbody>{"".join(table)}</tbody></table>
<p>{limits}</p><p><a href="benchmark/protocol.json">{'题目与判分规则' if zh else 'Prompts and rubric'}</a> · <a href="benchmark/results.json">{'原始回答与逐项评分（JSON）' if zh else 'Answers and scores (JSON)'}</a></p>
<h3>{'逐题核对' if zh else 'Inspect each response (Chinese)'}</h3>{"".join(details)}</section>'''
