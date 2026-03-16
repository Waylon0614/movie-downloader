# Movie Downloader Skill

🎬 全自动电影下载工具 - 傻瓜式操作，任何 Agent 都能轻松使用！

## ⚠️ 搜索前必须执行：中文电影名翻译

**这是最重要的一步，必须在搜索前完成。**

BT 站点只能用英文搜索，中文搜索无结果是正常的，不是 SKILL 的问题。

**执行规则：**
1. 用户输入电影名后，**先翻译成英文官方译名，再搜索**
2. 翻译时使用电影的官方英文名，而不是中文直译
3. 带上年份以提高精确度
4. **必须询问用户确认下载位置和资源选择**（见下方"用户确认流程"）

**示例：**
- 用户说"复仇者联盟2" → 翻译为 "Avengers Age of Ultron 2015" → 用英文搜索
- 用户说"流浪地球" → 翻译为 "The Wandering Earth 2019" → 用英文搜索
- 用户说"The Matrix 1999" → 已是英文，直接搜索

**告知用户格式：**
> 正在搜索《复仇者联盟2》的英文名 Avengers Age of Ultron 2015...

**禁止行为：**
- ❌ 禁止用中文直接在 BT 站点搜索
- ❌ 禁止因搜索结果是英文就认为找不到用户要的电影
- ❌ 禁止在没有尝试英文搜索的情况下报告"未找到资源"
- ❌ **禁止自动选择下载位置，必须询问用户**
- ❌ **禁止自动选择资源，必须展示选项让用户选择**

---

## ⚠️ 用户确认流程（必须执行）

### 步骤 1：确认下载位置
**必须询问用户**，不得自动决定：
```
请选择下载位置：
- [1] 桌面的「龙虾电影」文件夹（默认）
- [2] 其他位置（请告诉我路径）
```

### 步骤 2：展示搜索结果并让用户选择
**必须展示所有找到的资源**，不得自动选择：
```
找到 X 个资源，请选择要下载的：

| 编号 | 清晰度 | 大小 | 做种者 | 来源 |
|------|--------|------|--------|------|
| 1 | 1080p BluRay | 4.5 GB | 30人 | 蓝光原盘 |
| 2 | 1080p WEB-DL | 3.0 GB | 168人 | MAX流媒体 |
| ... | ... | ... | ... | ... |

请回复资源编号：
```

### 步骤 3：确认后开始下载
用户确认后，才开始下载。

---

## 功能特性

- ✅ **首次设置向导** - 引导用户选择下载目录和默认模式
- ✅ **依赖自动检查** - 检查并提示安装所需工具
- ✅ **全自动搜索** - Playwright 自动抓取 BT 站点
- ✅ **智能解析** - 自动提取清晰度、大小、做种数
- ✅ **双模式支持** - 手动选择 或 快速自动下载
- ✅ **配置持久化** - 设置保存到配置文件，下次直接使用

---

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

---

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
🔗 打开: https://therarbg.com/search/?search=The+Matrix+1999

✅ 找到 10 个资源:

#    清晰度   大小       做种   名称
────────────────────────────────────────────────
1    1080p    2.1 GB     156    The Matrix 1999 1080p BluRay...
2    4K       15.2 GB    89     The Matrix 1999 2160p UHD...
...

请选择资源编号 [1-10]: 1

✅ 已选择第 1 个资源

🔍 步骤 2/3: 获取磁力链接...
✅ 获取磁力链接成功!

📥 步骤 3/3: 开始下载...
下载目录: /Users/xxx/Desktop

[#cd49df 48KiB/73KiB(65%) CN:15 SD:2 DL:0B]

✅ 下载完成!

文件位置:
  The.Matrix.1999.1080p.BluRay.x264.mkv (2.10 GB)

🎉 全部完成! 电影已保存到 /Users/xxx/Desktop
```

#### 示例 2: 快速模式（跳过选择）

```bash
python3 movie-download.py "Inception 2010" --select 1
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

---

## 工作流程

```
┌─────────────────────────────────────────────────────────┐
│  0. 中文电影名翻译（必须）                               │
│     └── 中文名 → 英文官方译名 + 年份                    │
├─────────────────────────────────────────────────────────┤
│  1. 询问用户下载位置（必须）                             │
│     └── 桌面的「龙虾电影」/自定义路径                   │
├─────────────────────────────────────────────────────────┤
│  2. 检查依赖                                            │
│     ├── aria2 已安装？                                  │
│     ├── playwright 已安装？                             │
│     └── chromium 已安装？                               │
├─────────────────────────────────────────────────────────┤
│  3. 搜索电影（用英文搜索）                               │
│     ├── Playwright 打开 therarbg.com                    │
│     ├── 输入英文电影名搜索                              │
│     └── 解析前10个结果                                  │
├─────────────────────────────────────────────────────────┤
│  4. 展示结果并让用户选择资源（必须）                     │
│     └── 展示表格，等待用户输入编号                      │
├─────────────────────────────────────────────────────────┤
│  5. 获取磁力链接                                        │
│     └── 解析 magnet:?xt=urn:btih:...                   │
├─────────────────────────────────────────────────────────┤
│  6. 下载                                                │
│     ├── aria2 下载磁力链接                              │
│     ├── 显示下载进度                                    │
│     └── 保存到指定目录                                  │
└─────────────────────────────────────────────────────────┘
```

---

## 配置文件

配置文件位置: `~/.config/movie-downloader/config.json`

```json
{
  "download_dir": "/Users/xxx/Desktop",
  "default_mode": "manual",
  "first_run": false
}
```

---

## 故障排除

### 问题 1: "aria2 未安装"
```bash
brew install aria2       # macOS
sudo apt-get install aria2  # Linux
```

### 问题 2: "Playwright 未安装"
```bash
pip3 install playwright
python3 -m playwright install chromium
```

### 问题 3: 搜索不到结果
- 确认已使用英文电影名搜索（不是中文）
- 检查网络连接或尝试使用 VPN
- 检查电影名拼写是否正确
- **therarbg.com 搜索问题**：直接访问搜索结果 URL 可能返回"最新上传"而非搜索结果，需要在搜索框手动输入并点击搜索按钮

### 问题 6: therarbg.com 搜索结果不正确
**现象**：搜索结果显示的是"Top 10 in ALL, by latest"而非搜索结果
**原因**：therarbg.com 的搜索页面需要交互操作才能获取正确结果
**解决**：
1. 打开首页 `https://therarbg.com/`
2. 在搜索框输入电影名（英文）
3. 点击搜索按钮（🔍）
4. 等待搜索结果页面加载

**注意**：直接访问 `https://therarbg.com/search/?search=xxx` 可能无法获取正确结果

### 问题 4: 下载速度慢
- 选择做种数（Seeders）多的资源
- 尝试使用 VPN

### 问题 5: "无法获取磁力链接"
```bash
pip3 install --upgrade playwright
python3 -m playwright install chromium
```

---

## 注意事项

1. **版权问题** - 请确保您有合法下载和观看的权利
2. **网络安全** - BT 下载可能暴露 IP，建议使用 VPN
3. **存储空间** - 高清电影通常 1-10GB，请确保有足够空间
4. **首次运行** - 会自动下载 Chromium（约 100MB）

---

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

## BT 站点配置

### 主站点
- **therarbg.com** - 当前使用的主站点（推荐）

### 备用镜像站
如果主站点无法访问，可以尝试以下备用站点：
- https://rargb.to/（原站点，可能不稳定）

---

## 作者

**Waylon**
创建时间: 2026-03-14

> 💡 **制作花絮**: 此 skill 由 Waylon 和 OpenClaw 协作完成，经过多次迭代优化，希望大家用的开心！

## 许可证

MIT License - 自由使用和修改
