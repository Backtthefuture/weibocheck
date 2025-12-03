#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成微博热搜分析HTML报告 - 增强版（支持深度产品创意）
"""

import json
import os
import sys
from datetime import datetime


def load_analysis_results():
    """加载增强版分析结果"""
    analysis_file = 'enhanced_analysis_results.json'
    if os.path.exists(analysis_file):
        try:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
            print(f"✅ 成功加载增强版分析文件: {analysis_file} ({len(results)} 条结果)")
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
    deep_dive_count = sum(1 for r in results if r.get('is_deep_dive', False))

    return {
        'total_topics': total_topics,
        'high_score_count': high_score_count,
        'medium_score_count': medium_score_count,
        'avg_score': avg_score,
        'deep_dive_count': deep_dive_count
    }


def generate_product_html(result):
    """生成产品创意HTML"""
    if result.get('is_deep_dive', False) and 'product_ideas' in result:
        # 深度分析：展示3个产品创意
        ideas_html = '<div class="deep-dive-ideas">'
        ideas_html += '<div class="deep-dive-badge">🔥 深度分析</div>'

        for i, idea in enumerate(result['product_ideas'], 1):
            ideas_html += f'''
                <div class="product-idea enhanced">
                    <div class="idea-header">
                        <span class="idea-number">创意 {i}</span>
                        <span class="idea-dimension">{idea['dimension']}</span>
                    </div>
                    <div class="product-name">{idea['name']}</div>
                    <div class="product-info">
                        <div class="product-feature">
                            <span class="label">核心功能</span>
                            <span class="value">{idea['features']}</span>
                        </div>
                        <div class="product-feature">
                            <span class="label">目标用户</span>
                            <span class="value">{idea['target_users']}</span>
                        </div>
                    </div>
                    <div class="product-description">{idea['description']}</div>
                    <div class="unique-value">
                        <strong>💎 独特价值：</strong>{idea['unique_value']}
                    </div>
                </div>
            '''

        ideas_html += '</div>'
        return ideas_html
    elif result['has_idea'] and result.get('product'):
        # 普通分析：展示1个产品创意
        product = result['product']
        return f'''
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
        # 无创意
        reason = result.get('reason', '总分未达60分阈值')
        return f'<div class="no-idea"><span class="no-idea-icon">—</span><span class="no-idea-text">暂无可行产品创意</span><span class="no-idea-reason">{reason}</span></div>'


def generate_table_rows(results):
    """生成表格行"""
    rows = []

    for result in results:
        score_class = get_score_badge_class(result['total_score'])
        product_html = generate_product_html(result)

        # 为深度分析添加特殊标记
        deep_dive_class = 'deep-dive-row' if result.get('is_deep_dive', False) else ''

        row = f'''
            <tr data-score="{result['total_score']}" class="{deep_dive_class}">
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
    """生成增强版苹果风格HTML报告"""

    table_rows = generate_table_rows(results)

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜产品创意分析 - 增强版 - {datetime.now().strftime('%Y年%m月%d日')}</title>
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
        .container {{ max-width: 1600px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 60px; }}
        .title {{ font-size: 56px; font-weight: 700; letter-spacing: -0.005em; color: #1d1d1f; margin-bottom: 8px; line-height: 1.07143; }}
        .subtitle {{ font-size: 21px; font-weight: 400; color: #6e6e73; letter-spacing: 0.011em; line-height: 1.381; }}
        .badge {{ display: inline-block; background: linear-gradient(135deg, #ff6b6b, #ff8e53); color: white; padding: 4px 12px; border-radius: 12px; font-size: 14px; font-weight: 600; margin-left: 12px; }}

        /* Stats */
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 48px; }}
        .stat-card {{ background: #ffffff; border-radius: 18px; padding: 32px 28px; text-align: center; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
        .stat-card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12); }}
        .stat-number {{ font-size: 48px; font-weight: 700; color: #0071e3; line-height: 1.0; margin-bottom: 8px; }}
        .stat-label {{ font-size: 17px; color: #6e6e73; font-weight: 400; }}
        .stat-card.highlight {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .stat-card.highlight .stat-number {{ color: #ffffff; }}
        .stat-card.highlight .stat-label {{ color: #f0f0f0; }}

        /* Methodology */
        .methodology {{ background: #ffffff; border-radius: 18px; padding: 40px; margin-bottom: 32px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08); }}
        .methodology h3 {{ font-size: 28px; font-weight: 700; color: #1d1d1f; margin-bottom: 24px; letter-spacing: -0.003em; }}
        .score-weights {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }}
        .weight-item {{ background: #f5f5f7; padding: 24px; border-radius: 12px; }}
        .weight-item strong {{ display: block; font-size: 19px; font-weight: 600; color: #1d1d1f; margin-bottom: 8px; }}
        .weight-description {{ font-size: 15px; color: #6e6e73; line-height: 1.4; }}
        .threshold-note {{ margin-top: 24px; padding: 20px; background: #f5f5f7; border-radius: 12px; font-size: 15px; color: #6e6e73; line-height: 1.4; }}
        .deep-dive-note {{ margin-top: 16px; padding: 20px; background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); border-radius: 12px; font-size: 15px; color: #2d3436; line-height: 1.4; font-weight: 500; }}

        /* Table */
        .table-wrapper {{ background: #ffffff; border-radius: 18px; overflow: hidden; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08); }}
        .table-header {{ padding: 24px 32px; border-bottom: 1px solid #d2d2d7; display: flex; justify-content: space-between; align-items: center; }}
        .table-title {{ font-size: 24px; font-weight: 600; color: #1d1d1f; }}
        .sort-button {{ background: #0071e3; color: #ffffff; border: none; border-radius: 980px; padding: 8px 20px; font-size: 15px; font-weight: 500; cursor: pointer; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); display: flex; align-items: center; gap: 6px; }}
        .sort-button:hover {{ background: #0077ed; transform: scale(1.02); }}
        .sort-button:active {{ transform: scale(0.98); }}
        .sort-icon {{ display: inline-block; transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
        .sort-button.desc .sort-icon {{ transform: rotate(180deg); }}

        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #f5f5f7; padding: 16px 20px; text-align: left; font-size: 13px; font-weight: 600; color: #6e6e73; text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid #d2d2d7; }}
        td {{ padding: 24px 20px; border-bottom: 1px solid #d2d2d7; vertical-align: top; }}
        tr:last-child td {{ border-bottom: none; }}
        tr {{ transition: background-color 0.2s ease; }}
        tr:hover {{ background-color: #fbfbfd; }}
        tr.deep-dive-row {{ background: linear-gradient(to right, #fff5f5 0%, #ffffff 100%); }}
        tr.deep-dive-row:hover {{ background: linear-gradient(to right, #ffebeb 0%, #fbfbfd 100%); }}

        .rank-cell {{ width: 60px; text-align: center; }}
        .rank {{ font-size: 20px; font-weight: 700; color: #0071e3; }}
        .hotspot-cell {{ width: 18%; }}
        .hotspot-title {{ font-size: 17px; font-weight: 600; color: #1d1d1f; margin-bottom: 6px; line-height: 1.35; }}
        .heat-info {{ font-size: 13px; color: #ff3b30; font-weight: 500; }}
        .summary-cell {{ width: 22%; }}
        .event-summary {{ font-size: 15px; color: #6e6e73; line-height: 1.5; }}
        .product-cell {{ width: 35%; }}

        /* Deep Dive Ideas */
        .deep-dive-ideas {{ display: flex; flex-direction: column; gap: 16px; }}
        .deep-dive-badge {{ background: linear-gradient(135deg, #ff6b6b, #ff8e53); color: white; padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: 600; text-align: center; margin-bottom: 8px; display: inline-block; }}

        .product-idea {{ background: linear-gradient(135deg, #f5f5f7 0%, #ffffff 100%); border-radius: 12px; padding: 20px; border: 1px solid #d2d2d7; transition: all 0.3s ease; }}
        .product-idea.enhanced {{ border: 2px solid #ff8e53; background: linear-gradient(135deg, #fff9f5 0%, #ffffff 100%); }}
        .product-idea.enhanced:hover {{ transform: translateY(-2px); box-shadow: 0 8px 16px rgba(255, 107, 107, 0.15); }}

        .idea-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
        .idea-number {{ background: #0071e3; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
        .idea-dimension {{ color: #ff6b6b; font-size: 13px; font-weight: 600; }}

        .product-name {{ font-size: 17px; font-weight: 600; color: #0071e3; margin-bottom: 12px; }}
        .product-info {{ margin-bottom: 12px; }}
        .product-feature {{ display: flex; gap: 12px; margin-bottom: 8px; font-size: 14px; }}
        .product-feature .label {{ color: #6e6e73; font-weight: 500; min-width: 60px; }}
        .product-feature .value {{ color: #1d1d1f; flex: 1; }}
        .product-description {{ font-size: 14px; color: #6e6e73; line-height: 1.4; padding-top: 12px; border-top: 1px solid #d2d2d7; margin-bottom: 12px; }}
        .unique-value {{ background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); padding: 12px; border-radius: 8px; font-size: 13px; color: #2d3436; line-height: 1.4; }}
        .unique-value strong {{ display: block; margin-bottom: 4px; }}

        .no-idea {{ text-align: center; padding: 24px; color: #86868b; display: flex; flex-direction: column; align-items: center; gap: 8px; }}
        .no-idea-icon {{ font-size: 32px; opacity: 0.3; }}
        .no-idea-text {{ font-size: 15px; font-weight: 500; }}
        .no-idea-reason {{ font-size: 13px; opacity: 0.7; }}

        /* Score */
        .score-cell {{ width: 140px; text-align: center; }}
        .score-container {{ display: flex; flex-direction: column; align-items: center; gap: 12px; }}
        .score-badge {{ width: 80px; height: 80px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 700; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); transition: transform 0.2s ease; }}
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

        /* Footer */
        .footer {{ text-align: center; margin-top: 60px; padding-top: 40px; border-top: 1px solid #d2d2d7; }}
        .footer-text {{ font-size: 15px; color: #86868b; line-height: 1.6; }}

        /* Responsive */
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
            <h1 class="title">微博热搜产品创意分析<span class="badge">增强版</span></h1>
            <p class="subtitle">{datetime.now().strftime('%Y年%m月%d日')}</p>
        </header>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{stats['total_topics']}</div>
                <div class="stat-label">分析话题数</div>
            </div>
            <div class="stat-card highlight">
                <div class="stat-number">{stats['deep_dive_count']}</div>
                <div class="stat-label">深度分析话题</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['high_score_count']}</div>
                <div class="stat-label">优秀创意 (≥80分)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['medium_score_count']}</div>
                <div class="stat-label">良好创意 (60-79分)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['avg_score']:.1f}</div>
                <div class="stat-label">平均评分</div>
            </div>
        </div>

        <div class="methodology">
            <h3>评分方法论</h3>
            <div class="score-weights">
                <div class="weight-item">
                    <strong>有趣度 (80分)</strong>
                    <div class="weight-description">评估话题的新颖性、传播性和用户体验独特性</div>
                </div>
                <div class="weight-item">
                    <strong>有用度 (20分)</strong>
                    <div class="weight-description">评估产品的实用价值和问题解决能力</div>
                </div>
            </div>
            <div class="threshold-note">
                总分≥60分才会生成具体产品创意，确保创意的质量与可行性
            </div>
            <div class="deep-dive-note">
                🔥 深度分析：对于≥80分的高分话题，进行深度挖掘，从不同维度产出3个独特的产品创意
            </div>
        </div>

        <div class="table-wrapper">
            <div class="table-header">
                <div class="table-title">热搜分析详情</div>
                <button class="sort-button" id="sortButton">
                    <span>按评分排序</span>
                    <span class="sort-icon">↓</span>
                </button>
            </div>
            <table id="hotspotTable">
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>热点资讯</th>
                        <th>关键事件脉络</th>
                        <th>产品创意</th>
                        <th>综合评分</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>

        <footer class="footer">
            <p class="footer-text">
                本报告由微博热搜分析工具自动生成（增强版）<br>
                评分标准：有趣度 80% + 有用度 20%<br>
                高分话题（≥80分）进行深度分析，产出3个不同维度的产品创意<br>
                生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
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
    print("微博热搜分析报告生成器 - 增强版")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 加载分析结果
    print("【步骤1/3】加载增强版分析结果...")
    results = load_analysis_results()
    if not results:
        print("\n❌ 未能加载分析结果")
        return 1

    # 计算统计数据
    print("\n【步骤2/3】计算统计数据...")
    stats = calculate_stats(results)
    print(f"  📊 话题总数: {stats['total_topics']}")
    print(f"  🔥 深度分析: {stats['deep_dive_count']}")
    print(f"  ⭐ 优秀创意: {stats['high_score_count']}")
    print(f"  👍 良好创意: {stats['medium_score_count']}")
    print(f"  📈 平均分数: {stats['avg_score']:.1f}")

    # 生成HTML报告
    print("\n【步骤3/3】生成增强版苹果风格HTML报告...")
    html_content = generate_html_report(results, stats)

    # 创建output目录
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 已创建输出目录: {output_dir}")

    # 生成带日期的文件名
    date_str = datetime.now().strftime('%Y%m%d')
    output_file = os.path.join(output_dir, f'weibo_hotspot_analysis_enhanced_{date_str}.html')

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ HTML报告已保存: {output_file}")
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return 1

    print("\n" + "=" * 60)
    print("✅ 增强版报告生成完成！")
    print(f"\n📄 输出文件: {output_file}")
    print(f"📂 输出目录: {output_dir}/")
    print("\n💡 增强版特性:")
    print("   - 高分话题（≥80分）展示3个深度产品创意")
    print("   - 每个创意包含不同维度和独特价值")
    print("   - 深度分析话题有特殊标识和样式")
    print("   - 支持按评分排序和响应式设计")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
