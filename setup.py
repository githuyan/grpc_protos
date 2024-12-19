from setuptools import find_packages, setup

setup(
    name="grpc-protos",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "grpcio",
        "protobuf",
    ],
    python_requires=">=3.7",
)
