# Movie Downloader

🎬 全自动电影下载工具 - 一键搜索、选择、下载电影！

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()

[English](./README_EN.md) | 简体中文

## ✨ 功能特性

- ✅ **全自动搜索** - Playwright 自动抓取 BT 站点资源
- ✅ **智能解析** - 自动提取清晰度、大小、做种数
- ✅ **多选项展示** - 提供多个资源供选择对比
- ✅ **一键下载** - 使用 aria2 自动下载，支持断点续传
- ✅ **首次设置向导** - 引导配置下载目录和模式
- ✅ **双模式支持** - 手动选择 或 快速自动下载

## 📦 安装

### 环境要求

- Python 3.7+
- aria2
- Playwright + Chromium

### 快速安装

**macOS:**
```bash
brew install aria2
pip3 install playwright
python3 -m playwright install chromium
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install aria2
pip3 install playwright
python3 -m playwright install chromium
```

**Windows:**
1. 从 https://aria2.github.io/ 下载 aria2
2. `pip3 install playwright`
3. `python3 -m playwright install chromium`

### 安装 Movie Downloader

```bash
git clone https://github.com/Waylon0614/movie-downloader.git
cd movie-downloader
chmod +x movie-download.py
```

## 🚀 使用方法

### 基本用法

```bash
# 搜索并下载（交互式选择）
python3 movie-download.py "电影名 年份"

# 示例
python3 movie-download.py "The Matrix 1999"
python3 movie-download.py "Inception 2010"
python3 movie-download.py "肖申克的救赎 1994"
```

### 快速模式（跳过选择，自动选第1个）

```bash
python3 movie-download.py "电影名 年份" --select 1
```

### 直接下载磁力链接

```bash
python3 movie-download.py --magnet "magnet:?xt=urn:btih:..."
```

### 指定下载目录

```bash
python3 movie-download.py "电影名 年份" --dir "/path/to/folder"
```

## 📋 工作流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 检查依赖（aria2, Playwright, Chromium）              │
├─────────────────────────────────────────────────────────┤
│  2. 首次运行设置（下载目录、默认模式）                    │
├─────────────────────────────────────────────────────────┤
│  3. 搜索电影资源（Playwright 自动抓取）                  │
├─────────────────────────────────────────────────────────┤
│  4. 显示资源列表（清晰度、大小、做种数）                  │
├─────────────────────────────────────────────────────────┤
│  5. 用户选择 / 自动选择                                  │
├─────────────────────────────────────────────────────────┤
│  6. 获取磁力链接                                         │
├─────────────────────────────────────────────────────────┤
│  7. aria2 下载（显示进度）                               │
└─────────────────────────────────────────────────────────┘
```

## 🖥️ 示例输出

```
🎬 Movie Downloader - 全自动电影下载工具
============================================================

🔍 步骤 1/3: 搜索电影资源...
🎬 正在搜索: The Matrix 1999

✅ 找到 10 个资源:

#    清晰度   大小       做种   名称
────────────────────────────────────────────────
1    4K       15.2 GB    89     The Matrix 1999 2160p UHD...
2    1080p    2.1 GB     156    The Matrix 1999 1080p BluRay...
3    1080p    4.4 GB     74     The Matrix 1999 1080p...
...

请选择资源编号 [1-10]: 2

✅ 已选择第 2 个资源
🔍 步骤 2/3: 获取磁力链接...
✅ 获取磁力链接成功!

📥 步骤 3/3: 开始下载...
[#cd49df 0B/0B CN:18 SD:0 DL:0B]
[#cd49df 48MiB/2.1GiB(2%) CN:15 SD:2 DL:5.2MiB]
...

✅ 下载完成!
文件位置: ~/Desktop/The.Matrix.1999.1080p.BluRay.x264.mkv (2.10 GB)

🎉 全部完成!
```

## ⚙️ 配置

配置文件位置：`~/.config/movie-downloader/config.json`

```json
{
  "download_dir": "/Users/xxx/Desktop/龙虾电影",
  "default_mode": "manual",
  "first_run": false
}
```

### 重新设置

```bash
python3 movie-download.py --setup
```

## 🔧 故障排除

### "aria2 未安装"
```bash
brew install aria2  # macOS
sudo apt-get install aria2  # Linux
```

### "Playwright 未安装"
```bash
pip3 install playwright
python3 -m playwright install chromium
```

### 搜索不到结果
- 检查网络连接
- 尝试使用英文电影名
- 确认 rargb.to 可访问（可能需要 VPN）

### 下载速度慢
- 选择做种数（Seeders）多的资源
- 检查网络连接
- 尝试使用 VPN

## 📝 注意事项

1. **版权问题** - 请确保您有合法下载和观看的权利
2. **网络安全** - BT 下载可能暴露 IP，建议使用 VPN
3. **存储空间** - 高清电影通常 1-10GB，请确保有足够空间
4. **首次运行** - 会自动下载 Chromium（约 100MB）


## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件

## 👤 作者

**Waylon**

> 💡 此工具由 Waylon 和 OpenClaw（巨愚蠢的kimi） 协作完成，经过多次迭代优化，气的我肝颤。

---

⭐ 如果这个项目对你有帮助，请给个 Star！
