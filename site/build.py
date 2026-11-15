"""Build the bilingual static site: python3 site/build.py OUTPUT_DIRECTORY."""
from pilot import section
from broad import report
import hashlib
import re
import shutil
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

site = Path(__file__).resolve().parent
root = site.parent
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
skill = root / "SKILL.md"
version = re.search(r'^  version: "([0-9.]+)"$', skill.read_text(), re.M)[1]
name = "ambition-boundary-breaker"
repo = f"https://github.com/PIXMOVING-GO/{name}"
package = f"{name}-v{version}.zip"
with ZipFile(out / package, "w") as archive:
    for file in ["SKILL.md", "LICENSE"]:
        member = ZipInfo(f"{name}/{file}")
        member.external_attr = 0o100644 << 16
        archive.writestr(member, (root / file).read_bytes(), compress_type=ZIP_DEFLATED)
for file in ["SKILL.md", "LICENSE"]:
    shutil.copyfile(root / file, out / file)
shutil.copyfile(site / "style.css", out / "style.css")
digest = hashlib.sha256((out / package).read_bytes()).hexdigest()
(out / "SHA256SUMS").write_text(f"{digest}  {package}\n")

shutil.copytree(root / "benchmark", out / "benchmark", dirs_exist_ok=True)
for lang in ("zh-CN", "en"):
    zh = lang == "zh-CN"
    title = "雄心边界突破器" if zh else "Ambition Boundary Breaker"
    question = ('你有没有一个很想做，却从没认真写进计划的项目？'
             if zh else 'What would you love to build, but have never put on the roadmap?')
    problem = ('也许当初放下它，是因为团队太小，一次实验要等三个月，等结果回来，已经没有时间再试。今天再问 AI，它可能会沿着这段历史，给你一份同样谨慎的时间表。可如果你现在能在同一个季度里根据上一轮结果连做三轮实验，当初让你放弃的理由，还剩下几个？'
             if zh else 'Maybe your team was too small. One experiment took three months, and by the time the results came back, there was no time to try again. Ask AI for a timeline today and it may give you a careful estimate based on that same history. But suppose you could run three experiments this quarter, each informed by the last. Which of your reasons for shelving the idea would still hold?')
    lead = ('雄心边界突破器邀请 Agent 和你一起重选目标。带上那个被搁置的想法，让它提出一个你还没敢写下的目标，找出哪项条件已经改变，以及这周能做什么来验证这个判断。'
             if zh else "Ambition Boundary Breaker invites your agent to help choose the goal itself. Bring it a shelved idea. Ask it to propose a goal you haven't dared write down, identify what has changed, and suggest something you can do this week to find out whether it matters.")
    hypothesis = ("项目始于一个疑问。模型在已有文本上学习，偏好对齐又鼓励它回应用户的意图。当我们带着过去的工期和一个偏小的目标去问，Agent 会不会把这些前提也接过来，替我们把旧计划写得更周全？已有研究观察到部分模型会附和用户的信念。项目建议里的雄心是否也受影响，需要单独测量。"
                  if zh else "Models learn from existing text, and preference tuning encourages them to follow a user’s intent. If we bring yesterday’s timeline and a modest goal, will an agent quietly accept both and polish the old plan? Research has observed assistants echoing users’ beliefs. Whether that carries over to ambition in project advice is a separate empirical question.")
    prompt = ("我们是两人的维修培训团队，每周有两小时可以请教师傅。除了翻译更多教材，还能让学徒第一次做到什么？"
              if zh else "We are a two-person training team with two hours of expert time each week. What could our apprentices do for the first time if we looked beyond translating more manuals?")
    install = ("解压下载包，将其中的文件夹放入" if zh else "Extract the ZIP and place the enclosed folder in")
    start = ("新开一个对话，输入以下调用名和你的问题。" if zh else "Start a new chat with the invocation below and your question.")
    credit = ('<a href="https://www.pixmoving.com/">PIX Moving</a> 创始人兼 CEO' if zh else 'Founder and CEO of <a href="https://www.pixmoving.com/">PIX Moving</a>')
    collaborator = ("Agent 协作者：灌木丛（Guanmucong）" if zh else "Agent collaborator: Guanmucong (灌木丛)")
    role = ("参与推理、框架综合、Skill 系统协同设计、文档与实现支持；该署名不代表法律人格、所有权、治理授权或责任主体地位。" if zh else "Contributed to reasoning, framework synthesis, collaborative skill system design, documentation and implementation support. This credit confers no legal personhood, ownership, governance authority or status as a responsible party.")
    html = f"""<!doctype html>
<html lang="{lang}"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · PIX Moving</title><link rel="stylesheet" href="style.css">
<header><span>PIX Moving / {title}</span><nav><a href="./" lang="zh-CN">中文</a><a href="en.html" lang="en">English</a></nav></header>
<main>
<figure class="opening"><blockquote lang="en">“We wanted flying cars, instead we got 140 characters.”</blockquote>
<figcaption>{'我们想要会飞的汽车，得到的却是 140 个字符。<br>' if zh else ''}<a href="https://longreads.com/2011/07/26/we-wanted-flying-cars-instead-we-got-140-characters/">Founders Fund, 2011</a></figcaption></figure>
<h1>{question}</h1><p class="lead">{problem}</p><p>{hypothesis} <a href="https://arxiv.org/abs/2203.02155">InstructGPT</a> · <a href="https://arxiv.org/abs/2310.13548">{'迎合行为研究' if zh else 'Sycophancy study'}</a></p><p>{lead}</p><p><a href="#baseline">{'查看基线测试 ↓' if zh else 'See the baseline test ↓'}</a></p>
<a class="action" href="{package}" download>{'下载 Skill' if zh else 'Download skill'} · v{version}</a><a href="{repo}">GitHub ↗</a>
<section class="panel"><h2>{'从一个问题开始' if zh else 'Try a question'}</h2><p>{prompt}</p></section>
{report(zh, out)}
<details><summary>{'早期四题试测' if zh else 'Original four-case pilot'}</summary>{section(zh)}</details>
<section><h2>{'在 Codex 中使用' if zh else 'Use in Codex'}</h2><p>{install} <code>~/.codex/skills/</code>。 {start}</p><code>$ambition-boundary-breaker</code>
<p><a href="SKILL.md">{'阅读 Skill 原文' if zh else 'Read the skill'}</a> · <a href="SHA256SUMS">SHA-256</a> · <a href="LICENSE">MIT</a></p></section></main>
<footer><strong>Angelo Yu</strong> · {credit}<p>{collaborator}<br>{role}</p></footer></html>"""
    (out / ("index.html" if zh else "en.html")).write_text(html.replace("</code>。 ", "</code>. ") if not zh else html)
