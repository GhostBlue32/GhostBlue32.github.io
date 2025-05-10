#!/usr/bin/env bash
# 1. 同步 Obsidian 笔记到 Hexo
python sync_notes.py

# 2. 提交并推源码分支
git add source/_posts
git commit -m "chore: sync notes from Obsidian"
git push origin main

# 3. 生成并部署到 gh-pages
hexo clean
hexo g
hexo d