# GitHub Actions 部署指南 - Claude Agent SDK 方案

本文档详细说明如何将微博热搜分析器迁移到 GitHub Actions，使用 Claude Agent SDK 实现云端定时执行。

## 📋 目录

1. [方案概述](#方案概述)
2. [前置准备](#前置准备)
3. [配置步骤](#配置步骤)
4. [测试验证](#测试验证)
5. [成本估算](#成本估算)
6. [故障排查](#故障排查)

---

## 方案概述

### 架构设计

```
┌─────────────────────────────────────────────────────────┐
│              GitHub Actions (Ubuntu Runner)              │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  1. 获取微博热搜 (天行数据API)                    │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │  2. Claude API 搜索热点详情                       │   │
│  │     (使用 Anthropic Python SDK)                   │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │  3. Claude API 分析产品创意                       │   │
│  │     - 基础分析 (15个话题)                         │   │
│  │     - 深度分析 (≥80分话题)                        │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │  4. 生成 HTML 报告                                │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │  5. 提交到仓库 / 部署到 GitHub Pages              │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### 核心特性

- ✅ **完全自动化** - 无需人工干预
- ✅ **定时执行** - 每天早晚各执行一次
- ✅ **成本可控** - 约 $15-25/月
- ✅ **报告归档** - 自动保存历史报告
- ✅ **失败通知** - 执行失败时自动通知
- ✅ **手动触发** - 支持随时手动运行

---

## 前置准备

### 1. 注册 Anthropic API Key

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册账号并登录
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制并保存 API Key（格式：`sk-ant-...`）

**重要提示：**
- API Key 只显示一次，请妥善保存
- 建议设置使用限额，避免超支
- 推荐使用 Claude 3.5 Sonnet 模型（性价比最高）

### 2. 准备 GitHub 仓库

1. 在 GitHub 创建新仓库（或使用现有仓库）
2. 将项目代码推送到仓库
3. 确保仓库包含以下文件：
   - `.github/workflows/weibo-analyzer-agent-sdk.yml`
   - `run_agent_sdk_analyzer.py`
   - `generate_enhanced_report.py`
   - `requirements.txt`

### 3. 配置 GitHub Secrets

进入仓库设置页面：`Settings` → `Secrets and variables` → `Actions`

添加以下 Secrets：

| Secret 名称 | 说明 | 示例值 |
|------------|------|--------|
| `ANTHROPIC_API_KEY` | Claude API Key | `sk-ant-api03-xxx...` |
| `TIANAPI_KEY` | 天行数据API Key（可选） | `c96a7333c975965e491ff49466a1844b` |

**配置步骤：**
1. 点击 `New repository secret`
2. 输入 Secret 名称
3. 粘贴 Secret 值
4. 点击 `Add secret`

---

## 配置步骤

### 步骤 1：创建 GitHub Actions Workflow

文件已创建：[.github/workflows/weibo-analyzer-agent-sdk.yml](.github/workflows/weibo-analyzer-agent-sdk.yml)

**关键配置说明：**

```yaml
on:
  schedule:
    # 每天早上9点和晚上9点执行（北京时间）
    - cron: '0 1,13 * * *'  # UTC时间
  workflow_dispatch:  # 支持手动触发
```

**定时任务说明：**
- `0 1 * * *` = UTC 1:00 = 北京时间 9:00
- `0 13 * * *` = UTC 13:00 = 北京时间 21:00

**修改执行时间：**
如需修改执行时间，编辑 cron 表达式：
```
分钟 小时 日 月 星期
0-59 0-23 1-31 1-12 0-6
```

示例：
- 每小时执行：`0 * * * *`
- 每天中午12点：`0 4 * * *`（UTC 4:00 = 北京时间 12:00）
- 仅工作日执行：`0 1 * * 1-5`

### 步骤 2：创建主执行脚本

文件已创建：[run_agent_sdk_analyzer.py](run_agent_sdk_analyzer.py)

**脚本功能：**
1. 使用 Anthropic Python SDK 调用 Claude API
2. 获取微博热搜数据
3. 分析产品创意（基础 + 深度）
4. 保存 JSON 结果文件

**环境变量：**
- `ANTHROPIC_API_KEY` - Claude API Key（必需）
- `TIANAPI_KEY` - 天行数据API Key（可选，有默认值）
- `MAX_TOPICS` - 分析的热搜数量（默认15）

### 步骤 3：更新依赖文件

编辑 `requirements.txt`，添加 Anthropic SDK：

```txt
requests>=2.31.0
anthropic>=0.18.0
```

### 步骤 4：提交代码到 GitHub

```bash
# 添加所有新文件
git add .github/workflows/weibo-analyzer-agent-sdk.yml
git add run_agent_sdk_analyzer.py
git add GITHUB_ACTIONS_DEPLOYMENT.md
git add requirements.txt

# 提交
git commit -m "feat: 添加 GitHub Actions 自动化支持"

# 推送到远程仓库
git push origin main
```

---

## 测试验证

### 方法 1：手动触发 Workflow

1. 进入 GitHub 仓库页面
2. 点击 `Actions` 标签
3. 选择 `微博热搜分析 (Claude Agent SDK)` workflow
4. 点击 `Run workflow` 按钮
5. 选择分支（通常是 `main`）
6. 可选：修改 `max_topics` 参数（默认15）
7. 点击 `Run workflow` 确认

### 方法 2：等待定时触发

定时任务会在设定的时间自动执行：
- 北京时间 9:00（UTC 1:00）
- 北京时间 21:00（UTC 13:00）

### 查看执行日志

1. 进入 `Actions` 页面
2. 点击最近的 workflow 运行记录
3. 查看各个步骤的执行日志
4. 检查是否有错误或警告

### 验证输出结果

执行成功后，检查以下内容：

1. **JSON 文件**（提交到仓库）
   - `weibo_search_queries.json`
   - `hotspot_analysis_results.json`
   - `deep_dive_analysis.json`

2. **HTML 报告**（在 `output/` 目录）
   - `weibo_hotspot_analysis_enhanced_YYYYMMDD.html`

3. **Artifacts**（可下载）
   - 点击 workflow 运行记录
   - 滚动到底部查看 `Artifacts` 部分
   - 下载 `weibo-analysis-report-XXX.zip`

4. **GitHub Pages**（如果启用）
   - 访问 `https://<username>.github.io/<repo-name>/`
   - 查看最新的 HTML 报告

---

## 成本估算

### Claude API 成本

**模型：Claude 3.5 Sonnet**

| 项目 | 数量 | Token 消耗 | 单价 | 成本 |
|------|------|-----------|------|------|
| 输入 Token | ~2000/次 | 30,000/天 | $3/M | $0.09/天 |
| 输出 Token | ~1000/次 | 15,000/天 | $15/M | $0.23/天 |
| **每天总计** | 2次执行 | - | - | **$0.64/天** |
| **每月总计** | 60次执行 | - | - | **$19.20/月** |

**优化建议：**
- 使用 Claude 3.5 Haiku 进行初步筛选（便宜10倍）
- 只对高分话题使用 Sonnet 进行深度分析
- 预计可降低至 **$10-15/月**

### GitHub Actions 成本

- **公开仓库**：完全免费 ✅
- **私有仓库**：
  - 免费额度：2000分钟/月
  - 每次执行约15分钟
  - 每月使用：900分钟
  - 成本：**免费**（在额度内）

### 总成本

- **最低成本**：$10/月（优化后）
- **预期成本**：$15-20/月
- **最高成本**：$25/月（未优化）

---

## 故障排查

### 问题 1：API Key 无效

**错误信息：**
```
❌ 未设置 ANTHROPIC_API_KEY 环境变量
```

**解决方法：**
1. 检查 GitHub Secrets 是否正确配置
2. 确认 Secret 名称为 `ANTHROPIC_API_KEY`（区分大小写）
3. 重新生成 API Key 并更新 Secret

### 问题 2：API 调用失败

**错误信息：**
```
anthropic.APIError: Rate limit exceeded
```

**解决方法：**
1. 检查 API 使用限额
2. 在 Anthropic Console 增加限额
3. 减少 `MAX_TOPICS` 参数（默认15）
4. 增加请求间隔时间

### 问题 3：JSON 解析失败

**错误信息：**
```
⚠️ JSON 解析失败: Expecting value
```

**解决方法：**
1. 检查 Claude 返回的原始响应
2. 可能是 prompt 不够明确
3. 脚本已包含自动清理 markdown 代码块的逻辑
4. 如果持续失败，使用 fallback 结果

### 问题 4：Workflow 执行超时

**错误信息：**
```
Error: The operation was canceled.
```

**解决方法：**
1. 检查 `timeout-minutes` 设置（默认60分钟）
2. 减少分析的话题数量
3. 优化 API 调用逻辑（并发处理）

### 问题 5：报告未生成

**可能原因：**
- 分析结果文件不存在
- Python 脚本执行失败
- 文件权限问题

**解决方法：**
1. 检查 `hotspot_analysis_results.json` 是否存在
2. 查看 `generate_enhanced_report.py` 的执行日志
3. 手动运行脚本测试：
   ```bash
   python3 generate_enhanced_report.py
   ```

---

## 下一步

完成部署后，你可以：

1. **监控执行情况**
   - 定期查看 Actions 页面
   - 检查执行日志
   - 验证报告质量

2. **优化成本**
   - 使用 Haiku 模型进行初步筛选
   - 调整执行频率
   - 设置 API 使用限额

3. **增强功能**
   - 添加邮件通知
   - 集成 Slack/钉钉通知
   - 自动发布到社交媒体

4. **数据分析**
   - 分析历史趋势
   - 生成周报/月报
   - 可视化数据展示

---

## 相关文档

- [README.md](README.md) - 项目总览
- [QUICK_START_ENHANCED.md](QUICK_START_ENHANCED.md) - 本地运行指南
- [Anthropic API 文档](https://docs.anthropic.com/)
- [GitHub Actions 文档](https://docs.github.com/actions)

---

**最后更新：** 2026-01-14
**维护者：** Claude Code
