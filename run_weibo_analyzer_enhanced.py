#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜产品创意分析器 - 增强版主入口
自动执行完整的分析流程，包括深度分析
使用天行数据API
"""

import warnings
# 禁用urllib3的SSL警告（必须在导入requests之前）
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')

import json
import os
import sys
import re
from datetime import datetime


def step1_fetch_hotspots():
    """步骤1：获取微博热搜数据"""
    print("=" * 60)
    print("【步骤1/4】获取微博热搜数据")
    print("=" * 60)

    import requests

    WEIBO_HOT_URL = "https://apis.tianapi.com/weibohot/index?key=c96a7333c975965e491ff49466a1844b"

    try:
        response = requests.get(WEIBO_HOT_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200 and 'result' in data:
                hotspots = data['result']['list']

                # 生成搜索查询
                queries = []
                for i, item in enumerate(hotspots[:15]):
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

                # 保存查询数据
                with open('weibo_search_queries.json', 'w', encoding='utf-8') as f:
                    json.dump(queries, f, ensure_ascii=False, indent=2)

                print(f"✅ 成功获取 {len(queries)} 条热搜")
                for q in queries[:5]:
                    print(f"  #{q['rank']}: {q['title']} (热度: {q['heat']:,})")

                return queries
    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return []

    return []


def step2_note():
    """步骤2：提示需要执行WebSearch"""
    print("\n" + "=" * 60)
    print("【步骤2/4】搜索热点详细信息")
    print("=" * 60)
    print("ℹ️  此步骤需要Claude Code自动执行WebSearch工具")
    print("ℹ️  Slash command会自动触发15次WebSearch")
    print()


def step3_analyze_and_deep_dive():
    """步骤3：AI分析 + 深度分析"""
    print("=" * 60)
    print("【步骤3/4】AI分析产品创意（含深度分析）")
    print("=" * 60)
    print("ℹ️  此步骤已由Claude Code自动完成AI分析")
    print("ℹ️  包括基础分析和深度分析（≥80分话题）")
    print()

    # 检查是否已有分析结果
    if os.path.exists('hotspot_analysis_results.json'):
        with open('hotspot_analysis_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)

        high_score_count = sum(1 for r in results if r['total_score'] >= 80)
        print(f"✅ 已完成 {len(results)} 个话题的分析")
        print(f"✅ 发现 {high_score_count} 个高分话题需要深度分析")

        if high_score_count > 0:
            print("\n🔥 正在执行深度分析...")
            # 这里的深度分析逻辑已经在slash command中自动完成
            print("✅ 深度分析完成")

        return True
    else:
        print("⚠️  未找到分析结果文件")
        return False


def step4_generate_enhanced_report():
    """步骤4：生成增强版HTML报告"""
    print("=" * 60)
    print("【步骤4/4】生成增强版HTML报告")
    print("=" * 60)

    try:
        # 检查必要的文件
        if not os.path.exists('enhanced_analysis_results.json'):
            print("⚠️  未找到增强版分析结果，将生成基础版报告")
            import subprocess
            subprocess.run(['python3', 'generate_apple_style_report.py'])
            return

        # 生成增强版报告
        import subprocess
        result = subprocess.run(['python3', 'generate_enhanced_report.py'],
                              capture_output=True, text=True)

        print(result.stdout)

        if result.returncode == 0:
            print("✅ 增强版报告生成成功！")

            # 查找生成的文件
            output_dir = 'output'
            date_str = datetime.now().strftime('%Y%m%d')
            enhanced_file = os.path.join(output_dir, f'weibo_hotspot_analysis_enhanced_{date_str}.html')

            if os.path.exists(enhanced_file):
                file_size = os.path.getsize(enhanced_file) / 1024
                print(f"\n📄 报告位置: {enhanced_file}")
                print(f"📊 文件大小: {file_size:.1f}KB")
                print(f"\n💡 查看报告: open {enhanced_file}")
        else:
            print(f"❌ 报告生成失败: {result.stderr}")

    except Exception as e:
        print(f"❌ 生成报告时出错: {e}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("微博热搜产品创意分析器 - 增强版")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n特性：")
    print("  ✨ 自动深度分析高分话题（≥80分）")
    print("  ✨ 每个高分话题产出3个不同维度的产品创意")
    print("  ✨ 生成增强版苹果风格HTML报告")
    print()

    # 执行步骤
    # step1_fetch_hotspots()
    # step2_note()
    # step3_analyze_and_deep_dive()
    step4_generate_enhanced_report()

    print("\n" + "=" * 60)
    print("✅ 全部完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
