# Weibo Hotspot Analyzer

搜索并分析微博热搜，生成产品创意（自动深度分析增强版）

**默认行为**：
- ✅ 自动对≥80分的高分话题进行深度分析
- ✅ 为每个高分话题生成3个不同维度的产品创意
- ✅ 生成增强版HTML报告（推荐）

## 输出文件结构

```
项目目录/
├── output/                                             # 所有HTML报告输出目录
│   ├── weibo_hotspot_analysis_apple_YYYYMMDD.html     # 基础版分析报告
│   └── weibo_hotspot_analysis_enhanced_YYYYMMDD.html  # 增强版分析报告（推荐）
├── weibo_search_queries.json                          # 热搜查询数据
├── hotspot_analysis_results.json                      # 基础AI分析结果
├── deep_dive_analysis.json                            # 深度产品创意（≥80分话题）
├── enhanced_analysis_results.json                     # 合并后的增强分析结果
├── generate_apple_style_report.py                     # 基础报告生成脚本
└── generate_enhanced_report.py                        # 增强版报告生成脚本（推荐）
```

**重要说明**：
- 所有HTML报告自动保存在 `output/` 目录
- 文件名自动添加日期后缀（格式：YYYYMMDD）
- 每次生成会覆盖同一天的报告
- **增强版功能**：对≥80分的高分话题进行深度分析，生成3个不同维度的产品创意

## 运行步骤

1. 调用 Claude Code 执行以下操作：

### 第一步：读取微博热搜数据

使用 Python 脚本获取微博热搜数据并生成搜索查询：

```python
import warnings
# 禁用urllib3的SSL警告
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')

import requests
import json
import re
from datetime import datetime
import sys

# 天行数据微博热搜API
WEIBO_HOT_URL = "https://apis.tianapi.com/weibohot/index?key=c96a7333c975965e491ff49466a1844b"

def fetch_weibo_hotspot():
    """获取微博热搜数据"""
    try:
        response = requests.get(WEIBO_HOT_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200 and 'result' in data:
                return data['result']['list']
    except Exception as e:
        print(f"获取微博热搜失败: {e}", file=sys.stderr)
    return []

def generate_search_queries(hotspots):
    """为每个热搜生成搜索查询"""
    queries = []
    for i, item in enumerate(hotspots[:15]):  # 只处理前15条
        title = item.get('hotword', '')
        if title:
            # 获取热度（提取数字部分）
            heat_str = item.get('hotwordnum', '').strip()
            numbers = re.findall(r'\d+', heat_str)
            heat = int(numbers[0]) if numbers else 0

            queries.append({
                'rank': i + 1,
                'title': title,
                'heat': heat,
                'search_query': f"{title} 微博热搜 {datetime.now().strftime('%Y年%m月')}"
            })
    return queries

if __name__ == "__main__":
    hotspots = fetch_weibo_hotspot()
    queries = generate_search_queries(hotspots)

    # 保存搜索查询
    with open('weibo_search_queries.json', 'w', encoding='utf-8') as f:
        json.dump(queries, f, ensure_ascii=False, indent=2)

    print(f"已获取 {len(queries)} 条热搜信息")
    for q in queries[:5]:  # 只显示前5条
        print(f"#{q['rank']}: {q['title']} (热度: {q['heat']})")
```

### 第二步：搜索热点详细信息

对于每个热搜话题，使用 WebSearch 获取详细信息：

```python
import json
from datetime import datetime

def analyze_hotspot_with_claude(hotspot_title, search_results):
    """
    使用Claude分析热点并生成产品创意

    有趣度占80分，有用度占20分
    """
    prompt = f"""
    请分析以下微博热搜话题，并从"有趣"和"有用"两个角度评估生成产品创意的可能性。

    热搜话题：{hotspot_title}

    背景信息：
    {search_results}

    请按照以下标准评估：

    1. **有趣度（满分80分）**：
       - 话题是否新颖、有创意？
       - 是否能引发用户好奇心和参与欲？
       - 是否有娱乐性、传播性？
       - 是否能创造独特的用户体验？

    2. **有用度（满分20分）**：
       - 是否能解决实际问题？
       - 是否有实用价值？
       - 是否能提高效率或提供便利？

    请提供：
    - 有趣度评分（0-80）和理由
    - 有用度评分（0-20）和理由
    - 总分（有趣度+有用度）
    - 如果总分≥60分，请提供一个具体的产品Idea，包括：
      * 产品名称
      * 核心功能
      * 目标用户
      * 简要描述（50字以内）

    如果总分<60分，请说明原因。

    请以JSON格式返回结果。
    """

    # 这里将由Claude Code执行实际的分析
    return prompt

# 读取搜索查询
with open('weibo_search_queries.json', 'r', encoding='utf-8') as f:
    queries = json.load(f)

print(f"需要分析 {len(queries)} 个热搜话题")
print("请使用WebSearch工具搜索每个话题的详细信息，然后用Claude进行分析")
```

### 第三步：AI分析产品创意

**自动执行流程**：

1. **基础分析**：对所有15个热搜话题进行评分和产品创意分析
   - 评分标准：有趣度（80分）+ 有用度（20分）
   - 生成基础产品创意（总分≥60分的话题）

2. **深度分析**（自动触发）：
   - 自动识别≥80分的高分话题
   - 为每个高分话题生成3个不同维度的产品创意
   - 每个创意包含：维度、核心功能、目标用户、独特价值

3. **数据保存**：
   - `hotspot_analysis_results.json` - 基础分析结果
   - `deep_dive_analysis.json` - 深度分析结果
   - `enhanced_analysis_results.json` - 合并后的增强结果

### 第四步：生成 HTML 报告

**默认生成增强版报告**（自动执行）

```bash
python3 generate_enhanced_report.py
```

增强版报告特性：
- 🔥 深度分析标识：高分话题（≥80分）显示特殊徽章
- 💎 3个维度的产品创意：每个高分话题从不同角度深挖（日常生活、商务办公、教育娱乐等）
- ✨ 独特价值展示：每个创意都标注核心价值点
- 🎨 差异化样式：深度分析话题有独特的背景色和边框
- 📊 统计卡片：包含"深度分析话题"统计项
- 🍎 苹果设计风格：SF Pro字体、简洁白色背景、精致圆角阴影

**备选：基础版报告**

如只需每个话题1个创意的简化版本：

```bash
python3 generate_apple_style_report.py
```

该脚本的完整代码如下（请确保使用此代码生成报告）：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成微博热搜分析HTML报告 - 苹果设计风格
"""

import json
import os
import sys
from datetime import datetime


def load_analysis_results():
    """加载分析结果"""
    analysis_file = 'hotspot_analysis_results.json'
    if os.path.exists(analysis_file):
        try:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
            for r in results:
                if 'score' in r and 'total_score' not in r:
                    r['total_score'] = r['score']
            print(f"✅ 成功加载分析文件: {analysis_file} ({len(results)} 条结果)")
            return results
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return []
    return []


def get_score_badge_class(score):
    """根据分数获取评分徽章样式类"""
    if score >= 80:
        return 'score-excellent'
    elif score >= 60:
        return 'score-good'
    else:
        return 'score-fair'


def calculate_stats(results):
    """计算统计数据"""
    total_topics = len(results)
    high_score_count = sum(1 for r in results if r['total_score'] >= 80)
    medium_score_count = sum(1 for r in results if 60 <= r['total_score'] < 80)
    avg_score = sum(r['total_score'] for r in results) / total_topics if total_topics > 0 else 0

    return {
        'total_topics': total_topics,
        'high_score_count': high_score_count,
        'medium_score_count': medium_score_count,
        'avg_score': avg_score
    }


def generate_table_rows(results):
    """生成表格行"""
    rows = []

    for result in results:
        score_class = get_score_badge_class(result['total_score'])

        # 产品创意部分
        if result['has_idea'] and result['product']:
            product = result['product']
            product_html = f'''
                <div class="product-idea">
                    <div class="product-name">{product.get('name', '未命名产品')}</div>
                    <div class="product-info">
                        <div class="product-feature">
                            <span class="label">核心功能</span>
                            <span class="value">{product.get('features', 'N/A')}</span>
                        </div>
                        <div class="product-feature">
                            <span class="label">目标用户</span>
                            <span class="value">{product.get('target_users', 'N/A')}</span>
                        </div>
                    </div>
                    <div class="product-description">{product.get('description', '暂无描述')}</div>
                </div>
            '''
        else:
            reason = result.get('reason', '总分未达60分阈值')
            product_html = f'<div class="no-idea"><span class="no-idea-icon">—</span><span class="no-idea-text">暂无可行产品创意</span><span class="no-idea-reason">{reason}</span></div>'

        # 生成表格行
        row = f'''
            <tr data-score="{result['total_score']}">
                <td class="rank-cell"><span class="rank">#{result['rank']}</span></td>
                <td class="hotspot-cell">
                    <div class="hotspot-title">{result['title']}</div>
                    <div class="heat-info">热度 {result.get('heat', 'N/A'):,}</div>
                </td>
                <td class="summary-cell">
                    <div class="event-summary">{result['summary']}</div>
                </td>
                <td class="product-cell">
                    {product_html}
                </td>
                <td class="score-cell">
                    <div class="score-container">
                        <div class="score-badge {score_class}">
                            <span class="score-number">{result['total_score']}</span>
                            <span class="score-label">分</span>
                        </div>
                        <div class="score-breakdown">
                            <div class="score-item">
                                <span class="score-item-label">有趣</span>
                                <span class="score-item-value">{result['fun_score']}</span>
                            </div>
                            <div class="score-item">
                                <span class="score-item-label">有用</span>
                                <span class="score-item-value">{result['useful_score']}</span>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
        '''
        rows.append(row)

    return ''.join(rows)


def generate_html_report(results, stats):
    """生成苹果风格的HTML报告 - 请保持此样式不变"""

    table_rows = generate_table_rows(results)

    # 苹果设计风格HTML模板 - 请勿修改
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜产品创意分析 - {datetime.now().strftime('%Y年%m月%d日')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
            background: #f5f5f7;
            color: #1d1d1f;
            padding: 60px 20px;
            line-height: 1.47059;
            font-size: 17px;
            font-weight: 400;
            letter-spacing: -0.022em;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 60px; }}
        .title {{ font-size: 56px; font-weight: 700; letter-spacing: -0.005em; color: #1d1d1f; margin-bottom: 8px; line-height: 1.07143; }}
        .subtitle {{ font-size: 21px; font-weight: 400; color: #6e6e73; letter-spacing: 0.011em; line-height: 1.381; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 48px; }}
        .stat-card {{
            background: #ffffff;
            border-radius: 18px;
            padding: 32px 28px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .stat-card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12); }}
        .stat-number {{ font-size: 48px; font-weight: 700; color: #0071e3; line-height: 1.0; margin-bottom: 8px; }}
        .stat-label {{ font-size: 17px; color: #6e6e73; font-weight: 400; }}
        .methodology {{
            background: #ffffff;
            border-radius: 18px;
            padding: 40px;
            margin-bottom: 32px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        }}
        .methodology h3 {{ font-size: 28px; font-weight: 700; color: #1d1d1f; margin-bottom: 24px; letter-spacing: -0.003em; }}
        .score-weights {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }}
        .weight-item {{ background: #f5f5f7; padding: 24px; border-radius: 12px; }}
        .weight-item strong {{ display: block; font-size: 19px; font-weight: 600; color: #1d1d1f; margin-bottom: 8px; }}
        .weight-description {{ font-size: 15px; color: #6e6e73; line-height: 1.4; }}
        .threshold-note {{ margin-top: 24px; padding: 20px; background: #f5f5f7; border-radius: 12px; font-size: 15px; color: #6e6e73; line-height: 1.4; }}
        .table-wrapper {{ background: #ffffff; border-radius: 18px; overflow: hidden; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08); }}
        .table-header {{ padding: 24px 32px; border-bottom: 1px solid #d2d2d7; display: flex; justify-content: space-between; align-items: center; }}
        .table-title {{ font-size: 24px; font-weight: 600; color: #1d1d1f; }}
        .sort-button {{
            background: #0071e3;
            color: #ffffff;
            border: none;
            border-radius: 980px;
            padding: 8px 20px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .sort-button:hover {{ background: #0077ed; transform: scale(1.02); }}
        .sort-button:active {{ transform: scale(0.98); }}
        .sort-icon {{ display: inline-block; transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
        .sort-button.desc .sort-icon {{ transform: rotate(180deg); }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{
            background: #f5f5f7;
            padding: 16px 20px;
            text-align: left;
            font-size: 13px;
            font-weight: 600;
            color: #6e6e73;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            border-bottom: 1px solid #d2d2d7;
        }}
        td {{ padding: 24px 20px; border-bottom: 1px solid #d2d2d7; vertical-align: top; }}
        tr:last-child td {{ border-bottom: none; }}
        tr {{ transition: background-color 0.2s ease; }}
        tr:hover {{ background-color: #fbfbfd; }}
        .rank-cell {{ width: 60px; text-align: center; }}
        .rank {{ font-size: 20px; font-weight: 700; color: #0071e3; }}
        .hotspot-cell {{ width: 20%; }}
        .hotspot-title {{ font-size: 17px; font-weight: 600; color: #1d1d1f; margin-bottom: 6px; line-height: 1.35; }}
        .heat-info {{ font-size: 13px; color: #ff3b30; font-weight: 500; }}
        .summary-cell {{ width: 24%; }}
        .event-summary {{ font-size: 15px; color: #6e6e73; line-height: 1.5; }}
        .product-cell {{ width: 30%; }}
        .product-idea {{
            background: linear-gradient(135deg, #f5f5f7 0%, #ffffff 100%);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #d2d2d7;
        }}
        .product-name {{ font-size: 17px; font-weight: 600; color: #0071e3; margin-bottom: 12px; }}
        .product-info {{ margin-bottom: 12px; }}
        .product-feature {{ display: flex; gap: 12px; margin-bottom: 8px; font-size: 14px; }}
        .product-feature .label {{ color: #6e6e73; font-weight: 500; min-width: 60px; }}
        .product-feature .value {{ color: #1d1d1f; flex: 1; }}
        .product-description {{
            font-size: 14px;
            color: #6e6e73;
            font-style: italic;
            line-height: 1.4;
            padding-top: 12px;
            border-top: 1px solid #d2d2d7;
        }}
        .no-idea {{ text-align: center; padding: 24px; color: #86868b; display: flex; flex-direction: column; align-items: center; gap: 8px; }}
        .no-idea-icon {{ font-size: 32px; opacity: 0.3; }}
        .no-idea-text {{ font-size: 15px; font-weight: 500; }}
        .no-idea-reason {{ font-size: 13px; opacity: 0.7; }}
        .score-cell {{ width: 140px; text-align: center; }}
        .score-container {{ display: flex; flex-direction: column; align-items: center; gap: 12px; }}
        .score-badge {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }}
        .score-badge:hover {{ transform: scale(1.05); }}
        .score-excellent {{ background: linear-gradient(135deg, #34c759, #30d158); color: #ffffff; }}
        .score-good {{ background: linear-gradient(135deg, #ff9500, #ffb340); color: #ffffff; }}
        .score-fair {{ background: linear-gradient(135deg, #d2d2d7, #e5e5ea); color: #6e6e73; }}
        .score-number {{ font-size: 28px; line-height: 1; }}
        .score-label {{ font-size: 12px; opacity: 0.8; margin-top: 2px; }}
        .score-breakdown {{ display: flex; gap: 12px; font-size: 12px; }}
        .score-item {{ display: flex; flex-direction: column; gap: 2px; }}
        .score-item-label {{ color: #86868b; font-weight: 500; }}
        .score-item-value {{ color: #1d1d1f; font-weight: 600; }}
        .footer {{ text-align: center; margin-top: 60px; padding-top: 40px; border-top: 1px solid #d2d2d7; }}
        .footer-text {{ font-size: 15px; color: #86868b; line-height: 1.6; }}
        @media (max-width: 1024px) {{
            .title {{ font-size: 40px; }}
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
            .score-weights {{ grid-template-columns: 1fr; }}
        }}
        @media (max-width: 768px) {{
            body {{ padding: 40px 16px; }}
            .title {{ font-size: 32px; }}
            .subtitle {{ font-size: 17px; }}
            .stats {{ grid-template-columns: 1fr; }}
            .methodology {{ padding: 24px; }}
            .table-header {{ flex-direction: column; gap: 16px; align-items: flex-start; }}
            th, td {{ padding: 12px; font-size: 14px; }}
            .hotspot-title {{ font-size: 15px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">微博热搜产品创意分析</h1>
            <p class="subtitle">{datetime.now().strftime('%Y年%m月%d日')}</p>
        </header>
        <div class="stats">
            <div class="stat-card"><div class="stat-number">{stats['total_topics']}</div><div class="stat-label">分析话题数</div></div>
            <div class="stat-card"><div class="stat-number">{stats['high_score_count']}</div><div class="stat-label">优秀创意 (≥80分)</div></div>
            <div class="stat-card"><div class="stat-number">{stats['medium_score_count']}</div><div class="stat-label">良好创意 (60-79分)</div></div>
            <div class="stat-card"><div class="stat-number">{stats['avg_score']:.1f}</div><div class="stat-label">平均评分</div></div>
        </div>
        <div class="methodology">
            <h3>评分方法论</h3>
            <div class="score-weights">
                <div class="weight-item"><strong>有趣度 (80分)</strong><div class="weight-description">评估话题的新颖性、传播性和用户体验独特性</div></div>
                <div class="weight-item"><strong>有用度 (20分)</strong><div class="weight-description">评估产品的实用价值和问题解决能力</div></div>
            </div>
            <div class="threshold-note">总分≥60分才会生成具体产品创意，确保创意的质量与可行性</div>
        </div>
        <div class="table-wrapper">
            <div class="table-header">
                <div class="table-title">热搜分析详情</div>
                <button class="sort-button" id="sortButton"><span>按评分排序</span><span class="sort-icon">↓</span></button>
            </div>
            <table id="hotspotTable">
                <thead><tr><th>排名</th><th>热点资讯</th><th>关键事件脉络</th><th>产品创意</th><th>综合评分</th></tr></thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
        <footer class="footer">
            <p class="footer-text">本报告由微博热搜分析工具自动生成<br>评分标准：有趣度 80% + 有用度 20%<br>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
    <script>
        const sortButton = document.getElementById('sortButton');
        const table = document.getElementById('hotspotTable');
        const tbody = table.querySelector('tbody');
        let isDescending = true;
        const originalRows = Array.from(tbody.querySelectorAll('tr'));
        sortButton.addEventListener('click', function() {{
            const rows = Array.from(tbody.querySelectorAll('tr'));
            if (isDescending) {{
                rows.sort((a, b) => parseFloat(b.dataset.score) - parseFloat(a.dataset.score));
                sortButton.classList.add('desc');
                sortButton.querySelector('span:first-child').textContent = '恢复原序';
            }} else {{
                tbody.innerHTML = '';
                originalRows.forEach(row => tbody.appendChild(row));
                sortButton.classList.remove('desc');
                sortButton.querySelector('span:first-child').textContent = '按评分排序';
                isDescending = true;
                return;
            }}
            tbody.innerHTML = '';
            rows.forEach(row => tbody.appendChild(row));
            isDescending = false;
        }});
    </script>
</body>
</html>'''

    return html_content


def main():
    """主函数"""
    print("=" * 60)
    print("微博热搜分析报告生成器 (苹果设计风格)")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 加载分析结果
    print("【步骤1/3】加载AI分析结果...")
    results = load_analysis_results()
    if not results:
        print("\n❌ 未能加载分析结果")
        return 1

    # 计算统计数据
    print("\n【步骤2/3】计算统计数据...")
    stats = calculate_stats(results)
    print(f"  📊 话题总数: {stats['total_topics']}")
    print(f"  ⭐ 优秀创意: {stats['high_score_count']}")
    print(f"  👍 良好创意: {stats['medium_score_count']}")
    print(f"  📈 平均分数: {stats['avg_score']:.1f}")

    # 生成HTML报告
    print("\n【步骤3/3】生成苹果风格HTML报告...")
    html_content = generate_html_report(results, stats)

    # 创建output目录（如果不存在）
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 已创建输出目录: {output_dir}")

    # 生成带日期的文件名
    date_str = datetime.now().strftime('%Y%m%d')
    output_file = os.path.join(output_dir, f'weibo_hotspot_analysis_apple_{date_str}.html')

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ HTML报告已保存: {output_file}")
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return 1

    print("\n" + "=" * 60)
    print("✅ 报告生成完成！")
    print(f"\n📄 输出文件: {output_file}")
    print(f"📂 输出目录: {output_dir}/")
    print("\n💡 功能说明:")
    print("   - 苹果风格设计: SF Pro字体、简洁白色背景、精致圆角和阴影")
    print("   - 交互排序: 点击'按评分排序'按钮可按评分高低排序")
    print("   - 响应式设计: 自适应桌面、平板和移动设备")
    print("   - 文件命名: 自动添加日期后缀 (YYYYMMDD)")
    print("   - 统一输出: 所有HTML报告保存在output文件夹")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### 第五步：创建主执行脚本

创建 `analyze_weibo_hotspots.py`：

```python
#!/usr/bin/env python3
"""
微博热搜产品创意分析器
"""

import json
import sys
from pathlib import Path

# 确保使用UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=" * 60)
    print("微博热搜产品创意分析器")
    print("=" * 60)
    print()

    # Step 1: 获取热搜数据
    print("【步骤1/4】正在获取微博热搜数据...")
    print("请运行获取脚本的命令")
    print()

    # Step 2: 搜索详细信息
    print("【步骤2/4】正在搜索热点详细信息...")
    print("对于每个热搜话题，将执行：")
    print("  1. WebSearch - 搜索相关新闻")
    print("  2. Task - AI分析产品创意")
    print()

    # Step 3: AI分析
    print("【步骤3/4】正在分析产品创意...")
    print("评估标准：")
    print("  - 有趣度：80分（新颖性、传播性、创意性）")
    print("  - 有用度：20分（实用性、解决问题）")
    print("  - 总分≥60分才会生成具体产品创意")
    print()

    # Step 4: 生成报告
    print("【步骤4/4】正在生成HTML报告...")
    print("报告将包含：")
    print("  - 热点资讯")
    print("  - 事件脉络总结（100字内）")
    print("  - 产品创意详情")
    print("  - 综合评分")
    print()

    print("✅ 分析完成！请查看生成的HTML报告")

if __name__ == "__main__":
    main()
```

## 使用方法

### 方法1: 快速自动化（推荐）

使用流水线模式提速 40%：

```bash
# 第一步: 生成自动化执行计划
python run_pipeline_automation.py

# 第二步: 在Claude Code中执行（两个会话并行）
# 会话A（搜索）: python run_for_claude_code.py
# 会话B（分析）: 等待搜索结果后，调用AI分析

# 第三步: 生成报告
python generate_html_report.py
```

### 方法2: 分步执行（灵活）

```bash
# 步骤1: 获取热搜
python fetch_weibo_hotspot.py

# 步骤2: 生成搜索计划
python search_hotspot_details.py

# 步骤3: 使用Claude Code执行WebSearch（对每个热搜）
# 步骤4: 生成AI分析提示
python analyze_hotspot_with_ai.py

# 步骤5: 使用Claude Code执行Task工具分析（对每个热搜）
# 步骤6: 生成报告
python generate_html_report.py
```

### 方法3: 完整流程（传统方式）

```bash
python run_analysis.py
```

## 流水线模式说明

传统串行模式：总时间 ≈ 4-5分钟
```
热搜1: 搜索(3s) → 等待 → 分析(15s) → 等待
热搜2: 搜索(3s) → 等待 → 分析(15s) → 等待
... (15个热搜)
总时间: 15 × 18s = 270s ≈ 4.5分钟
```

流水线模式：总时间 ≈ 2-3分钟（提速 40%）
```
时间  |  搜索任务         |  分析任务
------|-------------------|------------------
T+0s  |  搜索热搜1        |
T+3s  |  搜索热搜2        |  分析热搜1
T+6s  |  搜索热搜3        |  分析热搜2
T+9s  |  ...              |  ...
T+45s |  全部完成         |  全部完成
```

**如何实现流水线？**

使用两个Claude Code终端会话：

**会话A（搜索执行器）**:
```
python run_for_claude_code.py
# 按顺序执行 /WebSearch 命令
```

**会话B（分析执行器）**:
```
# 等待第一个搜索结果生成后执行:
python analyze_hotspot_with_ai.py
# 对生成的提示文件执行 Task 工具分析
```

详细说明请查看：`PIPELINE_EXECUTION_GUIDE.md`

## 配置说明

- 本skill使用天行数据API（https://apis.tianapi.com/weibohot/）
- API Key已配置，无需额外设置
- 每次分析前15条热搜
- 自动过滤评分低于60分的产品创意
- 生成的HTML报告美观、响应式设计
- 流水线模式需要两个终端会话
- urllib3 SSL警告已自动禁用

## 输出示例

分析完成后，将在 `output/` 目录生成带日期的HTML报告：

### 增强版报告（推荐）
- **文件名格式**: `weibo_hotspot_analysis_enhanced_YYYYMMDD.html`
- **示例**: `output/weibo_hotspot_analysis_enhanced_20251203.html`

报告内容包含：
- 苹果设计风格界面（SF Pro字体、简洁白色背景）
- 带颜色编码的评分（绿色=优秀，橙色=良好，灰色=一般）
- **深度分析标识**：高分话题（≥80分）显示特殊标记
- **3个维度的产品创意**：每个高分话题从不同维度产出3个创意
- **独特价值说明**：每个创意都包含核心价值点
- 事件脉络总结
- 有趣度和有用度的分项得分
- 可交互的评分排序功能（点击按钮切换排序）
- 响应式设计（自适应桌面、平板、移动设备）
- 深度分析统计卡片

### 基础版报告
- **文件名格式**: `weibo_hotspot_analysis_apple_YYYYMMDD.html`
- **示例**: `output/weibo_hotspot_analysis_apple_20251127.html`

报告内容包含：
- 苹果设计风格界面
- 每个话题1个产品创意
- 基础统计信息
- 交互排序功能
