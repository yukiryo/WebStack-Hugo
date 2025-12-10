#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对网站进行系统分类
"""

import json


def classify_bookmarks(bookmarks):
    """
    对网站进行系统分类
    
    Args:
        bookmarks: 网站信息列表
        
    Returns:
        dict: 分类后的网站信息，键是分类名称，值是网站列表
    """
    # 分类规则
    categories = {
        "游戏": {
            "原神相关": [],
            "Steam相关": [],
            "其他游戏": [],
            "游戏工具": []
        },
        "工具": {
            "开发工具": [],
            "在线工具": [],
            "浏览器扩展": [],
            "其他工具": []
        },
        "学习": {
            "知识库": [],
            "教程": [],
            "文档": []
        },
        "娱乐": {
            "视频": [],
            "音乐": [],
            "漫画": [],
            "其他娱乐": []
        },
        "其他": []
    }
    
    # 分类关键词
    keywords = {
        "原神相关": ["原神", "genshin", "mihoyo", "seelie", "cocogoat", "paimon", "honeyhunterworld", "mona-uranai", "enka", "wishsimulator"],
        "Steam相关": ["steam", "steamdb", "挂刀", "cs2", "csgod", "cs2ob"],
        "其他游戏": ["nga", "明日方舟", "prts", "崩坏3", "黑塔", "herta", "honkai", "hsr", "minecraft", "mcmod", "zh.minecraft.wiki", "植物僵尸", "jspvz", "switch520", "warzone", "wzguides", "wzhub", "三角洲", "kkrb", "acgice"],
        "游戏工具": ["feixiaoqiu", "原神规划助手", "椰羊", "莫娜占卜铺", "Genshin Optimizer", "游戏作弊器", "flingtrainer", "liquipedia", "游戏工具"],
        "开发工具": ["codexy", "代码学院"],
        "在线工具": ["tool.pc.wiki", "lightnote", "mikutools", "ping0", "cobalt", "massgrave"],
        "浏览器扩展": ["scriptcat", "greasyfork"],
        "其他工具": ["zeroroku", "hakush", "next.moeub", "juij.fun", "非线性列车"],
        "知识库": ["书伴", "bookfere"],
        "教程": ["整合包教程", "yuque"],
        "文档": [],
        "视频": ["bilibili", "libvio", "mtyy", "麦田影院"],
        "音乐": [],
        "漫画": ["kxo.moe", "kmoe", "鲲 Galgame", "kungal"],
        "其他娱乐": ["vtbs", "vtbs.moe", "spring-plus", "susuifa", "miobt", "kemono", "milovana", "yinghezhinan", "硬核指南", "flysheep6", "flysheep资源避难所"],
    }
    
    # 遍历所有网站，进行分类
    for bookmark in bookmarks:
        title = bookmark["title"].lower()
        url = bookmark["url"].lower()
        
        # 标记是否已分类
        classified = False
        
        # 遍历所有分类和关键词
        for main_cat, sub_cats in categories.items():
            if main_cat == "其他":
                continue
                
            for sub_cat, sites in sub_cats.items():
                for keyword in keywords.get(sub_cat, []):
                    if keyword in title or keyword in url:
                        sites.append(bookmark)
                        classified = True
                        break
                if classified:
                    break
            if classified:
                break
        
        # 如果没有分类，放入其他
        if not classified:
            categories["其他"].append(bookmark)
    
    return categories


def save_classified_bookmarks(classified_bookmarks, output_file):
    """
    保存分类后的书签信息到JSON文件
    
    Args:
        classified_bookmarks: 分类后的网站信息
        output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(classified_bookmarks, f, ensure_ascii=False, indent=2)
    
    print(f"分类后的书签信息已保存到 {output_file}")
    
    # 统计每个分类的网站数量
    print("\n分类统计：")
    for main_cat, sub_cats in classified_bookmarks.items():
        if main_cat == "其他":
            print(f"{main_cat}: {len(sub_cats)} 个网站")
        else:
            print(f"{main_cat}:")
            for sub_cat, sites in sub_cats.items():
                print(f"  {sub_cat}: {len(sites)} 个网站")


def generate_webstack_yml(classified_bookmarks, output_file):
    """
    生成webstack.yml文件内容
    
    Args:
        classified_bookmarks: 分类后的网站信息
        output_file: 输出文件路径
    """
    # 图标映射
    icons = {
        "游戏": "fas fa-gamepad fa-lg",
        "原神相关": "fas fa-gem fa-lg",
        "Steam相关": "fab fa-steam fa-lg",
        "其他游戏": "fas fa-gamepad fa-lg",
        "游戏工具": "fas fa-tools fa-lg",
        "工具": "fas fa-tools fa-lg",
        "开发工具": "fas fa-code fa-lg",
        "在线工具": "fas fa-wrench fa-lg",
        "浏览器扩展": "fas fa-puzzle-piece fa-lg",
        "其他工具": "fas fa-cog fa-lg",
        "学习": "fas fa-book fa-lg",
        "知识库": "fas fa-book fa-lg",
        "教程": "fas fa-graduation-cap fa-lg",
        "文档": "fas fa-file-alt fa-lg",
        "娱乐": "fas fa-film fa-lg",
        "视频": "fas fa-video fa-lg",
        "音乐": "fas fa-music fa-lg",
        "漫画": "fas fa-book-open fa-lg",
        "其他娱乐": "fas fa-star fa-lg",
        "其他": "fas fa-ellipsis-h fa-lg"
    }
    
    # 生成YAML内容
    yaml_content = "---\n\n"
    
    for main_cat, sub_cats in classified_bookmarks.items():
        # 跳过空分类
        if main_cat == "其他" and not sub_cats:
            continue
            
        if main_cat != "其他":
            # 检查是否有子分类有网站
            has_sites = False
            for sub_cat, sites in sub_cats.items():
                if sites:
                    has_sites = True
                    break
            
            if not has_sites:
                continue
            
            yaml_content += f"- taxonomy: {main_cat}\n"
            yaml_content += f"  icon: {icons[main_cat]}\n"
            yaml_content += "  list:\n"
            
            for sub_cat, sites in sub_cats.items():
                if not sites:
                    continue
                    
                yaml_content += f"    - term: {sub_cat}\n"
                yaml_content += "      links:\n"
                
                for site in sites:
                    # 处理标题中的冒号，用引号包裹
                    title = site['title']
                    if ':' in title:
                        title = f'\"{title}\"'
                    
                    yaml_content += f"        - title: {title}\n"
                    yaml_content += f"          url: {site['url']}\n"
                    if site['description']:
                        yaml_content += f"          description: {site['description']}\n"
                    yaml_content += "\n"
        else:
            # 其他分类直接使用links
            if sub_cats:
                yaml_content += f"- taxonomy: {main_cat}\n"
                yaml_content += f"  icon: {icons[main_cat]}\n"
                yaml_content += "  links:\n"
                
                for site in sub_cats:
                    # 处理标题中的冒号，用引号包裹
                    title = site['title']
                    if ':' in title:
                        title = f'\"{title}\"'
                    
                    yaml_content += f"    - title: {title}\n"
                    yaml_content += f"      url: {site['url']}\n"
                    if site['description']:
                        yaml_content += f"      description: {site['description']}\n"
                    yaml_content += "\n"
    
    # 保存到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    print(f"\nwebstack.yml文件已生成到 {output_file}")


if __name__ == "__main__":
    # 读取提取的书签信息
    with open('bookmarks.json', 'r', encoding='utf-8') as f:
        bookmarks = json.load(f)
    
    # 去重
    unique_bookmarks = []
    seen_urls = set()
    for bookmark in bookmarks:
        if bookmark['url'] not in seen_urls:
            seen_urls.add(bookmark['url'])
            unique_bookmarks.append(bookmark)
    
    print(f"去重后共 {len(unique_bookmarks)} 个网站")
    
    # 分类
    classified_bookmarks = classify_bookmarks(unique_bookmarks)
    
    # 保存分类结果
    save_classified_bookmarks(classified_bookmarks, 'classified_bookmarks.json')
    
    # 生成webstack.yml文件
    generate_webstack_yml(classified_bookmarks, 'exampleSite/data/webstack.yml')
