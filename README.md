# Ambition Boundary Breaker

**English** · [简体中文](README.zh-CN.md)

An agent skill for people choosing what to pursue with AI. It asks the agent to contribute a goal you did not propose, explain what would make that goal possible, and identify the first experiment that could change your decision.

[Project site](https://skills.pixmoving.com/ambition-boundary/en.html) · [Download v1.1](https://skills.pixmoving.com/ambition-boundary/ambition-boundary-breaker-v1.1.zip) · [Read the skill](SKILL.md)

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
