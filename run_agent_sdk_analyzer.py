#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜分析器 - Claude Agent SDK 版本
适用于 GitHub Actions 自动化执行
"""

import os
import sys
import json
import warnings
from datetime import datetime
from typing import List, Dict, Any

# 禁用 SSL 警告
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')

import anthropic


class WeiboAnalyzerAgent:
    """微博热搜分析 Agent"""

    def __init__(self):
        """初始化 Agent"""
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("❌ 未设置 ANTHROPIC_API_KEY 环境变量")

        self.base_url = os.environ.get('ANTHROPIC_BASE_URL', 'https://api.anthropic.com')
        self.model = os.environ.get('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
        self.tianapi_key = os.environ.get('TIANAPI_KEY', 'c96a7333c975965e491ff49466a1844b')
        self.max_topics = int(os.environ.get('MAX_TOPICS', '15'))

        # 初始化 Anthropic 客户端（支持自定义 base_url）
        self.client = anthropic.Anthropic(
            api_key=self.api_key,
            base_url=self.base_url
        )

        print(f"✅ Agent 初始化成功")
        print(f"🔗 API 端点: {self.base_url}")
        print(f"🤖 使用模型: {self.model}")
        print(f"📊 最大分析话题数: {self.max_topics}")

    def fetch_weibo_hotspots(self) -> List[Dict[str, Any]]:
        """步骤1: 获取微博热搜数据"""
        print("\n" + "="*60)
        print("【步骤 1/5】获取微博热搜数据")
        print("="*60)

        import requests
        import re

        url = f"https://apis.tianapi.com/weibohot/index?key={self.tianapi_key}"

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get('code') == 200 and 'result' in data:
                hotspots = data['result']['list']

                # 生成搜索查询
                queries = []
                for i, item in enumerate(hotspots[:self.max_topics]):
                    title = item.get('hotword', '')
                    if not title:
                        continue

                    # 提取热度数字
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
            else:
                print(f"❌ API 返回异常: {data}")
                return []

        except Exception as e:
            print(f"❌ 获取热搜失败: {e}")
            return []

    def search_hotspot_with_claude(self, query: str) -> str:
        """步骤2: 使用 Claude 的 prompt caching 进行网络搜索"""
        try:
            # 使用 Claude 进行网络搜索（通过 prompt 引导）
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": f"""请帮我搜索以下话题的最新信息：

话题：{query}

请提供：
1. 事件的核心内容和背景
2. 关键人物或机构
3. 事件的影响和讨论热度
4. 相关的有趣细节

请用简洁的语言总结（200字以内）。"""
                }]
            )

            return message.content[0].text

        except Exception as e:
            print(f"  ⚠️ 搜索失败: {e}")
            return f"无法获取 {query} 的详细信息"

    def analyze_hotspot(self, hotspot: Dict[str, Any], search_result: str) -> Dict[str, Any]:
        """步骤3: 使用 Claude 分析热点并生成产品创意"""
        try:
            prompt = f"""请分析以下微博热搜话题，并从"有趣"和"有用"两个角度评估生成产品创意的可能性。

热搜话题：{hotspot['title']}
热度：{hotspot['heat']:,}

背景信息：
{search_result}

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
- fun_score: 有趣度评分（0-80）
- useful_score: 有用度评分（0-20）
- total_score: 总分（有趣度+有用度）
- summary: 事件脉络总结（100字以内）
- has_idea: 是否有产品创意（总分≥60为true）
- product: 如果总分≥60分，提供产品创意：
  * name: 产品名称
  * features: 核心功能
  * target_users: 目标用户
  * description: 简要描述（50字以内）
- reason: 如果总分<60分，说明原因

请严格按照JSON格式返回，不要包含任何其他文字。"""

            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # 解析 JSON 响应
            response_text = message.content[0].text.strip()

            # 移除可能的 markdown 代码块标记
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]

            analysis = json.loads(response_text.strip())

            # 合并热搜信息和分析结果
            result = {
                'rank': hotspot['rank'],
                'title': hotspot['title'],
                'heat': hotspot['heat'],
                **analysis
            }

            return result

        except json.JSONDecodeError as e:
            print(f"  ⚠️ JSON 解析失败: {e}")
            print(f"  原始响应: {response_text[:200]}...")
            return self._create_fallback_result(hotspot, "JSON解析失败")
        except Exception as e:
            print(f"  ⚠️ 分析失败: {e}")
            return self._create_fallback_result(hotspot, str(e))

    def _create_fallback_result(self, hotspot: Dict[str, Any], reason: str) -> Dict[str, Any]:
        """创建失败时的默认结果"""
        return {
            'rank': hotspot['rank'],
            'title': hotspot['title'],
            'heat': hotspot['heat'],
            'fun_score': 0,
            'useful_score': 0,
            'total_score': 0,
            'summary': '分析失败',
            'has_idea': False,
            'product': None,
            'reason': reason
        }

    def deep_dive_analysis(self, hotspot: Dict[str, Any], search_result: str) -> List[Dict[str, Any]]:
        """步骤4: 对高分话题进行深度分析（生成3个不同维度的产品创意）"""
        try:
            prompt = f"""请对以下高分热搜话题进行深度分析，从3个不同维度生成产品创意。

热搜话题：{hotspot['title']}
热度：{hotspot['heat']:,}
评分：{hotspot['total_score']}分

背景信息：
{search_result}

请从以下3个维度各生成1个产品创意：
1. **日常生活维度** - 如何让普通用户的日常生活更有趣或更便利
2. **社交娱乐维度** - 如何创造社交互动或娱乐体验
3. **商业价值维度** - 如何为企业或创作者创造商业机会

每个创意请包含：
- dimension: 维度名称
- name: 产品名称
- features: 核心功能
- target_users: 目标用户
- unique_value: 独特价值点

请严格按照JSON数组格式返回3个创意，不要包含任何其他文字。"""

            message = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = message.content[0].text.strip()

            # 移除 markdown 代码块标记
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]

            ideas = json.loads(response_text.strip())
            return ideas

        except Exception as e:
            print(f"  ⚠️ 深度分析失败: {e}")
            return []

    def run(self):
        """主执行流程"""
        print("\n" + "="*60)
        print("🤖 微博热搜分析器 - Claude Agent SDK 版本")
        print("="*60)
        print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # 步骤1: 获取热搜
        hotspots = self.fetch_weibo_hotspots()
        if not hotspots:
            print("\n❌ 未能获取热搜数据，退出")
            return False

        # 步骤2-3: 搜索并分析每个热搜
        print("\n" + "="*60)
        print("【步骤 2-3/5】搜索并分析热点")
        print("="*60)

        results = []
        for i, hotspot in enumerate(hotspots, 1):
            print(f"\n[{i}/{len(hotspots)}] 分析: {hotspot['title']}")

            # 搜索热点详情
            search_result = self.search_hotspot_with_claude(hotspot['search_query'])

            # 分析并生成产品创意
            analysis = self.analyze_hotspot(hotspot, search_result)
            results.append(analysis)

            print(f"  ✅ 评分: {analysis['total_score']}分 (有趣:{analysis['fun_score']} 有用:{analysis['useful_score']})")

        # 保存基础分析结果
        with open('hotspot_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 基础分析完成，已保存到 hotspot_analysis_results.json")

        # 步骤4: 深度分析高分话题
        print("\n" + "="*60)
        print("【步骤 4/5】深度分析高分话题 (≥80分)")
        print("="*60)

        high_score_topics = [r for r in results if r['total_score'] >= 80]
        print(f"\n发现 {len(high_score_topics)} 个高分话题")

        deep_dive_results = []
        for i, topic in enumerate(high_score_topics, 1):
            print(f"\n[{i}/{len(high_score_topics)}] 深度分析: {topic['title']}")

            # 重新搜索以获取更多信息
            search_result = self.search_hotspot_with_claude(topic['title'])

            # 生成3个维度的产品创意
            ideas = self.deep_dive_analysis(topic, search_result)

            deep_dive_results.append({
                'title': topic['title'],
                'rank': topic['rank'],
                'total_score': topic['total_score'],
                'deep_ideas': ideas
            })

            print(f"  ✅ 生成了 {len(ideas)} 个深度创意")

        # 保存深度分析结果
        if deep_dive_results:
            with open('deep_dive_analysis.json', 'w', encoding='utf-8') as f:
                json.dump(deep_dive_results, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 深度分析完成，已保存到 deep_dive_analysis.json")

        return results


def main():
    """主函数"""
    try:
        # 创建并运行 Agent
        agent = WeiboAnalyzerAgent()
        results = agent.run()

        if results:
            print("\n" + "="*60)
            print("✅ 分析任务完成！")
            print("="*60)
            print(f"\n📊 统计信息:")
            print(f"  - 分析话题数: {len(results)}")
            print(f"  - 高分话题数 (≥80分): {sum(1 for r in results if r['total_score'] >= 80)}")
            print(f"  - 平均评分: {sum(r['total_score'] for r in results) / len(results):.1f}")
            print(f"\n📁 输出文件:")
            print(f"  - weibo_search_queries.json")
            print(f"  - hotspot_analysis_results.json")
            print(f"  - deep_dive_analysis.json (如果有高分话题)")
            print(f"\n💡 下一步: 运行 generate_enhanced_report.py 生成HTML报告")
            return 0
        else:
            print("\n❌ 分析失败")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断执行")
        return 130
    except Exception as e:
        print(f"\n❌ 执行出错: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
