#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
打印 ZIP 文件的文件树结构
"""

import zipfile
import os
import sys
from pathlib import Path


def print_zip_tree(zip_path, prefix="", is_last=True, show_size=False):
    """
    递归打印 ZIP 文件的文件树结构
    
    Args:
        zip_path: ZIP 文件路径
        prefix: 当前行的前缀（用于树形结构）
        is_last: 是否是最后一个节点
        show_size: 是否显示文件大小
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 获取所有文件信息
            file_list = zip_ref.namelist()
            
            # 构建目录树结构
            tree = {}
            for file_name in file_list:
                parts = file_name.rstrip('/').split('/')
                current = tree
                for part in parts:
                    if part:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
            
            # 打印树形结构
            def print_tree(node, prefix, is_last_node):
                items = list(node.items())
                for i, (name, children) in enumerate(items):
                    is_last_item = (i == len(items) - 1)
                    
                    # 打印当前节点
                    if is_last_node:
                        connector = "└── " if is_last_item else "├── "
                        new_prefix = prefix + ("    " if is_last_item else "│   ")
                    else:
                        connector = "└── " if is_last_item else "├── "
                        new_prefix = prefix + ("    " if is_last_item else "│   ")
                    
                    # 获取文件信息
                    full_path = name
                    if zip_ref:
                        try:
                            info = zip_ref.getinfo(full_path if full_path in file_list else full_path + '/')
                            file_size = info.file_size
                            is_dir = info.is_dir()
                        except:
                            # 尝试查找匹配的路径
                            matching = [f for f in file_list if f.startswith(full_path + '/') or f == full_path]
                            if matching:
                                try:
                                    info = zip_ref.getinfo(matching[0])
                                    file_size = info.file_size
                                    is_dir = info.is_dir() or matching[0].endswith('/')
                                except:
                                    file_size = 0
                                    is_dir = len(children) > 0
                            else:
                                file_size = 0
                                is_dir = len(children) > 0
                    else:
                        file_size = 0
                        is_dir = len(children) > 0
                    
                    # 显示节点名称和大小
                    if show_size and not is_dir:
                        size_str = f" ({file_size} bytes)"
                    else:
                        size_str = ""
                    
                    dir_marker = "/" if is_dir else ""
                    print(f"{prefix}{connector}{name}{dir_marker}{size_str}")
                    
                    # 递归打印子节点
                    if children:
                        print_tree(children, new_prefix, is_last_item)
            
            # 打印 ZIP 文件名
            zip_name = os.path.basename(zip_path)
            print(f"{zip_name}")
            print("│")
            
            # 打印文件树
            print_tree(tree, "", True)
            
            # 打印统计信息
            print("\n" + "="*50)
            print(f"总文件数: {len([f for f in file_list if not f.endswith('/')])}")
            print(f"总目录数: {len([f for f in file_list if f.endswith('/')])}")
            total_size = sum(zip_ref.getinfo(f).file_size for f in file_list if not f.endswith('/'))
            print(f"总大小: {total_size} bytes ({total_size / 1024:.2f} KB)")
            
    except zipfile.BadZipFile:
        print(f"错误: {zip_path} 不是一个有效的 ZIP 文件")
        sys.exit(1)
    except FileNotFoundError:
        print(f"错误: 文件 {zip_path} 不存在")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


def print_zip_tree_simple(zip_path, show_size=False):
    """
    简化版本：直接打印 ZIP 文件中的所有文件路径
    
    Args:
        zip_path: ZIP 文件路径
        show_size: 是否显示文件大小
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            
            print(f"\nZIP 文件: {os.path.basename(zip_path)}")
            print("="*50)
            
            # 按路径排序
            file_list.sort()
            
            for file_name in file_list:
                if file_name.endswith('/'):
                    # 目录
                    print(f"[DIR] {file_name}")
                else:
                    # 文件
                    try:
                        info = zip_ref.getinfo(file_name)
                        if show_size:
                            print(f"[FILE] {file_name} ({info.file_size} bytes)")
                        else:
                            print(f"[FILE] {file_name}")
                    except:
                        print(f"[FILE] {file_name}")
            
            # 统计信息
            files = [f for f in file_list if not f.endswith('/')]
            dirs = [f for f in file_list if f.endswith('/')]
            total_size = sum(zip_ref.getinfo(f).file_size for f in files)
            
            print("\n" + "="*50)
            print(f"总文件数: {len(files)}")
            print(f"总目录数: {len(dirs)}")
            print(f"总大小: {total_size} bytes ({total_size / 1024:.2f} KB)")
            
    except zipfile.BadZipFile:
        print(f"错误: {zip_path} 不是一个有效的 ZIP 文件")
        sys.exit(1)
    except FileNotFoundError:
        print(f"错误: 文件 {zip_path} 不存在")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python print_zip_tree.py <zip_file_path> [--simple] [--size]")
        print("\n参数说明:")
        print("  zip_file_path: ZIP 文件路径")
        print("  --simple: 使用简化模式（列表形式）")
        print("  --size: 显示文件大小")
        print("\n示例:")
        print("  python print_zip_tree.py example.zip")
        print("  python print_zip_tree.py example.zip --simple")
        print("  python print_zip_tree.py example.zip --size")
        sys.exit(1)
    
    zip_path = sys.argv[1]
    use_simple = '--simple' in sys.argv
    show_size = '--size' in sys.argv
    
    # 检查文件是否存在
    if not os.path.exists(zip_path):
        print(f"错误: 文件 {zip_path} 不存在")
        sys.exit(1)
    
    # 打印文件树
    if use_simple:
        print_zip_tree_simple(zip_path, show_size)
    else:
        print_zip_tree(zip_path, show_size=show_size)


if __name__ == "__main__":
    main()
