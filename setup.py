from setuptools import setup

setup(
    name="reorg",
    version="0.1.0",
    license="MIT",
    author="Michael Hwang",
    description="Command-line to reorganize documents stored in CLB6 structure to..",
    packages=["reorg"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "reorg = reorg.cli:run"
            ]
        }
)
