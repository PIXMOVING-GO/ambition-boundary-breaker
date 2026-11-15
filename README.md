# Ambition Boundary Breaker

**English** · [简体中文](README.zh-CN.md)

> “We wanted flying cars, instead we got 140 characters.”
>
> — [Founders Fund, 2011](https://longreads.com/2011/07/26/we-wanted-flying-cars-instead-we-got-140-characters/)

**What would you love to build, but have never put on the roadmap?**

Maybe your team was too small. One experiment took three months, and by the time the results came back, there was no time to try again. Ask AI for a timeline today and it may give you a careful estimate based on that same history. But suppose you could run three experiments this quarter, each informed by the last. Which of your reasons for shelving the idea would still hold?

Ambition Boundary Breaker invites your agent to help choose the goal itself. Bring it a shelved idea. Ask it to propose a goal you haven't dared write down, identify what has changed, and suggest something you can do this week to find out whether it matters.

[Project site](https://skills.pixmoving.com/ambition-boundary/en.html) · [Download v1.1](https://skills.pixmoving.com/ambition-boundary/ambition-boundary-breaker-v1.1.zip) · [Read the skill](SKILL.md)

## Baseline pilot

Why might an agent inherit a modest target? Pretraining draws on historical text, and preference tuning encourages responsiveness to the user. We tested whether an assistant would propose a new goal when the brief already suggested one.

We compared direct answers with v1.1 on 60 constructed Chinese prompts, ten topics in each of six families. Direct answers proposed a new goal in 53/60 cases; answers with the skill did so in 59/60. The skill alone met this criterion in 6 pairs, both sides tied in 54, and the direct answer alone met it in 0. Each condition was sampled once and graded by the same model with labels masked. Real project outcomes were not measured.

[Domain charts, 120 answers and judgments](https://skills.pixmoving.com/ambition-boundary/en.html#baseline)

## Try it

> We are a two-person training team translating ten repair manuals. With agents and two hours of expert time each week, what goal should we pursue?

One possible ambition is to help an apprentice reason through an unfamiliar fault. Use one chapter to build a practice scenario. Ask a technician to listen as the apprentice explains a new case. That observation helps decide whether to expand to a family of machines.

## How it works

1. Describe who could do something for the first time. Let the user choose which ambition to pursue.
2. Trace how AI changes the critical path and where the next bottleneck moves.
3. For open-ended discovery, estimate time to usable feedback, uncertainty resolved per round, and opportunities for parallel and sequential experiments. Assess longer agent task horizons and additional compute against that specific workflow.
4. Choose an affordable action with an observable result. Use the result to expand, revise or retire the goal.

## Install

Download and extract the ZIP. For a personal Codex installation, place the enclosed folder at `~/.codex/skills/ambition-boundary-breaker/`. Start a new chat and invoke `$ambition-boundary-breaker` with your question. The skill is written in Chinese and instructs the agent to respond in the user's language.

## License and credits

[MIT License](LICENSE)

**Angelo Yu**

Founder and CEO of [PIX Moving](https://www.pixmoving.com/)

Agent collaborator: **Guanmucong (灌木丛)**

Contributed to reasoning, framework synthesis, collaborative skill system design, documentation and implementation support. This credit confers no legal personhood, ownership, governance authority or status as a responsible party.
