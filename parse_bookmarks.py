#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析HTML书签文件，提取网站信息
"""

import os
import json
from bs4 import BeautifulSoup


def parse_bookmarks(file_path):
    """
    解析HTML书签文件，提取网站信息
    
    Args:
        file_path: HTML书签文件路径
        
    Returns:
        list: 网站信息列表，每个元素是包含title、url、description的字典
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有的书签链接
    bookmarks = []
    
    # 查找所有的DT标签，其中包含A标签的就是书签
    for dt in soup.find_all('dt'):
        a_tag = dt.find('a')
        if a_tag:
            # 提取书签信息
            title = a_tag.text.strip()
            url = a_tag.get('href', '').strip()
            
            # 提取描述信息（如果有的话）
            description = a_tag.get('description', '')
            if not description:
                # 尝试从下一个DD标签中获取描述
                dd_tag = dt.find_next_sibling('dd')
                if dd_tag:
                    description = dd_tag.text.strip()
            
            # 只添加有效的URL
            if url and url.startswith(('http://', 'https://')):
                bookmarks.append({
                    'title': title,
                    'url': url,
                    'description': description
                })
    
    return bookmarks


def save_bookmarks(bookmarks, output_file):
    """
    保存书签信息到JSON文件
    
    Args:
        bookmarks: 网站信息列表
        output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)
    
    print(f"书签信息已保存到 {output_file}")
    print(f"共提取到 {len(bookmarks)} 个有效书签")


if __name__ == "__main__":
    # HTML书签文件路径
    html_file = "favorites_2025_12_1.html"
    
    # 输出JSON文件路径
    output_file = "bookmarks.json"
    
    # 解析书签
    bookmarks = parse_bookmarks(html_file)
    
    # 保存书签信息
    save_bookmarks(bookmarks, output_file)
