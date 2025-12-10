#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为网站查找并添加合适的图标
"""

import os
import yaml
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse


def load_webstack(file_path):
    """
    加载webstack.yml文件
    
    Args:
        file_path: webstack.yml文件路径
        
    Returns:
        list: webstack数据
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_webstack(data, file_path):
    """
    保存webstack.yml文件
    
    Args:
        data: webstack数据
        file_path: webstack.yml文件路径
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def get_domain(url):
    """
    从URL中提取域名
    
    Args:
        url: 网站URL
        
    Returns:
        str: 域名
    """
    parsed = urlparse(url)
    return parsed.netloc


def find_favicon(url):
    """
    查找网站的favicon
    
    Args:
        url: 网站URL
        
    Returns:
        str: favicon URL
    """
    try:
        # 发送请求获取网页内容，忽略SSL验证
        response = requests.get(url, timeout=5, verify=False)
        response.raise_for_status()
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找favicon链接
        favicon = None
        
        # 查找link标签中的favicon
        link_tags = soup.find_all('link', rel=lambda x: x and ('icon' in x.lower() or 'shortcut' in x.lower()))
        for tag in link_tags:
            if tag.get('href'):
                favicon = tag.get('href')
                break
        
        # 如果没有找到，尝试默认路径
        if not favicon:
            domain = get_domain(url)
            favicon = f"https://{domain}/favicon.ico"
        
        # 处理相对路径
        if favicon and not favicon.startswith(('http://', 'https://')):
            if favicon.startswith('/'):
                domain = get_domain(url)
                favicon = f"https://{domain}{favicon}"
            else:
                favicon = f"{url.rstrip('/')}/{favicon}"
        
        return favicon
    except Exception as e:
        print(f"查找favicon失败 {url}: {e}")
        return None


def download_favicon(favicon_url, save_path):
    """
    下载favicon
    
    Args:
        favicon_url: favicon URL
        save_path: 保存路径
        
    Returns:
        bool: 是否下载成功
    """
    try:
        response = requests.get(favicon_url, timeout=5, verify=False)
        response.raise_for_status()
        
        # 确定文件扩展名
        content_type = response.headers.get('content-type', '')
        if 'image/png' in content_type:
            ext = 'png'
        elif 'image/jpeg' in content_type or 'image/jpg' in content_type:
            ext = 'jpg'
        elif 'image/gif' in content_type:
            ext = 'gif'
        elif 'image/webp' in content_type:
            ext = 'webp'
        else:
            # 尝试从URL中获取扩展名
            ext = favicon_url.split('.')[-1].lower()
            if ext not in ['png', 'jpg', 'gif', 'webp', 'ico']:
                ext = 'ico'
        
        # 保存文件
        save_path_with_ext = f"{save_path}.{ext}"
        with open(save_path_with_ext, 'wb') as f:
            f.write(response.content)
        
        return save_path_with_ext
    except Exception as e:
        print(f"下载favicon失败 {favicon_url}: {e}")
        return None


def update_webstack_icons(webstack_data, logos_dir):
    """
    更新webstack数据中的图标
    
    Args:
        webstack_data: webstack数据
        logos_dir: 图标保存目录
        
    Returns:
        list: 更新后的webstack数据
    """
    # 确保logos目录存在
    os.makedirs(logos_dir, exist_ok=True)
    
    processed_count = 0
    
    for taxonomy in webstack_data:
        if 'list' in taxonomy:
            # 有子分类
            for term in taxonomy['list']:
                for link in term['links']:
                    # 跳过已有图标的网站
                    if 'logo' in link and link['logo'] != 'default.webp':
                        continue
                    
                    processed_count += 1
                    print(f"处理第 {processed_count} 个网站: {link['title']}")
                    
                    url = link['url']
                    title = link['title']
                    
                    # 查找favicon
                    favicon_url = find_favicon(url)
                    if favicon_url:
                        # 生成保存路径
                        domain = get_domain(url)
                        # 清理文件名
                        safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_').lower()
                        save_path = os.path.join(logos_dir, safe_title)
                        
                        # 下载favicon
                        saved_file = download_favicon(favicon_url, save_path)
                        if saved_file:
                            # 更新logo字段
                            logo_filename = os.path.basename(saved_file)
                            link['logo'] = logo_filename
                            print(f"已为 {title} 添加图标: {logo_filename}")
        elif 'links' in taxonomy:
            # 没有子分类
            for link in taxonomy['links']:
                # 跳过已有图标的网站
                if 'logo' in link and link['logo'] != 'default.webp':
                    continue
                
                processed_count += 1
                print(f"处理第 {processed_count} 个网站: {link['title']}")
                
                url = link['url']
                title = link['title']
                
                # 查找favicon
                favicon_url = find_favicon(url)
                if favicon_url:
                    # 生成保存路径
                    domain = get_domain(url)
                    # 清理文件名
                    safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_').lower()
                    save_path = os.path.join(logos_dir, safe_title)
                    
                    # 下载favicon
                    saved_file = download_favicon(favicon_url, save_path)
                    if saved_file:
                        # 更新logo字段
                        logo_filename = os.path.basename(saved_file)
                        link['logo'] = logo_filename
                        print(f"已为 {title} 添加图标: {logo_filename}")
    
    return webstack_data


if __name__ == "__main__":
    # 配置
    webstack_file = "exampleSite/data/webstack.yml"
    logos_dir = "static/assets/images/logos"
    
    # 打印当前工作目录
    print(f"当前工作目录: {os.getcwd()}")
    print(f"webstack文件路径: {os.path.abspath(webstack_file)}")
    print(f"logos目录路径: {os.path.abspath(logos_dir)}")
    
    # 加载webstack数据
    print("加载webstack数据...")
    webstack_data = load_webstack(webstack_file)
    print(f"加载的数据长度: {len(webstack_data)}")
    
    # 更新图标
    print("开始更新图标...")
    updated_data = update_webstack_icons(webstack_data, logos_dir)
    
    # 保存更新后的数据
    print("保存更新后的数据...")
    save_webstack(updated_data, webstack_file)
    print(f"数据已保存到: {os.path.abspath(webstack_file)}")
    
    # 验证保存结果
    print("验证保存结果...")
    reloaded_data = load_webstack(webstack_file)
    # 检查第一个网站的logo是否已更新
    if len(reloaded_data) > 0 and 'list' in reloaded_data[0]:
        first_site = reloaded_data[0]['list'][0]['links'][0]
        print(f"第一个网站: {first_site['title']}, logo: {first_site['logo']}")
    
    print("图标更新完成!")
