# 微博热搜分析工具 - 快速开始（增强版）

## 🚀 一键启动

```bash
/weibo_hotspot_analyzer
```

## ✨ 默认行为（已固化）

当你运行 `/weibo_hotspot_analyzer` 时，将自动执行以下流程：

### 1. 获取热搜数据
- 自动从微博API获取最新的15条热搜
- 保存到 `weibo_search_queries.json`

### 2. 搜索详细信息
- 对每个热搜话题执行WebSearch
- 收集新闻报道和背景信息

### 3. AI分析（含深度分析）
**基础分析**：
- 对15个话题进行评分（有趣度80分 + 有用度20分）
- 为≥60分的话题生成1个产品创意

**深度分析（自动触发）**：
- 自动识别≥80分的高分话题
- 为每个高分话题生成**3个不同维度**的产品创意
- 包含维度、核心功能、目标用户、独特价值

### 4. 生成增强版HTML报告
- 默认生成增强版报告
- 文件位置：`output/weibo_hotspot_analysis_enhanced_YYYYMMDD.html`
- 包含深度分析的特殊视觉效果

## 📊 预期输出

```
output/
└── weibo_hotspot_analysis_enhanced_20251203.html  (62KB)
    ├── 基础分析话题：9个（60-79分，每个1个创意）
    ├── 深度分析话题：4个（≥80分，每个3个创意）
    └── 产品创意总数：21个
```

## 🔥 深度分析示例

当发现高分话题时（如：理想AI眼镜Livis，88分），会自动生成3个创意：

```
创意1：AR生活助手眼镜（日常生活增强）
├─ 核心功能：实时翻译、卡路里识别、价格比价
└─ 独特价值：解放双手获得超能力般的信息增强体验

创意2：智能会议记录眼镜（商务办公场景）
├─ 核心功能：AI记录会议、识别发言人、生成待办
└─ 独特价值：彻底解放笔记负担，专注讨论本身

创意3：亲子互动AR眼镜（教育娱乐）
├─ 核心功能：AR故事投影、互动游戏、学习卡片识别
└─ 独特价值：将科技与亲子陪伴结合，创造独特体验
```

## 📁 生成的文件

**数据文件**：
- `weibo_search_queries.json` - 热搜查询数据
- `hotspot_analysis_results.json` - 基础分析结果
- `deep_dive_analysis.json` - 深度分析结果（≥80分话题）
- `enhanced_analysis_results.json` - 合并后的完整结果

**报告文件**：
- `output/weibo_hotspot_analysis_enhanced_YYYYMMDD.html` - **增强版**（推荐）
- `output/weibo_hotspot_analysis_apple_YYYYMMDD.html` - 基础版（备选）

## 🎯 如何查看结果

**方式1：自动打开（推荐）**
```bash
open output/weibo_hotspot_analysis_enhanced_$(date +%Y%m%d).html
```

**方式2：手动查找**
```bash
ls -lh output/
# 找到最新的 weibo_hotspot_analysis_enhanced_*.html 文件
```

**方式3：在Finder中打开**
- 打开 `output` 文件夹
- 双击最新的 `weibo_hotspot_analysis_enhanced_*.html` 文件

## ⚙️ 自定义选项

### 只生成基础版报告（不包含深度分析）

```bash
python3 generate_apple_style_report.py
```

### 重新生成增强版报告（使用已有数据）

```bash
python3 generate_enhanced_report.py
```

### 手动触发完整流程

```bash
python3 run_weibo_analyzer_enhanced.py
```

## 🔧 配置说明

所有配置已固化在 `.claude/commands/weibo_hotspot_analyzer.md` 中。

默认设置：
- ✅ 分析前15条热搜
- ✅ 深度分析阈值：≥80分
- ✅ 深度分析创意数：3个/话题
- ✅ 基础创意阈值：≥60分
- ✅ 默认生成增强版报告

## 📈 统计信息示例

运行后可以看到：

```
✅ 分析完成：共 15 个热搜话题
   💡 生成产品创意：9 个（≥60分）
   🔥 深度分析话题：4 个（≥80分）
   📊 产品创意总数：21 个
   📈 平均评分：61.1 分
```

## 💡 提示

1. **首次运行**：确保已安装依赖 `pip install requests`
2. **查看报告**：推荐使用Chrome/Safari浏览器打开HTML报告
3. **交互功能**：报告中的"按评分排序"按钮可以对话题重新排序
4. **响应式设计**：支持桌面、平板、移动设备查看

## 🆘 故障排除

**Q: 提示找不到分析结果文件？**
A: 确保已经完成步骤2（WebSearch）和步骤3（AI分析）

**Q: 没有深度分析内容？**
A: 检���是否有话题评分≥80分，如果没有则不会触发深度分析

**Q: 如何修改深度分析阈值？**
A: 当前阈值固定为80分，如需修改请编辑 `generate_enhanced_report.py`

## 📚 更多文档

- `ENHANCEMENT_SUMMARY.md` - 详细的增强功能说明
- `README.md` - 完整项目文档
- `.claude/commands/weibo_hotspot_analyzer.md` - Slash command定义

---

**版本**: v2.0 Enhanced
**最后更新**: 2025-12-03
**状态**: ✅ 已固化，下次运行自动使用增强版
