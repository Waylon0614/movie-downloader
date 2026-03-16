# Movie Downloader Skill

🎬 全自动电影下载工具 - 傻瓜式操作，任何 Agent 都能轻松使用！

## 功能特性

- ✅ **首次设置向导** - 引导用户选择下载目录和默认模式
- ✅ **依赖自动检查** - 检查并提示安装所需工具
- ✅ **全自动搜索** - Playwright 自动抓取 BT 站点
- ✅ **智能解析** - 自动提取清晰度、大小、做种数
- ✅ **双模式支持** - 手动选择 或 快速自动下载
- ✅ **配置持久化** - 设置保存到配置文件，下次直接使用

## 依赖工具及安装方法

### 必需工具

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| **aria2** | BT 下载工具 | `brew install aria2` |
| **playwright** | 浏览器自动化 | `pip3 install playwright` |
| **chromium** | 无头浏览器 | `python3 -m playwright install chromium` |

### 安装步骤（按顺序执行）

#### 步骤 1: 安装 aria2

**macOS:**
```bash
brew install aria2
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install aria2
```

**Windows:**
1. 从 https://aria2.github.io/ 下载
2. 解压并将 aria2c.exe 添加到 PATH

#### 步骤 2: 安装 Playwright

```bash
pip3 install playwright
```

#### 步骤 3: 安装 Chromium 浏览器

```bash
python3 -m playwright install chromium
```

> **注意**: 这会下载约 100MB 的 Chromium 浏览器，只需执行一次

### 验证安装

```bash
# 检查 aria2
aria2c --version

# 检查 playwright
python3 -c "import playwright; print('OK')"

# 检查 chromium
ls ~/.cache/ms-playwright/
```

## 使用方法

### 基本用法

```bash
# 首次运行 - 会自动进入设置向导
python3 movie-download.py "电影名 年份"

# 示例
python3 movie-download.py "The Matrix 1999"
python3 movie-download.py "Inception 2010"
```

### 命令行参数

```bash
python3 movie-download.py [电影名] [选项]

选项:
  --select N, -s N     快速模式：直接选择第N个资源
  --magnet URL, -m URL 直接下载指定的磁力链接
  --dir PATH, -d PATH  指定下载目录（覆盖配置）
  --setup              重新运行设置向导
  -h, --help           显示帮助信息
```

### 使用示例

#### 示例 1: 首次使用（进入设置向导）

```bash
$ python3 movie-download.py "The Matrix 1999"

============================================================
🎬 Movie Downloader - 全自动电影下载工具
============================================================

🎉 欢迎使用 Movie Downloader！

这是您第一次使用，需要进行一些简单设置。

📁 步骤 1/2: 选择下载目录

电影将下载到哪个文件夹？
  [1] 桌面 (默认) - /Users/xxx/Desktop
  [2] 下载文件夹 - /Users/xxx/Downloads
  [3] 自定义路径

请选择 [1-3]: 1
✅ 已选择: 桌面

⚙️  步骤 2/2: 选择默认模式

您希望默认使用哪种模式？
  [1] 手动模式 (推荐)
      - 搜索后显示资源列表
      - 您手动选择要下载的资源
      - 可以比较清晰度、大小、做种数

  [2] 快速模式
      - 自动选择第1个资源
      - 无需等待，直接开始下载
      - 适合信任搜索结果排序的情况

请选择 [1-2]: 1
✅ 已选择: 手动模式

✅ 设置完成！

🔧 检查依赖...
  [1/2] 检查 aria2...
      ✅ aria2 已安装
  [2/2] 检查 Playwright...
      ✅ Playwright 已安装
      ✅ Chromium 已安装
✅ 所有依赖已就绪

🔍 步骤 1/3: 搜索电影资源...
🎬 正在搜索: The Matrix 1999
🔗 打开: https://rargb.to/search/?search=The+Matrix+1999

✅ 找到 10 个资源:

#    清晰度   大小       做种   名称
────────────────────────────────────────────────
1    1080p    2.1 GB     156    The Matrix 1999 1080p BluRay...
2    4K       15.2 GB    89     The Matrix 1999 2160p UHD...
...

提示: 输入数字选择资源，或按 Ctrl+C 取消

请选择资源编号 [1-10]: 1

✅ 已选择第 1 个资源

🔍 步骤 2/3: 获取磁力链接...
✅ 获取磁力链接成功!

📥 步骤 3/3: 开始下载...
下载目录: /Users/xxx/Desktop

[#cd49df 0B/0B CN:18 SD:0 DL:0B]
[#cd49df 48KiB/73KiB(65%) CN:15 SD:2 DL:0B]
...

✅ 下载完成!

文件位置:
  The.Matrix.1999.1080p.BluRay.x264.mkv (2.10 GB)

🎉 全部完成! 电影已保存到 /Users/xxx/Desktop
```

#### 示例 2: 快速模式（跳过选择）

```bash
# 使用 --select 直接选择第1个资源
python3 movie-download.py "Inception 2010" --select 1

# 或使用配置的快速模式
# (在设置向导中选择"快速模式"作为默认)
```

#### 示例 3: 直接下载磁力链接

```bash
python3 movie-download.py --magnet "magnet:?xt=urn:btih:..."
```

#### 示例 4: 指定下载目录

```bash
python3 movie-download.py "Movie Name 2024" --dir "/path/to/folder"
```

#### 示例 5: 重新设置

```bash
python3 movie-download.py --setup
```

## 工作流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 检查依赖                                            │
│     ├── aria2 已安装？                                  │
│     ├── playwright 已安装？                             │
│     └── chromium 已安装？                               │
│     如有缺失，提示安装命令                               │
├─────────────────────────────────────────────────────────┤
│  2. 首次运行设置（仅第一次）                             │
│     ├── 选择下载目录（桌面/下载/自定义）                 │
│     └── 选择默认模式（手动/快速）                        │
├─────────────────────────────────────────────────────────┤
│  3. 搜索电影                                            │
│     ├── Playwright 打开 rargb.to                        │
│     ├── 输入电影名搜索                                  │
│     └── 解析前10个结果                                  │
├─────────────────────────────────────────────────────────┤
│  4. 选择资源                                            │
│     ├── 手动模式: 显示列表，用户输入编号                │
│     └── 快速模式: 自动选择第1个                         │
├─────────────────────────────────────────────────────────┤
│  5. 获取磁力链接                                        │
│     ├── 打开资源详情页                                  │
│     └── 解析 magnet:?xt=urn:btih:...                   │
├─────────────────────────────────────────────────────────┤
│  6. 下载                                                │
│     ├── aria2 下载磁力链接                              │
│     ├── 显示下载进度                                    │
│     └── 保存到指定目录                                  │
└─────────────────────────────────────────────────────────┘
```

## 配置文件

配置文件位置: `~/.config/movie-downloader/config.json`

示例内容:
```json
{
  "download_dir": "/Users/xxx/Desktop",
  "default_mode": "manual",
  "first_run": false
}
```

## 故障排除

### 问题 1: "aria2 未安装"

**解决:**
```bash
brew install aria2  # macOS
sudo apt-get install aria2  # Linux
```

### 问题 2: "Playwright 未安装"

**解决:**
```bash
pip3 install playwright
python3 -m playwright install chromium
```

### 问题 3: 搜索不到结果

**可能原因:**
- 网络连接问题
- rargb.to 被屏蔽（尝试使用 VPN）
- 电影名拼写错误

**解决:**
- 检查网络: `ping rargb.to`
- 尝试英文电影名
- 使用 VPN

### 问题 4: 下载速度慢

**解决:**
- 选择做种数（Seeders）多的资源
- 检查网络连接
- 尝试使用 VPN

### 问题 5: "无法获取磁力链接"

**可能原因:**
- 网站结构改变
- 页面加载超时

**解决:**
- 更新 Playwright: `pip3 install --upgrade playwright`
- 重新安装 Chromium: `python3 -m playwright install chromium`

## 注意事项

1. **版权问题** - 请确保您有合法下载和观看的权利
2. **网络安全** - BT 下载可能暴露 IP，建议使用 VPN
3. **存储空间** - 高清电影通常 1-10GB，请确保有足够空间
4. **首次运行** - 会自动下载 Chromium（约 100MB）

## 技术栈

- **浏览器自动化**: Playwright + Chromium
- **下载工具**: aria2
- **编程语言**: Python 3
- **BT 协议**: BitTorrent (磁力链接)

## 文件结构

```
~/.openclaw/workspace/skills/movie-downloader/
├── SKILL.md              # 本文件（详细说明）
├── README.md             # 快速入门文档
├── movie-download.py     # 主程序（Python）
└── movie-download.sh     # 备用脚本（Bash）
```

## 作者

蒜蓉小龙虾（拌凉面版）
创建时间: 2026-03-14

> 💡 **制作花絮**: 此 skill 由 Waylon 通过 OpenClaw 全自动制作（和龙虾来回拉扯了好久），希望大家用的开心！

## 许可证

MIT License - 自由使用和修改
