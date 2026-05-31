# AI OSS Radar

[![CI](https://github.com/renjingzhuo-maker/AI-/actions/workflows/ci.yml/badge.svg)](https://github.com/renjingzhuo-maker/AI-/actions/workflows/ci.yml)

AI OSS Radar 是一个用于自动发现并评估 AI GitHub 仓库的开源项目。它会从三个维度给仓库打分：使用情况、生态系统重要性和活跃度，帮助开发者更快判断一个 AI 项目是否值得学习、依赖或参与贡献。

## 项目亮点

- 评分维度清晰：综合 stars、forks、watchers、topic、license、语言、更新时间和 issue 压力。
- 可直接运行：提供 Python CLI，可以读取本地 JSON，也可以调用 GitHub API 发现仓库。
- 易于扩展：评分逻辑集中在独立模块，后续可以继续加入发布频率、贡献者健康度和依赖生态分析。
- GitHub 友好：包含测试、CI、贡献指南、Issue 模板和安全说明，适合作为长期维护的开源仓库。

## 快速开始

```bash
cd ai-oss-radar
python -m pip install -e .
ai-oss-radar score --input examples/seed_repositories.json
```

生成 Markdown 报告：

```bash
cd ai-oss-radar
ai-oss-radar score --input examples/seed_repositories.json --output examples/sample_report.md
```

搜索真实 GitHub AI 仓库：

```bash
cd ai-oss-radar
GITHUB_TOKEN=your_token ai-oss-radar discover --topic llm --min-stars 1000 --limit 25
```

`GITHUB_TOKEN` 不是必须的，但建议设置，否则 GitHub API 容易触发限流。

## 仓库结构

```text
ai-oss-radar/
  src/ai_oss_radar/       核心代码
  tests/                  单元测试
  examples/               示例输入和示例报告
  docs/                   评分模型说明
```

## 示例结果

| Rank | Repository | Overall | Usage | Ecosystem | Activity |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | huggingface/transformers | 94.73 | 100.00 | 93.18 | 90.40 |
| 2 | langchain-ai/langchain | 93.99 | 99.73 | 89.46 | 92.56 |

完整项目文档在 [ai-oss-radar/README.md](ai-oss-radar/README.md)，评分模型说明在 [ai-oss-radar/docs/scoring.md](ai-oss-radar/docs/scoring.md)。

## 许可证

MIT
