#!/usr/bin/env python3
import os
import subprocess
import json
import argparse
from typing import List, Dict, Optional

def run_package_crp(project: Dict, defaults: Dict, args: argparse.Namespace):
    """执行单个项目的package-crp.py"""
    cmd = ["dev-tool", "crp", args.command if hasattr(args, 'command') else "pack"]
    
    # 添加所有支持的参数
    params = {
        'topic': args.topic if hasattr(args, 'topic') else None,
        'name': project.get('name', defaults.get('name')),
        'tag': args.tag if hasattr(args, 'tag') else project.get('projectTag', defaults.get('projectTag')),
        'branch': project.get('branch', defaults.get('branch'))
    }
    
    # 添加非空参数到命令
    for param, value in params.items():
        if value:
            if isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{param}", item])
            else:
                cmd.extend([f"--{param}", value])
    
    try:
        project_name = params.get('name', '未命名项目')
        print(f"执行项目: {project_name}")
        subprocess.run(cmd, check=True)
        print(f"项目 {project_name} 完成")
    except subprocess.CalledProcessError as e:
        print(f"项目 {project_name} 执行失败: {e}")

def main():
    parser = argparse.ArgumentParser(description='批量执行package-crp.py')
    parser.add_argument('command', nargs='?', default='pack', 
                       choices=['pack', 'test', 'lasttag'], help='执行的命令')
    parser.add_argument('--config', default='packages/batch-package-crp.packages', 
                       help='配置文件路径')
    # 添加所有package-crp支持的参数
    parser.add_argument('--topic', help='topic名称')
    parser.add_argument('--tag', help='项目tag')
    args = parser.parse_args()

    def find_config_file(filename):
        """查找配置文件，如果是绝对路径直接检查，否则尝试多个默认路径"""
        # 如果是绝对路径，直接检查
        if os.path.isabs(filename):
            if os.path.exists(filename):
                return filename
            raise FileNotFoundError(f"Config file not found at absolute path: {filename}")

        # 相对路径时尝试多个默认位置
        search_paths = [
            os.path.join(os.getcwd(), filename),  # 当前目录
            os.path.expanduser(f'~/.config/dev-tool/packages/{filename}'),  # packages目录
            os.path.expanduser(f'~/.config/dev-tool/{filename}')  # 默认config目录
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                return path
                
        raise FileNotFoundError(
            f"Could not find config file {filename} in: current directory, "
            f"~/.config/dev-tool/packages/, ~/.config/dev-tool/"
        )

    try:
        config_path = find_config_file(args.config)
        with open(config_path) as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"错误: 配置文件 {args.config} 不存在于以下路径: 当前目录, ~/.config/dev-tool/packages/, ~/.config/dev-tool/")
        return
    except json.JSONDecodeError:
        print(f"错误: 配置文件 {config_path} 格式不正确")
        return

    defaults = config.get('defaults', {})
    projects = config.get('projects', [])

    if not projects:
        print("警告: 配置文件中没有定义项目")
        return

    for project in projects:
        run_package_crp(project, defaults, args)

if __name__ == "__main__":
    main()
