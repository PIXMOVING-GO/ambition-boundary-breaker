"""Build the bilingual static site: python3 site/build.py OUTPUT_DIRECTORY."""
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

for lang in ("zh-CN", "en"):
    zh = lang == "zh-CN"
    title = "雄心边界突破器" if zh else "Ambition Boundary Breaker"
    lead = ("与 Agent 一起选择值得追求的未来，找出一个今天就能开始、结果足以改变你判断的实验。"
            if zh else "Choose a future worth pursuing with your agent. Design a first experiment whose outcome could change your next decision.")
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
<header><span>PIX Moving / Skills</span><nav><a href="./" lang="zh-CN">中文</a><a href="en.html" lang="en">English</a></nav></header>
<main><h1>{title}</h1><p class="lead">{lead}</p>
<a class="action" href="{package}" download>{'下载 Skill' if zh else 'Download skill'} · v{version}</a><a href="{repo}">GitHub ↗</a>
<section class="panel"><h2>{'从一个问题开始' if zh else 'Try a question'}</h2><p>{prompt}</p></section>
<section><h2>{'在 Codex 中使用' if zh else 'Use in Codex'}</h2><p>{install} <code>~/.codex/skills/</code>。 {start}</p><code>$ambition-boundary-breaker</code>
<p><a href="SKILL.md">{'阅读 Skill 原文' if zh else 'Read the skill'}</a> · <a href="SHA256SUMS">SHA-256</a> · <a href="LICENSE">MIT</a></p></section></main>
<footer><strong>Angelo Yu</strong> · {credit}<p>{collaborator}<br>{role}</p></footer></html>"""
    (out / ("index.html" if zh else "en.html")).write_text(html.replace("</code>。 ", "</code>. ") if not zh else html)
