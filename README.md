# 太迪杯 - 智能财报问答系统

> 基于 LLM 的智能财报问答平台，支持 Text2SQL、自然语言查询、数据可视化

---

## 项目概述

本项目是一个**智能财报问答系统**，能够：
- 将自然语言问题自动转换为 SQL 查询
- 多轮对话理解财务问题并给出答案
- 自动生成数据可视化图表
- 支持 OpenAI、DeepSeek、Gemini 等多种 LLM

---

## 快速链接

| 文档 | 说明 |
|------|------|
| [团队协作指南.md](团队协作指南.md) | Git 协作、分支管理、PR 流程 |
| [financial-assistant/操作指南.md](financial-assistant/操作指南.md) | 完整技术文档、配置说明、常见问题 |
| [financial-assistant/快速启动指南.md](financial-assistant/快速启动指南.md) | 5 分钟快速上手 |

---

## 项目结构

```
taidi_cup_B/
├── 团队协作指南.md           # Git 协作指南（新人必看）
├── financial-assistant/       # 主应用
│   ├── 操作指南.md          # 详细技术文档
│   ├── 快速启动指南.md      # 快速启动
│   └── chatbot_financial_statement/
│       ├── home.py          # Streamlit 入口
│       ├── pages/            # 页面组件
│       ├── agent/            # AI 代理核心
│       └── ETL/              # 数据导入
```

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/smooth-QAQ/taidi_cup_B.git
cd taidi_cup_B
```

### 2. 查看详细指南

- **新人必看**：[团队协作指南.md](团队协作指南.md)
- **技术文档**：[financial-assistant/操作指南.md](financial-assistant/操作指南.md)

### 3. 技术栈

| 组件 | 技术 |
|------|------|
| LLM | OpenAI GPT / DeepSeek / Gemini / vLLM |
| 数据库 | PostgreSQL + ChromaDB |
| 前端 | Streamlit |
| 容器 | Docker + Docker Compose |

---

## 团队成员

- **管理员**：smooth-QAQ
- **队员**：待添加

---

## 联系方式

- 仓库：https://github.com/smooth-QAQ/taidi_cup_B
- 问题反馈：提交 GitHub Issue 或联系管理员

---

*最后更新：2026-04-19*
