#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional

class ProtoGenerator:
    def __init__(self, source_dir: str = "protos", target_dir: str = "services"):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        # 遍历 source_dir 下的所有文件，排除 common 目录
        self.service_packages = [
            proto_file
            for proto_file in self.source_dir.rglob("*.proto")
            # if "common" not in proto_file.parts
        ]

    def clean_generated_files(self) -> None:
        """清理之前生成的文件"""
        for package in self.service_packages:
            target_package_dir = self.target_dir / package
            if target_package_dir.exists():
                # 只删除生成的pb2文件，保留其他文件
                for file in target_package_dir.glob("*pb2*"):
                    file.unlink()

    def generate(self) -> None:
        """生成proto代码"""
        self.clean_generated_files()

        # 遍历每个proto文件并生成相应的代码
        for proto_file in self.service_packages:
            proto_path = str(proto_file)
            target_package_dir = self.target_dir / proto_file.parent.relative_to(self.source_dir)
            
            # 确保目标目录存在
            target_package_dir.mkdir(parents=True, exist_ok=True)
            
            # 使用grpc_tools.protoc生成代码
            cmd = [
                "python3", "-m", "grpc_tools.protoc",
                f"--python_out={target_package_dir}",
                f"--grpc_python_out={target_package_dir}",
                f"--mypy_out={target_package_dir}",
                "--proto_path=.",
                f"--proto_path={self.source_dir}",
                proto_path
            ]
            print(" ".join(cmd), "-----")
            result = subprocess.run(cmd)


def main() -> None:
    parser = argparse.ArgumentParser(description="Proto代码生成工具")
    parser.add_argument(
        "--source-dir",
        default="protos",
        help="proto文件所在目录 (默认: protos)"
    )
    parser.add_argument(
        "--target-dir",
        default="services",
        help="生成代码的目标目录 (默认: services)"
    )

    args = parser.parse_args()
    generator = ProtoGenerator(args.source_dir, args.target_dir)
    generator.generate()

if __name__ == "__main__":
    main()