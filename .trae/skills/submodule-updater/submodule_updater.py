#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Submodule 更新工具
支持更新所有子模块或指定目录下的子模块
"""

import os
import re
import subprocess
import time
from typing import List, Tuple, Optional
from pathlib import Path


class SubmoduleUpdater:
    """Git Submodule 更新器类"""

    def __init__(self, base_dir: str = None):
        """
        初始化更新器
        
        Args:
            base_dir: 基础目录路径，默认为当前工作目录
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.success_count = 0
        self.failure_count = 0
        self.start_time = 0

    def parse_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """
        解析用户指令
        
        Args:
            command: 用户输入的指令
            
        Returns:
            (是否更新全部, 目录路径)
        """
        command = command.strip()
        command_lower = command.lower()
        
        # 模式2：更新指定目录下的子模块（先检查，避免被"所有"模式匹配）
        patterns_dir = [
            r'更新\s*(.+?)\s*下的\s*submodule',
            r'update\s+submodules\s+in\s+(.+)',
            r'update\s+(.+)\s+submodules'
        ]
        
        for pattern in patterns_dir:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                dir_path = match.group(1).strip()
                # 统一路径分隔符
                dir_path = dir_path.replace('\\', '/')
                return (False, dir_path)
        
        # 模式1：更新所有子模块
        patterns_all = [
            r'更新所有submodule',
            r'更新全部submodule',
            r'update\s+all\s+submodules',
            r'update\s+every\s+submodule'
        ]
        
        for pattern in patterns_all:
            if re.search(pattern, command, re.IGNORECASE):
                return (True, None)
        
        # 默认返回更新所有
        return (True, None)

    def check_git_repository(self) -> bool:
        """
        检查当前目录是否为 Git 仓库
        
        Returns:
            是否为 Git 仓库
        """
        git_dir = self.base_dir / '.git'
        return git_dir.exists()

    def check_gitmodules(self) -> bool:
        """
        检查是否存在 .gitmodules 文件
        
        Returns:
            是否存在 .gitmodules 文件
        """
        gitmodules = self.base_dir / '.gitmodules'
        return gitmodules.exists()

    def check_directory(self, dir_path: str) -> bool:
        """
        检查指定目录是否存在
        
        Args:
            dir_path: 目录路径
            
        Returns:
            目录是否存在
        """
        target_dir = self.base_dir / dir_path
        return target_dir.exists() and target_dir.is_dir()

    def get_submodules(self) -> List[str]:
        """
        获取所有子模块列表
        
        Returns:
            子模块路径列表
        """
        try:
            result = subprocess.run(
                ['git', 'submodule', 'status'],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                return []
            
            submodules = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    # 子模块状态格式: [-+ ]<sha1> <path> <description>
                    parts = line.split()
                    if len(parts) >= 2:
                        submodules.append(parts[1])
            
            return submodules
        except Exception:
            return []

    def update_submodule(self, submodule_path: str) -> Tuple[bool, str]:
        """
        更新单个子模块
        
        Args:
            submodule_path: 子模块路径
            
        Returns:
            (是否成功, 错误信息)
        """
        try:
            result = subprocess.run(
                ['git', 'submodule', 'update', '--remote', '--merge', submodule_path],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return (True, '')
            else:
                error_msg = result.stderr.strip() if result.stderr else '未知错误'
                return (False, error_msg)
        except Exception as e:
            return (False, str(e))

    def update_all_submodules(self) -> None:
        """更新所有子模块"""
        try:
            result = subprocess.run(
                ['git', 'submodule', 'update', '--remote', '--merge'],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                # 解析输出以获取更新的子模块
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines:
                    if line.strip():
                        print(f"✓ {line.strip()}")
                self.success_count = len(output_lines)
            else:
                print(f"✗ 错误: {result.stderr.strip()}")
                self.failure_count = 1
        except Exception as e:
            print(f"✗ 错误: {str(e)}")
            self.failure_count = 1

    def execute(self, command: str) -> bool:
        """
        执行更新操作
        
        Args:
            command: 用户指令
            
        Returns:
            是否成功执行
        """
        self.start_time = time.time()
        self.success_count = 0
        self.failure_count = 0
        
        # 解析指令
        update_all, dir_path = self.parse_command(command)
        
        # 验证环境
        if not self.check_git_repository():
            print("✗ 错误: 当前目录不是 Git 仓库", flush=True)
            return False
        
        if not self.check_gitmodules():
            print("✗ 错误: 未找到任何子模块（.gitmodules 文件不存在）", flush=True)
            return False
        
        if not update_all:
            if not self.check_directory(dir_path):
                print(f"✗ 错误: 指定的目录不存在: {dir_path}", flush=True)
                return False
        
        # 执行更新
        if update_all:
            print("✓ 开始更新所有子模块...", flush=True)
            self.update_all_submodules()
        else:
            print(f"✓ 开始更新 {dir_path} 目录下的子模块...", flush=True)
            
            # 获取指定目录下的子模块
            all_submodules = self.get_submodules()
            target_submodules = [
                sub for sub in all_submodules 
                if sub.startswith(dir_path)
            ]
            
            if not target_submodules:
                print(f"✗ 错误: 在 {dir_path} 目录下未找到任何子模块", flush=True)
                return False
            
            # 逐个更新子模块
            for submodule in target_submodules:
                print(f"✓ 正在更新: {submodule}", flush=True)
                success, error = self.update_submodule(submodule)
                
                if success:
                    print(f"✓ 子模块 {submodule} 更新成功", flush=True)
                    self.success_count += 1
                else:
                    print(f"✗ 子模块 {submodule} 更新失败: {error}", flush=True)
                    self.failure_count += 1
        
        # 显示统计信息
        elapsed_time = time.time() - self.start_time
        print("\n✓ 子模块更新完成", flush=True)
        print(f"✓ 成功: {self.success_count} 个", flush=True)
        print(f"✗ 失败: {self.failure_count} 个", flush=True)
        print(f"⏱ 总耗时: {elapsed_time:.1f} 秒", flush=True)
        
        return self.failure_count == 0


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python submodule_updater.py <指令>")
        print("示例:")
        print("  python submodule_updater.py '更新所有submodule'")
        print("  python submodule_updater.py '更新src/libs下的submodule'")
        sys.exit(1)
    
    command = ' '.join(sys.argv[1:])
    updater = SubmoduleUpdater()
    success = updater.execute(command)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
