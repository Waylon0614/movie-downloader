#!/usr/bin/env python3
"""
Movie Downloader - 全自动电影下载工具
使用 Playwright 自动化浏览器抓取资源，aria2 下载电影

作者: Waylon
版本: 1.0.0

制作花絮: 此 skill 由 Waylon 和 OpenClaw 协作完成，
         经过多次迭代优化，希望大家用的开心！
"""

import asyncio
import sys
import os
import re
import subprocess
import json
from pathlib import Path

# 配置文件路径
CONFIG_FILE = Path.home() / ".config/movie-downloader/config.json"

# 默认配置
DEFAULT_CONFIG = {
    "download_dir": str(Path.home() / "Desktop"),
    "default_mode": "manual",  # manual 或 quick
    "first_run": True
}

# 颜色
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_color(color, text):
    print(f"{color}{text}{Colors.END}")

def print_banner():
    """打印欢迎横幅"""
    print_color(Colors.CYAN, "=" * 60)
    print_color(Colors.CYAN, "🎬 Movie Downloader - 全自动电影下载工具")
    print_color(Colors.CYAN, "=" * 60)
    print()

def load_config():
    """加载配置文件"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """保存配置文件"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def setup_first_run():
    """首次运行设置向导"""
    print_color(Colors.YELLOW, "🎉 欢迎使用 Movie Downloader！")
    print()
    print("这是您第一次使用，需要进行一些简单设置。")
    print()
    
    config = DEFAULT_CONFIG.copy()
    
    # 1. 选择下载目录
    print_color(Colors.BLUE, "📁 步骤 1/2: 选择下载目录")
    print()
    print("电影将下载到哪个文件夹？")
    print(f"  [1] 桌面 (默认) - {Path.home() / 'Desktop'}")
    print(f"  [2] 下载文件夹 - {Path.home() / 'Downloads'}")
    print(f"  [3] 自定义路径")
    print()
    
    while True:
        choice = input("请选择 [1-3]: ").strip()
        if choice == "1" or choice == "":
            config["download_dir"] = str(Path.home() / "Desktop")
            print_color(Colors.GREEN, f"✅ 已选择: 桌面")
            break
        elif choice == "2":
            config["download_dir"] = str(Path.home() / "Downloads")
            print_color(Colors.GREEN, f"✅ 已选择: 下载文件夹")
            break
        elif choice == "3":
            custom_path = input("请输入完整路径: ").strip()
            if custom_path:
                config["download_dir"] = custom_path
                print_color(Colors.GREEN, f"✅ 已选择: {custom_path}")
                break
            else:
                print_color(Colors.RED, "❌ 路径不能为空")
        else:
            print_color(Colors.RED, "❌ 无效的选择")
    
    print()
    
    # 2. 选择默认模式
    print_color(Colors.BLUE, "⚙️  步骤 2/2: 选择默认模式")
    print()
    print("您希望默认使用哪种模式？")
    print()
    print("  [1] 手动模式 (推荐)")
    print("      - 搜索后显示资源列表")
    print("      - 您手动选择要下载的资源")
    print("      - 可以比较清晰度、大小、做种数")
    print()
    print("  [2] 快速模式")
    print("      - 自动选择第1个资源")
    print("      - 无需等待，直接开始下载")
    print("      - 适合信任搜索结果排序的情况")
    print()
    
    while True:
        choice = input("请选择 [1-2]: ").strip()
        if choice == "1" or choice == "":
            config["default_mode"] = "manual"
            print_color(Colors.GREEN, "✅ 已选择: 手动模式")
            break
        elif choice == "2":
            config["default_mode"] = "quick"
            print_color(Colors.GREEN, "✅ 已选择: 快速模式")
            break
        else:
            print_color(Colors.RED, "❌ 无效的选择")
    
    print()
    
    # 保存配置
    config["first_run"] = False
    save_config(config)
    
    print_color(Colors.GREEN, "✅ 设置完成！")
    print()
    print("您随时可以重新运行设置:")
    print("  movie-download --setup")
    print()
    print("-" * 60)
    print()
    
    return config

def check_dependencies():
    """检查并安装必要的依赖"""
    print_color(Colors.BLUE, "🔧 检查依赖...")
    print()
    
    deps_ok = True
    install_cmds = []
    
    # 1. 检查 aria2
    print("  [1/2] 检查 aria2...")
    if subprocess.run(["which", "aria2c"], capture_output=True).returncode != 0:
        print_color(Colors.RED, "      ❌ aria2 未安装")
        print()
        print("      安装命令:")
        print("        macOS: brew install aria2")
        print("        Linux: sudo apt-get install aria2")
        print("        Windows: 从 https://aria2.github.io/ 下载")
        print()
        install_cmds.append("brew install aria2")
        deps_ok = False
    else:
        print_color(Colors.GREEN, "      ✅ aria2 已安装")
    
    # 2. 检查 playwright
    print("  [2/2] 检查 Playwright...")
    try:
        import playwright
        print_color(Colors.GREEN, "      ✅ Playwright 已安装")
        
        # 检查 chromium (支持 Linux 和 macOS 路径)
        cache_dirs = [
            Path.home() / ".cache/ms-playwright",  # Linux
            Path.home() / "Library/Caches/ms-playwright"  # macOS
        ]
        chromium_found = any(
            list(cache_dir.glob("chromium-*"))
            for cache_dir in cache_dirs
            if cache_dir.exists()
        )
        if not chromium_found:
            print_color(Colors.YELLOW, "      ⚠️  Chromium 浏览器未安装")
            print()
            print("      安装命令:")
            print("        python3 -m playwright install chromium")
            print()
            install_cmds.append("python3 -m playwright install chromium")
            deps_ok = False
        else:
            print_color(Colors.GREEN, "      ✅ Chromium 已安装")
    except ImportError:
        print_color(Colors.RED, "      ❌ Playwright 未安装")
        print()
        print("      安装命令:")
        print("        pip3 install playwright")
        print("        python3 -m playwright install chromium")
        print()
        install_cmds.append("pip3 install playwright")
        install_cmds.append("python3 -m playwright install chromium")
        deps_ok = False
    
    print()
    
    if not deps_ok:
        print_color(Colors.RED, "❌ 依赖检查失败")
        print()
        print("请运行以下命令安装依赖:")
        print()
        for cmd in install_cmds:
            print(f"  {cmd}")
        print()
        return False
    
    print_color(Colors.GREEN, "✅ 所有依赖已就绪")
    print()
    return True

# 搜索电影
async def search_movie(query: str):
    """在 therarbg.com 搜索电影 - 修复版：使用首页搜索框"""
    from playwright.async_api import async_playwright
    
    print_color(Colors.YELLOW, f"🎬 正在搜索: {query}")
    print_color(Colors.BLUE, f"🔗 打开: https://therarbg.com/")
    print()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # 步骤1: 打开首页
            await page.goto("https://therarbg.com/", wait_until="networkidle", timeout=30000)
            
            # 步骤2: 在搜索框输入查询
            # 等待搜索框加载
            await page.wait_for_selector('input[type="text"]', timeout=10000)
            
            # 找到搜索框并输入
            search_input = await page.query_selector('input[type="text"]')
            if search_input:
                await search_input.fill(query)
                print_color(Colors.BLUE, f"⌨️  输入搜索词: {query}")
            else:
                raise Exception("找不到搜索框")
            
            # 步骤3: 点击搜索按钮
            search_button = await page.query_selector('button:has-text("")') or \
                          await page.query_selector('button[type="submit"]') or \
                          await page.query_selector('button i.fa-search') or \
                          await page.query_selector('button:has(i)')
            
            if search_button:
                await search_button.click()
                print_color(Colors.BLUE, "🔍 点击搜索按钮")
            else:
                # 如果找不到按钮，尝试按回车
                await search_input.press("Enter")
                print_color(Colors.BLUE, "⌨️  按回车搜索")
            
            # 等待搜索结果页面加载
            await page.wait_for_load_state("networkidle", timeout=30000)
            
            # 步骤4: 等待搜索结果表格加载
            await page.wait_for_selector("table", timeout=10000)
            
            # 给页面一点时间渲染结果
            await asyncio.sleep(2)
            
            # 解析搜索结果
            results = []
            rows = await page.query_selector_all("table tr")
            
            for row in rows[2:]:  # 跳过表头
                try:
                    cells = await row.query_selector_all("td")
                    if len(cells) >= 6:
                        # 提取信息
                        name_cell = cells[1]
                        name_link = await name_cell.query_selector("a")
                        if name_link:
                            name = await name_link.inner_text()
                            detail_url = await name_link.get_attribute("href")
                            
                            size = await cells[4].inner_text()
                            seeders = await cells[5].inner_text()
                            
                            # 提取清晰度
                            quality = "Unknown"
                            if "1080p" in name:
                                quality = "1080p"
                            elif "2160p" in name or "4K" in name:
                                quality = "4K"
                            elif "720p" in name:
                                quality = "720p"
                            
                            results.append({
                                "name": name.strip(),
                                "detail_url": "https://therarbg.com" + detail_url if detail_url.startswith("/") else detail_url,
                                "size": size.strip(),
                                "seeders": seeders.strip(),
                                "quality": quality
                            })
                except Exception as e:
                    continue
            
            await browser.close()
            
            # 验证结果是否包含搜索词
            if results and query.split()[0] not in results[0]["name"]:
                print_color(Colors.YELLOW, "⚠️  警告: 搜索结果可能不正确，请检查")
            
            return results
            
        except Exception as e:
            print_color(Colors.RED, f"❌ 搜索失败: {e}")
            await browser.close()
            return []

# 获取磁力链接
async def get_magnet_link(detail_url: str):
    """从详情页获取磁力链接"""
    from playwright.async_api import async_playwright
    
    print_color(Colors.YELLOW, f"🔍 获取磁力链接...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(detail_url, wait_until="networkidle", timeout=30000)
            
            # 查找磁力链接
            magnet_link = None
            
            # 方法1: 查找 magnet: 开头的链接
            links = await page.query_selector_all("a[href^='magnet:']")
            if links:
                magnet_link = await links[0].get_attribute("href")
            
            # 方法2: 查找包含 magnet 的文本
            if not magnet_link:
                page_content = await page.content()
                magnet_match = re.search(r'magnet:\?xt=urn:btih:[a-zA-Z0-9]+[^"\'>\s]+', page_content)
                if magnet_match:
                    magnet_link = magnet_match.group(0)
            
            await browser.close()
            return magnet_link
            
        except Exception as e:
            print_color(Colors.RED, f"❌ 获取磁力链接失败: {e}")
            await browser.close()
            return None

# 下载电影
def download_movie(magnet_link: str, download_dir: str):
    """使用 aria2 下载电影"""
    print_color(Colors.YELLOW, "📥 开始下载...")
    print(f"下载目录: {download_dir}")
    print()
    
    # 创建下载目录
    Path(download_dir).mkdir(parents=True, exist_ok=True)
    
    # 构建 aria2c 命令
    cmd = [
        "aria2c",
        f"--dir={download_dir}",
        "--seed-time=0",
        "--bt-stop-timeout=600",
        "--max-concurrent-downloads=5",
        "--split=10",
        "--summary-interval=30",
        "--allow-overwrite=true",
        magnet_link
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("")
        print_color(Colors.GREEN, "✅ 下载完成!")
        print("")
        print("文件位置:")
        
        # 列出下载的文件
        download_path = Path(download_dir)
        files = list(download_path.glob("*.mkv")) + list(download_path.glob("*.mp4")) + list(download_path.glob("*.avi"))
        for f in files:
            size = f.stat().st_size / (1024**3)  # GB
            print(f"  {f.name} ({size:.2f} GB)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("")
        print_color(Colors.RED, f"❌ 下载失败 (错误码: {e.returncode})")
        return False

# 显示搜索结果
def display_results(results):
    """显示搜索结果表格"""
    if not results:
        print_color(Colors.RED, "❌ 未找到资源")
        return False
    
    print("")
    print_color(Colors.GREEN, f"✅ 找到 {len(results)} 个资源:\n")
    
    print(f"{'#':<4} {'清晰度':<8} {'大小':<10} {'做种':<6} {'名称'}")
    print("-" * 80)
    
    for i, r in enumerate(results[:10], 1):  # 只显示前10个
        name = r['name'][:40] + "..." if len(r['name']) > 40 else r['name']
        print(f"{i:<4} {r['quality']:<8} {r['size']:<10} {r['seeders']:<6} {name}")
    
    return True

# 主函数
async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="全自动电影下载工具")
    parser.add_argument("query", nargs="?", help="电影名 [年份]")
    parser.add_argument("--select", "-s", type=int, help="直接选择第N个资源（快速模式）")
    parser.add_argument("--magnet", "-m", help="直接下载指定磁力链接")
    parser.add_argument("--setup", action="store_true", help="重新运行设置向导")
    parser.add_argument("--dir", "-d", help="指定下载目录（覆盖配置）")
    
    args = parser.parse_args()
    
    # 打印横幅
    print_banner()
    
    # 加载配置
    config = load_config()
    
    # 重新设置
    if args.setup:
        config = setup_first_run()
        return
    
    # 首次运行
    if config.get("first_run", True):
        config = setup_first_run()
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 确定下载目录
    download_dir = args.dir if args.dir else config["download_dir"]
    
    # 如果提供了磁力链接，直接下载
    if args.magnet:
        download_movie(args.magnet, download_dir)
        return
    
    # 检查是否有查询词
    if not args.query:
        print_color(Colors.RED, "❌ 请提供电影名")
        print()
        print("用法:")
        print("  movie-download \"电影名 年份\"")
        print("  movie-download \"电影名 年份\" --select 5")
        print("  movie-download --magnet \"magnet:?xt=urn:btih:...\"")
        print()
        sys.exit(1)
    
    # 搜索电影
    print_color(Colors.BLUE, "🔍 步骤 1/3: 搜索电影资源...")
    results = await search_movie(args.query)
    
    if not display_results(results):
        sys.exit(1)
    
    # 选择资源
    if args.select:
        # 用户指定了选择（快速模式）
        if 1 <= args.select <= len(results):
            selected = results[args.select - 1]
            print("")
            print_color(Colors.BLUE, f"✅ 快速模式: 已选择第 {args.select} 个资源")
            print(f"   {selected['name'][:50]}...")
        else:
            print_color(Colors.RED, f"❌ 无效的选择: {args.select}，有效范围 1-{len(results)}")
            sys.exit(1)
    elif config["default_mode"] == "quick":
        # 配置为快速模式
        selected = results[0]
        print("")
        print_color(Colors.BLUE, f"✅ 快速模式: 自动选择第 1 个资源")
        print(f"   {selected['name'][:50]}...")
    else:
        # 手动模式：让用户选择
        print("")
        print("提示: 输入数字选择资源，或按 Ctrl+C 取消")
        print()
        while True:
            try:
                choice = input("请选择资源编号 [1-10]: ").strip()
                choice = int(choice)
                if 1 <= choice <= len(results[:10]):
                    selected = results[choice - 1]
                    print("")
                    print_color(Colors.BLUE, f"✅ 已选择第 {choice} 个资源")
                    break
                else:
                    print_color(Colors.RED, "❌ 无效的选择")
            except ValueError:
                print_color(Colors.RED, "❌ 请输入数字")
            except KeyboardInterrupt:
                print("")
                print_color(Colors.YELLOW, "⚠️  已取消")
                sys.exit(0)
    
    print("")
    print_color(Colors.BLUE, f"🔍 步骤 2/3: 获取磁力链接...")
    
    magnet_link = await get_magnet_link(selected['detail_url'])
    
    if not magnet_link:
        print_color(Colors.RED, "❌ 无法获取磁力链接")
        sys.exit(1)
    
    print_color(Colors.GREEN, f"✅ 获取磁力链接成功!")
    
    print("")
    print_color(Colors.BLUE, f"📥 步骤 3/3: 开始下载...")
    
    if download_movie(magnet_link, download_dir):
        print("")
        print_color(Colors.GREEN, f"🎉 全部完成! 电影已保存到 {download_dir}")
    else:
        print("")
        print_color(Colors.RED, "❌ 下载失败")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("")
        print_color(Colors.YELLOW, "⚠️  用户取消")
        sys.exit(0)
    except Exception as e:
        print("")
        print_color(Colors.RED, f"❌ 错误: {e}")
        sys.exit(1)
