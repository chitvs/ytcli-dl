from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A minimal command-line YouTube downloader"

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ytcli-dl",
    version="1.0.0",
    author="Alessandro Chitarrini",
    license="MIT license",
    description="A minimal command-line YouTube downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chitvs/ytcli-dl",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ytcli-dl=ytcli_dl.cli:main",
        ],
    },
)