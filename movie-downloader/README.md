# Movie Downloader

🎬 全自动电影下载工具 - 一键搜索、选择、下载电影！

## 功能特性

- ✅ **全自动搜索** - 自动抓取 BT 站点资源
- ✅ **智能解析** - 提取清晰度、大小、做种数
- ✅ **多选项展示** - 提供多个资源供选择
- ✅ **一键下载** - 使用 aria2 自动下载
- ✅ **首次设置向导** - 引导配置下载目录和模式

## 安装

### 1. 安装依赖

```bash
# macOS
brew install aria2
pip3 install playwright
python3 -m playwright install chromium

# Linux
sudo apt-get install aria2
pip3 install playwright
python3 -m playwright install chromium
```

### 2. 安装 Skill

```bash
# 通过 skillhub 安装
skillhub install movie-downloader

# 或手动安装
git clone https://github.com/yourusername/movie-downloader.git
cd movie-downloader
chmod +x movie-download.py
```

## 使用方法

### 基本用法

```bash
# 搜索并下载
python3 movie-download.py "电影名 年份"

# 示例
python3 movie-download.py "Iron Man 2008"
python3 movie-download.py "The Matrix 1999"
```

### 快速模式（跳过选择）

```bash
python3 movie-download.py "电影名 年份" --select 1
```

### 直接下载磁力链接

```bash
python3 movie-download.py --magnet "magnet:?xt=urn:btih:..."
```

## 工作流程

```
1. 搜索电影 → 2. 显示选项 → 3. 用户选择 → 4. 获取磁力链接 → 5. 下载
```

## 示例输出

```
🎬 Movie Downloader - 全自动电影下载工具

🔍 步骤 1/3: 搜索电影资源...
🎬 正在搜索: Iron Man 2008

✅ 找到 10 个资源:

#    清晰度   大小       做种   名称
────────────────────────────────────────────────
1    4K       22.7 GB    147    Iron Man 2008 UHD BluRay 2160p...
2    1080p    4.4 GB     74     Iron Man 2008 1080p BluRay...
3    1080p    10.3 GB    45     Iron Man 2008 BluRay 1080p...
4    1080p    7.0 GB     33     Iron Man 2008 IMAX 1080p...
5    720p     797 MB     14     Iron.Man.2008.720p.DSNP.WEBRip...
...

请选择资源编号 [1-10]: 5

✅ 已选择第 5 个资源
🔍 步骤 2/3: 获取磁力链接...
✅ 获取磁力链接成功!

📥 步骤 3/3: 开始下载...
[#cee0bc 797MiB/797MiB(100%) CN:9 SD:1 DL:14MiB]

✅ 下载完成!

文件位置:
  Iron.Man.2008.720p.DSNP.WEBRip.800MB.x264-GalaxyRG.mkv (797 MB)

🎉 全部完成! 电影已保存到 ~/Desktop/龙虾电影/
```

## 配置

配置文件位置: `~/.config/movie-downloader/config.json`

```json
{
  "download_dir": "/Users/xxx/Desktop/龙虾电影",
  "default_mode": "manual"
}
```

## 重新设置

```bash
python3 movie-download.py --setup
```

## 依赖

- Python 3.7+
- aria2
- Playwright
- Chromium

## 注意事项

1. **版权问题** - 请确保您有合法下载和观看的权利
2. **网络安全** - BT 下载可能暴露 IP，建议使用 VPN
3. **存储空间** - 高清电影通常 1-10GB，请确保有足够空间

## 作者

Waylon

> 💡 **制作花絮**: 此 skill 由 Waylon 通过 OpenClaw 全自动制作（和龙虾来回拉扯了好久），希望大家用的开心！

## 许可证

MIT License
