# 🚚 项目迁移检查清单

使用本清单确保项目在新电脑上正确设置。

## 📦 迁移前准备（旧电脑）

### 确认要复制的文件
- [ ] 所有 `.py` 文件（6个核心脚本）
- [ ] `.claude/` 目录（Skill配置）
- [ ] `requirements.txt`（依赖列表）
- [ ] `README.md`（说明文档）
- [ ] `QUICK_START.md`（快速入门）
- [ ] `setup.sh`（安装脚本）
- [ ] `.gitignore`（可选）
- [ ] `weibo_search_queries.json`（可选，运行时会重新生成）

### 打包方式
**选项A：使用压缩包**
```bash
cd ..
tar -czf weibo-analyzer.tar.gz 微博热搜分析/
# 或使用zip
zip -r weibo-analyzer.zip 微博热搜分析/
```

**选项B：使用Git**
```bash
cd 微博热搜分析
git add .
git commit -m "准备迁移"
git push  # 推送到远程仓库
```

**选项C：使用U盘/网盘**
直接复制整个文件夹到U盘或同步到网盘。

---

## 🖥️ 新电脑设置步骤

### 第一步：系统要求检查
- [ ] **操作系统**：macOS / Linux / Windows
- [ ] **Python 3.8+**：`python3 --version`
- [ ] **pip**：`pip3 --version`
- [ ] **网络连接**：可访问 weibo.com

### 第二步：安装Claude Code
- [ ] 访问 [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [ ] 按照官方文档安装Claude Code
- [ ] 验证安装：`claude --version`
- [ ] 配置Claude API密钥（如需要）

### 第三步：复制项目文件
- [ ] 将项目文件夹复制到新电脑
- [ ] 推荐位置：`~/Documents/微博热搜分析`
- [ ] 确认所有文件完整（特别是 `.claude/` 目录）

### 第四步：运行安装脚本
```bash
cd 微博热搜分析
./setup.sh
```

安装脚本会自动：
- [ ] 检查Python环境
- [ ] 安装Python依赖（requests）
- [ ] 验证Claude Code
- [ ] 创建输出目录
- [ ] 测试网络连接

### 第五步：手动验证（如果setup.sh失败）

**检查Python**
```bash
python3 --version
# 应显示 3.8.0 或更高
```

**安装依赖**
```bash
pip3 install -r requirements.txt
# 或手动安装
pip3 install requests
```

**验证requests库**
```bash
python3 -c "import requests; print('OK')"
# 应显示 OK
```

**检查文件权限**
```bash
ls -la
# 确认 .py 文件有读权限
# 确认 .sh 文件有执行权限
```

### 第六步：测试运行

**测试1：单个脚本**
```bash
python3 fetch_weibo_hotspot.py
```
- [ ] 成功获取热搜数据
- [ ] 生成 `weibo_search_queries.json`

**测试2：生成报告**
```bash
python3 generate_apple_style_report.py
```
- [ ] 在 `output/` 目录生成HTML报告

**测试3：完整流程**
```bash
python3 run_analysis.py
```
- [ ] 全部步骤执行成功
- [ ] 生成最终报告

**测试4：Claude Code Skill**
```bash
claude
# 在Claude Code中输入：
/weibo_hotspot_analyzer
```
- [ ] Skill被识别
- [ ] 可以正常执行

---

## 🔍 故障排查

### 问题：找不到Python模块
```
ModuleNotFoundError: No module named 'requests'
```
**解决：**
```bash
pip3 install requests
```

### 问题：权限被拒绝
```
Permission denied: ./setup.sh
```
**解决：**
```bash
chmod +x setup.sh
chmod +x use_weibo_analyzer.sh
```

### 问题：Claude Code未识别skill
```
Unknown command: /weibo_hotspot_analyzer
```
**解决：**
1. 确认在项目目录内运行 `claude`
2. 检查 `.claude/commands/` 目录是否存在
3. 重启Claude Code

### 问题：无法访问微博API
```
Connection timeout
```
**解决：**
1. 检查网络连接
2. 如在公司网络，配置代理
3. 确认防火墙未阻止访问

---

## ✅ 最终验证清单

运行前最后检查：
- [ ] Python 3.8+ 已安装
- [ ] Claude Code 已安装并可用
- [ ] requests 库已安装
- [ ] 项目文件完整（包括.claude目录）
- [ ] 可以访问网络（weibo.com）
- [ ] output 目录已创建
- [ ] 所有脚本有执行权限

---

## 📊 成功标志

如果以下都正常，说明迁移成功：
- ✅ `python3 fetch_weibo_hotspot.py` 成功获取热搜
- ✅ `python3 generate_apple_style_report.py` 生成HTML报告
- ✅ 在浏览器中打开报告显示正常
- ✅ Claude Code中 `/weibo_hotspot_analyzer` 可用

---

## 🎯 快速迁移命令（总结）

**旧电脑打包：**
```bash
tar -czf weibo-analyzer.tar.gz 微博热搜分析/
```

**新电脑设置：**
```bash
# 1. 解压
tar -xzf weibo-analyzer.tar.gz
cd 微博热搜分析

# 2. 运行安装脚本
./setup.sh

# 3. 测试运行
python3 fetch_weibo_hotspot.py

# 4. 完整运行
python3 run_analysis.py
```

**总耗时：** 约5-10分钟（取决于网络速度）

---

## 💡 迁移建议

1. **备份数据**：迁移前备份 `output/` 目录中的历史报告
2. **保留原项目**：在新电脑验证成功前不要删除旧电脑的文件
3. **网络环境**：首次运行建议在稳定网络环境下
4. **版本控制**：建议使用Git管理项目，便于多设备同步

---

## 📞 需要帮助？

- 📖 详细文档：`README.md`
- 🚀 快速入门：`QUICK_START.md`
- 🛠️ Skill说明：`.claude/commands/weibo_hotspot_analyzer.md`
