#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证YAML文件格式是否正确
"""

import yaml


def validate_yaml(file_path):
    """
    验证YAML文件格式是否正确
    
    Args:
        file_path: YAML文件路径
        
    Returns:
        bool: True表示格式正确，False表示格式错误
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print(f"{file_path} 文件格式正确")
        return True
    except yaml.YAMLError as e:
        print(f"{file_path} 文件格式错误: {e}")
        return False


if __name__ == "__main__":
    # 验证webstack.yml文件
    validate_yaml('exampleSite/data/webstack.yml')
