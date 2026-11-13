# 🃏 桥牌叫牌学习笔记 (Bridge Bidding Notes)

这是一个基于 [Astro](https://astro.build/) 构建的纯静态、渐进式桥牌叫牌教学网站。网站以“自然叫牌法/2/1体系”为基础，从基础开叫开始，逐步深入至应叫、约定叫及竞争叫。

本项目专为桥牌初学者设计，通过大量直观的表格、互动式选择题和牌例演示，帮助读者快速建立完整的叫牌逻辑。

## 📂 目录

```text
bridge-notes/
├── public/                 # 静态资源（图片、图标等）
├── src/
│   ├── content/            # (可选) Astro 内容集合
│   ├── layouts/
│   │   └── Layout.astro    # 全局页面布局
│   ├── pages/
│   │   ├── index.astro     # 网站首页（跳转至目录）
│   │   └── chapters/       # 所有教学章节（Markdown 文件）
│   │       ├── index.md                # 课程大纲
│   │       ├── 01-normal-opening.md    # 第一章：正常开叫与阻击
│   │       ├── 02-first-response.md    # 第二章：一阶花色应叫
│   │       ├── 03-nt-response.md       # 第三章：无将应叫
│   │       ├── 04-strong-response.md   # 第四章：2♣ 强牌应叫
│   │       ├── 05-preemptive-opening.md# 第五章：应叫阻击叫
│   │       └── 06-competitive-bidding.md# 第六章：竞争叫
└── package.json
```