# 雄心边界突破器

[English](README.md) · **简体中文**

> “We wanted flying cars, instead we got 140 characters.”
>
> — [Founders Fund, 2011](https://longreads.com/2011/07/26/we-wanted-flying-cars-instead-we-got-140-characters/)

我们想要会飞的汽车，得到的却是 140 个字符。

**你有没有一个很想做，却从没认真写进计划的项目？**

也许当初放下它，是因为团队太小，一次实验要等三个月，等结果回来，已经没有时间再试。今天再问 AI，它可能会沿着这段历史，给你一份同样谨慎的时间表。可如果你现在能在同一个季度里根据上一轮结果连做三轮实验，当初让你放弃的理由，还剩下几个？

雄心边界突破器邀请 Agent 和你一起重选目标。带上那个被搁置的想法，让它提出一个你还没敢写下的目标，找出哪项条件已经改变，以及这周能做什么来验证这个判断。

[项目主页](https://skills.pixmoving.com/ambition-boundary/) · [下载 v1.1](https://skills.pixmoving.com/ambition-boundary/ambition-boundary-breaker-v1.1.zip) · [阅读 Skill](SKILL.md)

## 基线测试

模型从既有文本中学习，偏好对齐鼓励它回应用户的意图。当用户给出一个沿用过去经验的目标，Agent 会不会也默认接受它？我们做了一次配对测试。

四道题中，直接提问有 3 道提出了新的受益结果或研究问题，加载 Skill 后有 4 道。差异只出现在档案馆题。直接回答计算馆员能否核验 600 张照片，Skill 组还建议让居民按村名检索、参与辨认人物。两组在解释历史限制和使用反馈上都是 4/4。这次观测只发现一组差异，尚不足以判断 AI 普遍缺乏雄心，或估计 Skill 的稳定收益。

[查看图表和逐题回答](https://skills.pixmoving.com/ambition-boundary/#baseline)

## 试一试

> 我们是两人的维修培训团队，准备翻译十份教材。现在有 Agent，每周还能请两位师傅各给一小时，我们能追求什么更有野心的目标？

一个可能的目标是让学徒第一次遇到陌生故障时，也能解释下一步该查什么。取一章教材做成练习，请师傅听学徒讲解一个没见过的变式。这次观察能帮助团队决定，是否值得把练习扩展到整个设备系列。

## 工作方式

1. 描绘一个人或一个团队第一次能做到什么，由使用者选择值得追求的目标。
2. 沿实际工作过程找出 AI 能改变的环节，以及提速后会出现的下一个瓶颈。
3. 对没有标准答案的探索，估计获得可用反馈所需时间、每轮解决的不确定性，以及并行和连续实验的空间。结合具体流程，判断 Agent 长时程能力和可用算力增长能带来什么变化。
4. 做一次代价小、结果可观察的验证，据此扩大投入、修订目标或结束探索。

## 安装

下载并解压 ZIP。个人使用 Codex 时，将其中的文件夹放在 `~/.codex/skills/ambition-boundary-breaker/`。打开新对话，输入 `$ambition-boundary-breaker` 和你的问题。Skill 以中文编写，会要求 Agent 使用提问者的语言回答。

## 许可与署名

[MIT 许可证](LICENSE)

**Angelo Yu**

[PIX Moving](https://www.pixmoving.com/) 创始人兼 CEO

Agent 协作者：灌木丛（Guanmucong）

参与推理、框架综合、Skill 系统协同设计、文档与实现支持；该署名不代表法律人格、所有权、治理授权或责任主体地位。
