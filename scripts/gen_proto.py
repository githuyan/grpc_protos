#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path


class ProtoGenerator:
    """Proto文件代码生成器

    用于将.proto文件编译生成对应的Python代码，支持生成gRPC服务代码和消息类型代码。

    Attributes:
        source_dir: proto文件的源目录
        target_dir: 生成代码的目标目录
        common_protos: 存储common目录下的公共proto文件列表
        service_packages: 存储服务相关的proto文件列表
    """

    def __init__(self, source_dir: str = "protos", target_dir: str = "services"):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)

        # 遍历source_dir下的所有proto文件，区分common和service文件
        self.common_protos = []
        self.service_packages = []
        for proto_file in self.source_dir.rglob("*.proto"):
            if proto_file.is_file():
                # 将common目录下的proto文件归类为公共文件
                if "common" in proto_file.parts:
                    self.common_protos.append(proto_file)
                else:
                    self.service_packages.append(proto_file)

    def clean_target_dir(self) -> None:
        """清理目标目录

        删除并重新创建目标目录和__init__.py文件，确保每次生成代码时都是从干净的状态开始
        """
        if self.target_dir.exists():
            shutil.rmtree(self.target_dir)
        self.target_dir.mkdir(parents=True, exist_ok=True)
        (self.target_dir / "__init__.py").touch()

    def generate(self) -> None:
        """生成proto代码

        使用grpc_tools.protoc编译器将proto文件转换为Python代码：
        1. --python_out: 生成消息类型的Python代码
        2. --grpc_python_out: 生成gRPC服务的Python代码
        3. --mypy_out: 生成类型提示文件
        4. --proto_path: 指定proto文件的搜索路径
        """
        # 首先清理目标目录
        self.clean_target_dir()

        # 遍历每个服务相关的proto文件并生成代码
        for proto_file in self.service_packages:

            # 构建protoc命令并执行
            cmd = [
                "python3",
                "-m",
                "grpc_tools.protoc",
                f"--python_out={self.target_dir}",
                f"--grpc_python_out={self.target_dir}",
                f"--mypy_out={self.target_dir}",
                f"--proto_path={self.source_dir}",
                str(proto_file),
                # 添加所有common proto文件作为依赖
                *[str(common_proto) for common_proto in self.common_protos],
            ]
            subprocess.run(cmd)


def main() -> None:
    """主函数：解析命令行参数并执行代码生成"""
    parser = argparse.ArgumentParser(description="Proto代码生成工具")
    parser.add_argument(
        "--source-dir", default="protos", help="proto文件所在目录 (默认: protos)"
    )
    parser.add_argument(
        "--target-dir", default="services", help="生成代码的目标目录 (默认: services)"
    )

    args = parser.parse_args()
    generator = ProtoGenerator(args.source_dir, args.target_dir)
    generator.generate()


if __name__ == "__main__":
    main()
