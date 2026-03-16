#!/bin/bash
# Movie Downloader - 全自动电影下载工具
# 用法: movie-download "电影名 [年份]"

set -e

# 配置
DOWNLOAD_DIR="$HOME/Desktop/龙虾电影"
RARGB_SEARCH="https://rargb.to/search/?search="
BROWSER_PORT="18800"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 检查依赖
check_dependencies() {
    if ! command -v aria2c &> /dev/null; then
        echo -e "${RED}错误: aria2 未安装${NC}"
        echo "请运行: brew install aria2"
        exit 1
    fi
    
    if ! command -v browser &> /dev/null && ! command -v openclaw &> /dev/null; then
        echo -e "${RED}错误: 未找到 browser 工具${NC}"
        exit 1
    fi
}

# URL 编码
url_encode() {
    local string="$1"
    local encoded=""
    local pos c o
    
    for (( pos=0; pos<${#string}; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9]) encoded+="$c" ;;
            *) 
                printf -v o '%%%02x' "'$c"
                encoded+="$o"
                ;;
        esac
    done
    echo "$encoded"
}

# 搜索电影（使用 browser 自动化）
search_movie() {
    local query="$1"
    local encoded_query=$(url_encode "$query")
    local search_url="${RARGB_SEARCH}${encoded_query}"
    
    echo -e "${YELLOW}🎬 正在搜索: $query${NC}"
    echo "URL: $search_url"
    echo ""
    
    # 使用 browser 打开搜索页面并获取结果
    # 这里需要调用 OpenClaw 的 browser 工具
    echo -e "${BLUE}请稍候，正在抓取搜索结果...${NC}"
    
    # 实际使用时，这里应该调用 browser 命令
    # 由于 browser 是 OpenClaw 内部工具，这里输出提示
    echo ""
    echo -e "${YELLOW}由于 browser 工具需要在 OpenClaw 环境中运行，请使用以下命令:${NC}"
    echo ""
    echo "  browser open '$search_url'"
    echo "  browser snapshot --delayMs 5000"
    echo ""
    echo "然后解析结果，选择资源编号。"
}

# 获取磁力链接（从详情页）
get_magnet_from_detail() {
    local detail_url="$1"
    
    echo -e "${YELLOW}🔍 正在获取磁力链接...${NC}"
    echo "URL: $detail_url"
    echo ""
    
    # 实际使用时调用 browser
    echo -e "${YELLOW}请在 OpenClaw 中执行:${NC}"
    echo "  browser open '$detail_url'"
    echo "  browser snapshot --delayMs 3000"
    echo ""
    echo "然后查找 magnet:?xt=urn:btih:... 链接"
}

# 下载电影
download_movie() {
    local magnet_link="$1"
    
    echo -e "${YELLOW}📥 开始下载电影${NC}"
    echo "磁力链接: ${magnet_link:0:60}..."
    echo "下载目录: $DOWNLOAD_DIR"
    echo ""
    
    mkdir -p "$DOWNLOAD_DIR"
    
    if aria2c \
        --dir="$DOWNLOAD_DIR" \
        --seed-time=0 \
        --bt-stop-timeout=600 \
        --max-concurrent-downloads=5 \
        --split=10 \
        --summary-interval=30 \
        --allow-overwrite=true \
        "$magnet_link"; then
        
        echo ""
        echo -e "${GREEN}✅ 下载完成!${NC}"
        echo ""
        echo "文件位置:"
        ls -lh "$DOWNLOAD_DIR"/*.mkv "$DOWNLOAD_DIR"/*.mp4 2>/dev/null || ls -lh "$DOWNLOAD_DIR"
        return 0
    else
        echo ""
        echo -e "${RED}❌ 下载失败${NC}"
        return 1
    fi
}

# 使用说明
usage() {
    cat << EOF
${YELLOW}Movie Downloader - 全自动电影下载工具${NC}

用法:
  movie-download <命令> [参数]

命令:
  search <电影名> [年份]     搜索电影资源
  download <磁力链接>        直接下载电影
  auto <电影名> [年份]       全自动搜索并下载（推荐）

示例:
  movie-download search "神偷奶爸" 2010
  movie-download search "Despicable Me" 2010
  movie-download download "magnet:?xt=urn:btih:..."
  movie-download auto "神偷奶爸" 2010

注意:
  全自动模式需要 OpenClaw 环境支持 browser 工具
EOF
}

# 全自动模式（搜索+下载）
auto_download() {
    local query="$1"
    
    echo -e "${YELLOW}🤖 全自动模式启动${NC}"
    echo "搜索: $query"
    echo ""
    
    # 步骤 1: 搜索
    search_movie "$query"
    
    echo ""
    echo -e "${BLUE}────────────────────────────────────${NC}"
    echo -e "${YELLOW}请查看上面的搜索结果，然后:${NC}"
    echo ""
    echo "1. 记下你想下载的资源编号（如 #5）"
    echo "2. 复制该资源的详情页 URL"
    echo "3. 运行: movie-download magnet <详情页URL>"
    echo ""
}

# 从详情页获取并下载
get_and_download() {
    local detail_url="$1"
    
    get_magnet_from_detail "$detail_url"
    
    echo ""
    echo -e "${YELLOW}获取到磁力链接后，运行:${NC}"
    echo "  movie-download download \"磁力链接\""
}

# 主程序
main() {
    check_dependencies
    
    if [ $# -eq 0 ]; then
        usage
        exit 1
    fi
    
    case "$1" in
        search)
            shift
            if [ $# -eq 0 ]; then
                echo "错误: 请提供电影名"
                exit 1
            fi
            search_movie "$*"
            ;;
        download)
            shift
            if [ $# -eq 0 ]; then
                echo "错误: 请提供磁力链接"
                exit 1
            fi
            download_movie "$1"
            ;;
        auto)
            shift
            if [ $# -eq 0 ]; then
                echo "错误: 请提供电影名"
                exit 1
            fi
            auto_download "$*"
            ;;
        magnet)
            shift
            if [ $# -eq 0 ]; then
                echo "错误: 请提供详情页 URL"
                exit 1
            fi
            get_and_download "$1"
            ;;
        --help|-h)
            usage
            ;;
        *)
            # 默认使用全自动模式
            auto_download "$*"
            ;;
    esac
}

main "$@"
