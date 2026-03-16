#!/bin/bash
# Movie Downloader Skill 发布脚本

echo "🎬 Movie Downloader Skill 发布工具"
echo "===================================="
echo ""

# 检查必要文件
echo "📋 检查必要文件..."
required_files=("SKILL.md" "README.md" "movie-download.py")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file 不存在"
        exit 1
    fi
done

echo ""
echo "📦 打包 Skill..."

# 创建发布目录
mkdir -p dist
cp -r *.md *.py dist/

# 创建压缩包
cd dist
tar -czf movie-downloader-v1.0.0.tar.gz *
cd ..

echo ""
echo "✅ 打包完成: dist/movie-downloader-v1.0.0.tar.gz"
echo ""
echo "📤 发布方式:"
echo ""
echo "1. 上传到 GitHub:"
echo "   - 创建仓库: https://github.com/new"
echo "   - 仓库名: movie-downloader"
echo "   - 上传文件: SKILL.md, README.md, movie-download.py"
echo ""
echo "2. 提交到 SkillHub:"
echo "   - 联系 SkillHub 管理员"
echo "   - 提供 GitHub 仓库链接"
echo "   - 等待审核收录"
echo ""
echo "3. 手动安装:"
echo "   git clone https://github.com/yourusername/movie-downloader.git"
echo "   cd movie-downloader"
echo "   chmod +x movie-download.py"
echo ""
