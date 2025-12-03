#!/bin/bash
# 微博热搜分析工具 - 安装脚本
# 适用于新电脑的快速设置

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  微博热搜分析工具 - 环境设置"
echo "=========================================="
echo ""

# 检查Python版本
echo "【步骤1/4】检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python 3"
    echo "请先安装Python 3.8或更高版本"
    echo "下载地址: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python版本: $PYTHON_VERSION"

# 检查pip
echo ""
echo "【步骤2/4】检查pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到pip3"
    echo "请先安装pip"
    exit 1
fi
echo "✅ pip3 已安装"

# 安装依赖
echo ""
echo "【步骤3/4】安装Python依赖..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo "✅ 依赖安装完成"
else
    echo "⚠️  未找到requirements.txt，手动安装requests..."
    pip3 install requests
    echo "✅ requests 安装完成"
fi

# 验证安装
echo ""
echo "【步骤4/4】验证安装..."

# 测试requests
if python3 -c "import requests" 2>/dev/null; then
    echo "✅ requests库正常"
else
    echo "❌ requests库导入失败"
    exit 1
fi

# 检查Claude Code
echo ""
echo "检查Claude Code..."
if command -v claude &> /dev/null; then
    CLAUDE_VERSION=$(claude --version 2>&1 || echo "未知版本")
    echo "✅ Claude Code已安装: $CLAUDE_VERSION"
else
    echo "⚠️  未检测到Claude Code"
    echo "这是一个Claude Code Skill，需要安装Claude Code才能使用"
    echo "安装方法: https://github.com/anthropics/claude-code"
fi

# 创建output目录
if [ ! -d "output" ]; then
    mkdir -p output
    echo "✅ 已创建output目录"
fi

# 测试网络连接
echo ""
echo "测试网络连接..."
if curl -s --head --request GET https://weibo.com | grep "200 OK" > /dev/null; then
    echo "✅ 可以访问微博API"
else
    echo "⚠️  无法访问微博（可能需要代理）"
fi

# 完成
echo ""
echo "=========================================="
echo "  ✅ 环境设置完成！"
echo "=========================================="
echo ""
echo "📚 使用方法："
echo ""
echo "  方式1: 使用Claude Code Skill"
echo "    $ claude"
echo "    > /weibo_hotspot_analyzer"
echo ""
echo "  方式2: 直接运行Python脚本"
echo "    $ python3 run_analysis.py"
echo ""
echo "  方式3: 流水线模式（更快）"
echo "    $ python3 run_pipeline_automation.py"
echo ""
echo "📖 详细说明请查看 README.md"
echo ""
