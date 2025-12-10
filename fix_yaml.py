#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复YAML文件中的格式问题
"""

import json


def fix_yaml_file(input_file, output_file):
    """
    修复YAML文件中的格式问题
    
    Args:
        input_file: 输入YAML文件路径
        output_file: 输出YAML文件路径
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 修复包含冒号的标题
    fixed_lines = []
    for line in lines:
        if line.strip().startswith('- title:'):
            # 检查标题中是否包含冒号
            if ':' in line[9:].strip() and not (line[9:].strip().startswith('"') or line[9:].strip().startswith("'")):
                # 提取标题内容
                title = line[9:].strip()
                # 用引号包裹标题
                fixed_line = f"        - title: \"{title}\"\n"
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # 保存修复后的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"YAML文件已修复并保存到 {output_file}")


if __name__ == "__main__":
    # 修复webstack.yml文件
    fix_yaml_file('exampleSite/data/webstack.yml', 'exampleSite/data/webstack.yml.fixed')
