#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def install(dev: bool = False) -> None:
    """安装项目依赖"""
    cmd = ["uv", "pip", "install", "-r"]
    if dev:
        cmd.append("requirements-dev.txt")
    else:
        cmd.append("requirements.txt")
    subprocess.run(cmd, check=True)


def format_code() -> None:
    """格式化代码"""
    subprocess.run(["black", "."], check=True)
    subprocess.run(["isort", "."], check=True)


def lint() -> None:
    """运行代码检查"""
    subprocess.run(["ruff", "check", "."], check=True)
    subprocess.run(["mypy", "services/"], check=True)


def test() -> None:
    """运行测试"""
    subprocess.run(["pytest", "tests/"], check=True)


def clean() -> None:
    """清理生成的文件"""
    root = Path(".")
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyi",
        "**/*_pb2.py",
        "**/*_pb2_grpc.py",
    ]

    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                for file in path.iterdir():
                    file.unlink()
                path.rmdir()


def main() -> None:
    parser = argparse.ArgumentParser(description="开发工具脚本")
    parser.add_argument(
        "command", choices=["install", "install-dev", "format", "lint", "test", "clean"]
    )

    args = parser.parse_args()

    try:
        if args.command == "install":
            install()
        elif args.command == "install-dev":
            install(dev=True)
        elif args.command == "format":
            format_code()
        elif args.command == "lint":
            lint()
        elif args.command == "test":
            test()
        elif args.command == "clean":
            clean()
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
