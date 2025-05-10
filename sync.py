import os, re, datetime, yaml

# ========== 配置区域 ==========
# Obsidian 笔记库根目录（请修改为实际路径）
OBSIDIAN_DIR = "/Users/haoenhuang/Desktop/Obsidian/GhostBlue/读书笔记"
# Hexo 博客 posts 目录（请修改为实际 Hexo 项目路径）
HEXO_POSTS_DIR = "/Users/haoenhuang/Desktop/blog/source/_posts"
# =============================

# 确保输出目录存在
os.makedirs(HEXO_POSTS_DIR, exist_ok=True)

# 用于收集警告信息
warnings = []
# 用于记录已处理的文件名（用于清理过期文件）
processed = set()

for root, dirs, files in os.walk(OBSIDIAN_DIR):
    for filename in files:
        if not filename.endswith(".md"):
            continue  # 只处理 Markdown 文件
        name_no_ext = os.path.splitext(filename)[0]
        folder_name = os.path.basename(root)
        # 跳过索引文件：文件名（不含扩展）与所在文件夹同名的文件
        if name_no_ext == folder_name:
            continue

        filepath = os.path.join(root, filename)
        try:
            text = open(filepath, 'r', encoding='utf-8').read()
        except Exception as e:
            warnings.append(f"Warning: 无法读取文件 {filepath} ({e})")
            continue

        # 查找 YAML Front Matter 块
        lines = text.splitlines()
        if not lines or lines[0].strip() != '---':
            warnings.append(f"Warning: 文件 {filename} 缺少 YAML Front Matter，已跳过")
            continue
        try:
            closing_index = lines.index('---', 1)
        except ValueError:
            warnings.append(f"Warning: 文件 {filename} 的 Front Matter 缺少结束分隔符 '---'")
            continue

        # 提取 Front Matter 内容并解析 YAML
        fm_lines = lines[1:closing_index]
        content_lines = lines[closing_index+1:]
        fm_text = "\n".join(fm_lines)
        try:
            data = yaml.safe_load(fm_text)
        except Exception as e:
            warnings.append(f"Warning: YAML 解析 {filename} 时出错: {e}")
            continue
        if not isinstance(data, dict):
            warnings.append(f"Warning: 文件 {filename} 的 Front Matter 格式不正确，已跳过")
            continue

        # 提取标题，日期字段
        title = data.get('title', name_no_ext)
        # 优先选用 date 字段，否则使用 date_creation 或 created，其次使用 modified
        date_val = data.get('date') or data.get('date_creation') or data.get('created') or data.get('modified')
        if date_val is None:
            warnings.append(f"Warning: 文件 {filename} 无日期字段，默认使用当前日期")
            date_val = datetime.datetime.now()
        # 将 date 转为字符串（Hexo 要求具体日期时间格式）
        if isinstance(date_val, datetime.datetime):
            date_str = date_val.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(date_val, datetime.date):
            date_str = date_val.strftime("%Y-%m-%d")
        else:
            # 如果是字符串，尝试解析为统一格式
            date_str = str(date_val)
            try:
                # 优先尝试标准格式 YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
                parsed = datetime.datetime.fromisoformat(date_str)
            except Exception:
                parsed = None
                # 尝试常见日期格式
                for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%b %d %Y", "%B %d %Y"):
                    try:
                        parsed = datetime.datetime.strptime(date_str, fmt)
                        break
                    except Exception:
                        continue
            if parsed:
                # 只有日期没有时间则格式化为 YYYY-MM-DD，否则带上时间
                if parsed.time() == datetime.time(0, 0):
                    date_str = parsed.strftime("%Y-%m-%d")
                else:
                    date_str = parsed.strftime("%Y-%m-%d %H:%M:%S")
            # 若仍未能解析，则保持原格式字符串
        # 提取并合并标签
        tags_seen = set()
        tags_list = []

        # 处理 Front Matter 中的 tags 字段
        yaml_tags = data.get('tags')
        if yaml_tags:
            if isinstance(yaml_tags, list):
                for tag in yaml_tags:
                    if tag is None:
                        # YAML 将 "- #标签" 解析为 None（注释），此时尝试从原文本恢复
                        continue
                    if not isinstance(tag, str):
                        tag = str(tag)
                    t = tag.strip()
                    if t.startswith('#'):
                        t = t.lstrip('#')
                    # 去除尾部可能的标点符号
                    t = t.rstrip("，。,.?；;!$")
                    if t and t not in tags_seen:
                        tags_seen.add(t)
                        tags_list.append(t)
                # 补充：恢复 YAML 中被当作注释解析掉的标签
                for line in fm_lines:
                    stripped = line.strip()
                    if stripped.startswith('-'):
                        after_dash = stripped[1:].lstrip()
                        if after_dash.startswith('#'):
                            raw_tag = after_dash[1:].strip()
                            if raw_tag and raw_tag not in tags_seen:
                                tags_seen.add(raw_tag)
                                tags_list.append(raw_tag)
            elif isinstance(yaml_tags, str):
                tag_str = yaml_tags.strip()
                if tag_str:
                    if '#' in tag_str:
                        # 如 "tags: #tag1 #tag2"
                        candidates = re.findall(r'#([\w\-\u4e00-\u9fff]+)', tag_str)
                        if not candidates:
                            candidates = [tag_str]
                    else:
                        # 如 "tags: tag1, tag2" 或 "tag1 tag2"
                        if ',' in tag_str:
                            parts = [p.strip() for p in tag_str.split(',') if p.strip()]
                        elif '；' in tag_str or ';' in tag_str:
                            parts = [p.strip() for p in re.split('[;；]', tag_str) if p.strip()]
                        else:
                            parts = tag_str.split()
                        candidates = parts
                    for t in candidates:
                        t = t.strip()
                        if t.startswith('#'):
                            t = t.lstrip('#')
                        t = t.rstrip("，。,.?；;!$")
                        if t and t not in tags_seen:
                            tags_seen.add(t)
                            tags_list.append(t)

        # 扫描正文内容中的 #标签
        content_text = "\n".join(content_lines)
        for match in re.finditer(r'#([\w\-\u4e00-\u9fff]+)', content_text):
            tag = match.group(1)
            # 排除纯数字（如 #2023 在正文可能是章节号而非标签；酌情处理，这里不严过滤）
            tag = tag.rstrip("，。,.?；;!$")
            if tag and tag not in tags_seen:
                tags_seen.add(tag)
                tags_list.append(tag)

        # 构造新的 Front Matter 数据
        front_matter = {
            'title': title,
            'date': date_str,
            'tags': tags_list
        }

        # 将结果写入 Hexo 博客的 _posts 目录
        output_path = os.path.join(HEXO_POSTS_DIR, filename)
        try:
            with open(output_path, 'w', encoding='utf-8') as f_out:
                f_out.write("---\n")
                # 使用 yaml.safe_dump 输出 YAML，保证 Unicode 正常写出
                yaml.safe_dump(front_matter, f_out, allow_unicode=True, sort_keys=False)
                f_out.write("---\n")
                # 写入正文内容，保持原有换行和格式
                if content_lines:
                    f_out.write("\n".join(content_lines).strip() + "\n")
                else:
                    f_out.write("\n")
            # 标记此文件已处理，后续用于清理多余文件
            processed.add(filename)
        except Exception as e:
            warnings.append(f"Warning: 写入文件 {output_path} 时出错: {e}")

# 输出所有警告信息
for w in warnings:
    print(w)
# ====== prune step：删除 Hexo 里多余的文件 ======
for existing in os.listdir(HEXO_POSTS_DIR):
    if existing.endswith(".md") and existing not in processed:
        try:
            os.remove(os.path.join(HEXO_POSTS_DIR, existing))
            print(f"Prune: 删除过期文章 {existing}")
        except Exception as e:
            print(f"Warning: 删除 {existing} 失败: {e}")
print(f"同步完成，共处理 {len(os.listdir(HEXO_POSTS_DIR))} 篇笔记。")
