from setuptools import setup

setup(
    name="rearrange",
    version="0.1.0",
    license="MIT",
    author="Michael Hwang",
    description="Command-line to rearrange documents stored in CLB6 structure to..",
    packages=["rearrange"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "rearrange = rearrange.cli:run"
            ]
        }
)
