#!/usr/bin/env python3
"""
智慧交通数据分析系统一键运行脚本
"""
import os
import sys
import subprocess
import platform

def run_command(cmd, cwd=None):
    """
    运行命令并返回结果
    """
    print(f"执行命令: {cmd}")
    # 使用UTF-8编码捕获输出，避免编码错误
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    print(result.stdout)
    if result.stderr:
        print(f"错误: {result.stderr}")
    return result.returncode

def main():
    print("=== 智慧交通数据分析系统一键运行脚本 ===")
    print()
    
    # 检查Python环境
    print("检查Python环境...")
    python_version = platform.python_version()
    print(f"当前Python版本: {python_version}")
    
    # 运行主程序
    print("\n运行主程序...")
    if run_command("python main.py") != 0:
        print("错误：主程序运行失败")
        return 1
    print("主程序运行完成")
    
    # 启动可视化仪表盘
    print("\n启动可视化仪表盘...")
    print("注意：可视化仪表盘将在浏览器中打开")
    
    # Windows系统
    subprocess.Popen("start cmd /k \"streamlit run src\\visualization\\dashboard.py\"", shell=True)
    
    print("\n=== 系统启动完成 ===")
    print("请在浏览器中查看可视化仪表盘")
    return 0

if __name__ == "__main__":
    sys.exit(main())