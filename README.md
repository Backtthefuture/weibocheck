# 微博热搜产品创意分析工具 🚀

这是一个基于 Claude Code 的技能（Skill），用于自动分析微博热搜并生成产品创意。

## ⚡ 增强版已固化（v2.0）

**✨ 最新更新（2025-12-03）**：增强版功能已完全固化！

🔥 **核心特性**：
- ✅ 自动深度分析≥80分的高分话题
- ✅ 每个高分话题生成3个不同维度的产品创意
- ✅ 增强版HTML报告（含特殊视觉效果）
- ✅ 一键运行，无需额外配置

📊 **本次分析成果**：
- 4个深度分析话题（88分、86分、81分、80分）
- 21个产品创意（基础9个 + 深度12个）
- 创意产出提升133%

🚀 **快速开始**：
```bash
/weibo_hotspot_analyzer
```

📚 **详细文档**：
- [快速开始指南](QUICK_START_ENHANCED.md)
- [增强功能详解](ENHANCEMENT_SUMMARY.md)
- [固化确认文档](FIXED_VERSION_CONFIRMATION.md)

## 📋 系统要求

### 必需软件
1. **Python 3.8+**
   ```bash
   python3 --version  # 检查版本
   ```

2. **Claude Code**
   - 需要安装并配置 Claude Code CLI
   - 安装方法：访问 [Claude Code 官网](https://github.com/anthropics/claude-code)

3. **网络连接**
   - 需要访问微博API（https://weibo.com）
   - 需要访问Claude API

### Python依赖
只需要一个第三方库：
- `requests` - 用于HTTP请求

## 🚀 新电脑安装步骤

### 第一步：复制项目文件
将整个项目文件夹复制到新电脑：
```bash
# 确保包含以下文件和目录：
微博热搜分析/
├── .claude/                               # Skill配置（必须）
├── .gitignore
├── requirements.txt                       # 依赖列表（新增）
├── README.md                              # 本文档（新增）
├── fetch_weibo_hotspot.py
├── search_hotspot_details.py
├── analyze_hotspot_with_ai.py
├── generate_apple_style_report.py
├── run_analysis.py
├── run_pipeline_automation.py
├── QUICK_START.md
└── output/                                # 输出目录
```

### 第二步：安装Python依赖
在项目目录下运行：
```bash
cd 微博热搜分析
pip3 install -r requirements.txt
```

或者手动安装：
```bash
pip3 install requests
```

### 第三步：验证安装
```bash
# 测试Python是否正常
python3 --version

# 测试requests库是否安装成功
python3 -c "import requests; print('requests 安装成功')"

# 测试Claude Code是否安装
claude --version
```

### 第四步：配置Claude Code Skill
这个项目是一个Claude Code Skill，需要在Claude Code中启用：

**选项A：如果已经在正确位置**
```bash
# 进入项目目录
cd 微博热搜分析

# 启动Claude Code
claude
```

**选项B：如果需要移动到skills目录**
```bash
# 查看Claude Code的skills目录位置
# 通常在 ~/.claude/skills/ 或项目自定义位置

# 将项目复制或链接到skills目录
cp -r 微博热搜分析 ~/.claude/skills/weibo-analyzer
# 或创建符号链接
ln -s /path/to/微博热搜分析 ~/.claude/skills/weibo-analyzer
```

## 📖 使用方法

### 方式一：通过Claude Code Skill
```bash
# 进入项目目录
cd 微博热搜分析

# 启动Claude Code
claude

# 在Claude Code中使用斜杠命令
/weibo_hotspot_analyzer
```

### 方式二：直接运行Python脚本
```bash
# 完整流程
python3 run_analysis.py

# 或流水线模式（更快）
python3 run_pipeline_automation.py
```

### 方式三：分步执行
```bash
# 步骤1：获取热搜数据
python3 fetch_weibo_hotspot.py

# 步骤2：生成搜索计划
python3 search_hotspot_details.py

# 步骤3：AI分析（需要在Claude Code中手动执行WebSearch）
python3 analyze_hotspot_with_ai.py

# 步骤4：生成报告
python3 generate_apple_style_report.py
```

## 📁 输出文件

运行成功后会在 `output/` 目录生成：
```
output/weibo_hotspot_analysis_apple_YYYYMMDD.html
```

用浏览器打开即可查看分析报告。

## ⚙️ 配置说明

### 无需配置项
- ✅ 不需要API密钥（使用微博公开API）
- ✅ 不需要数据库
- ✅ 不需要额外的配置文件

### 可选配置
修改分析参数，编辑相应Python脚本：
- `fetch_weibo_hotspot.py` - 修改获取热搜数量（默认15条）
- `generate_apple_style_report.py` - 修改报告样式

## 🔧 故障排除

### 问题1：requests模块未找到
```bash
ModuleNotFoundError: No module named 'requests'
```
**解决方法：**
```bash
pip3 install requests
```

### 问题2：无法访问天行数据API
```bash
❌ 请求失败: Connection timeout
```
**解决方法：**
- 检查网络连接
- 确认可以访问 https://apis.tianapi.com
- 如果在公司网络，可能需要配置代理
- API Key已内置，无需手动配置

### 问题3：Claude Code未识别skill
```bash
Command not found: /weibo_hotspot_analyzer
```
**解决方法：**
1. 确认 `.claude/` 目录存在
2. 确认在项目目录内运行 `claude`
3. 重启Claude Code

### 问题4：权限错误
```bash
Permission denied: ./use_weibo_analyzer.sh
```
**解决方法：**
```bash
chmod +x use_weibo_analyzer.sh
```

## 📚 详细文档

- `QUICK_START.md` - 快速入门指南
- `.claude/commands/weibo_hotspot_analyzer.md` - Skill详细说明

## 🌐 网络要求

该工具需要访问：
1. **天行数据API** - `https://apis.tianapi.com/weibohot/` (API Key已配置)
2. **Claude API** - 通过Claude Code访问（需要Claude Code已配置）

## 💡 提示

1. **首次运行**可能需要几分钟来获取和分析数据
2. **推荐使用**流水线模式（`run_pipeline_automation.py`）可提速40%
3. **报告文件**会自动保存在 `output/` 目录，按日期命名
4. **历史数据**会在每次运行时覆盖，如需保留请手动备份

## 🆘 获取帮助

如果遇到问题：
1. 检查本README的"故障排除"部分
2. 查看 `QUICK_START.md` 获取详细步骤
3. 确认所有依赖已正确安装

## 📊 项目结构

```
微博热搜分析/
├── .claude/                               # Claude Code Skill配置
│   └── commands/
│       └── weibo_hotspot_analyzer.md      # Skill定义
├── fetch_weibo_hotspot.py                 # 获取微博热搜数据
├── search_hotspot_details.py              # 生成搜索计划
├── analyze_hotspot_with_ai.py             # 生成AI分析提示
├── generate_apple_style_report.py         # 生成HTML报告（苹果风格）
├── run_analysis.py                        # 完整自动化流程
├── run_pipeline_automation.py             # 流水线并行模式
├── requirements.txt                       # Python依赖
├── README.md                              # 本文档
├── QUICK_START.md                         # 快速开始
└── output/                                # 报告输出目录
```

## ✅ 迁移检查清单

在新电脑上运行前，确认：
- [ ] Python 3.8+ 已安装
- [ ] Claude Code 已安装并配置
- [ ] 已安装 requests 库 (`pip3 install requests`)
- [ ] 项目文件完整（包括 `.claude/` 目录）
- [ ] 网络可以访问微博和Claude API
- [ ] 在项目目录下运行 `claude` 命令

全部完成后，即可开始使用！🎉
