#!/usr/bin/env bash
set -e
# 切到博客根目录
cd /Users/haoenhuang/Desktop/blog

# 1. 同步 Obsidian 笔记到 Hexo
python3 sync.py

# 2. 提交并推送源码分支
git add .
MSG="sync notes at $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$MSG" || true
git push origin main

# 3. 生成 & 部署到 gh-pages
hexo clean
hexo generate
hexo deploy

echo "✅ 全部完成！"