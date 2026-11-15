"""Run or resume the frozen evaluation. Usage: python3 run.py PRIVATE_RUN_DIRECTORY"""
import csv
import json
import random
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

here = Path(__file__).resolve().parent
cache = Path(sys.argv[1]).resolve()
cache.mkdir(parents=True, exist_ok=True)
cases = list(csv.DictReader((here / "cases.tsv").open(), delimiter="\t"))
skill = (here.parents[1] / "SKILL.md").read_text()
protocol = (here / "protocol.md").read_text()
shared = protocol.split("Shared instruction: ")[1].split("\n")[0]
rubric = protocol.split("Primary outcome: ")[1].split("\n")[0]
random.Random(617).shuffle(cases)
flip_rng = random.Random(831)
order = {c["id"]: flip_rng.choice([["direct", "skill"], ["skill", "direct"]]) for c in cases}
batches = [cases[i:i+5] for i in range(0, len(cases), 5)]

def request(key, prompt, validate):
    saved = cache / (key + ".json")
    if saved.exists():
        value = json.loads(saved.read_text())
        validate(value)
        return value
    for attempt in range(3):
        prefix = cache / f"{key}-{attempt}"
        output = prefix.with_suffix(".txt")
        with tempfile.TemporaryDirectory() as tmp, prefix.with_suffix(".log").open("w") as log, prefix.with_suffix(".jsonl").open("w") as events:
            try:
                result = subprocess.run(["codex","exec","--ignore-user-config","--ephemeral","--skip-git-repo-check","-C",tmp,"-s","read-only","-m","gpt-6-astra","-c",'model_reasoning_effort="medium"',"--json","-o",str(output),"-"],input=prompt,text=True,stdout=events,stderr=log,timeout=290)
                if result.returncode:
                    raise ValueError("incomplete generation")
                log_items = [json.loads(l) for l in prefix.with_suffix(".jsonl").read_text().splitlines()]
                assert log_items[-1]["type"] == "turn.completed"
                assert all(e["item"]["type"] in {"error","agent_message","reasoning"} for e in log_items if e["type"]=="item.completed")
                reply = output.read_text().strip()
                if reply.startswith("```"):
                    reply = "\n".join(reply.splitlines()[1:-1])
                value = json.loads(reply)
                validate(value)
            except (ValueError, AssertionError, KeyError, TypeError, subprocess.TimeoutExpired) as err:
                print(key, attempt+1, type(err).__name__, flush=True)
                continue
        saved.write_text(json.dumps(value, ensure_ascii=False))
        print(key, "ok", flush=True)
        return value
    raise RuntimeError(key)

def run_batch(task):
    n, condition = task
    rows = batches[n]
    questions = {c["id"]:c["question"] for c in rows}
    def validate(value):
        assert set(value) == set(questions)
        for answer in value.values():
            if condition == "judge":
                assert set(answer) == {"A","B"}
                for item in answer.values():
                    assert len(item["scores"]) == 3 and all(type(x) is int and x in (0,1) for x in item["scores"])
                    assert isinstance(item["reason"], str) and item["reason"].strip()
            else:
                assert isinstance(answer, str) and len(answer.strip()) >= 30
    if condition == "judge":
        inputs = {}
        for qid,q in questions.items():
            inputs[qid] = {"question":q}
            for side, cond in zip("AB",order[qid]):
                inputs[qid][side]=json.loads((cache/f"{n}-{cond}.json").read_text())[qid]
        prompt = ("Judge independently and strictly using this rubric: "+rubric+"\nReturn only a JSON object keyed by question ID. Each maps to A and B; for each give scores:[G,H,F] as three integers and reason: a short Chinese explanation covering all three criteria grounded in the text. A tie is fine. Do not use tools.\n"+json.dumps(inputs,ensure_ascii=False))
    else:
        prompt = shared + "\n" + (skill if condition=="skill" else "")+"\n"+json.dumps(questions,ensure_ascii=False)
    return request(f"{n}-{condition}",prompt,validate)

def main():
    with ThreadPoolExecutor(6) as pool:
        list(pool.map(run_batch, [(n,c) for n in range(len(batches)) for c in ("direct","skill")]))
        list(pool.map(run_batch, [(n,"judge") for n in range(len(batches))]))
    rows=[]
    for n,batch in enumerate(batches):
        grades=json.loads((cache/f"{n}-judge.json").read_text())
        for c in batch:
            row=dict(c)
            for side,cond in zip("AB",order[c["id"]]):
                row[cond]={"answer":json.loads((cache/f"{n}-{cond}.json").read_text())[c["id"]],**grades[c["id"]][side]}
            rows.append(row)
    (here/"results.json").write_text(json.dumps(sorted(rows,key=lambda r:r["id"]),ensure_ascii=False,indent=2)+"\n")

if __name__ == "__main__":
    main()
