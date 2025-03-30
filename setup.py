from setuptools import setup, find_packages

setup(
    name="puml",
    version="0.1.0",
    author="Kaspar Mitte",
    description="extracts class charts from source code and draws uml charts",
    packages=find_packages(
        include=["puml", "puml.*", "src", "src.*", "example", "example.*"]
    ),
    install_requires=[]
)
