from setuptools import setup, find_packages

setup(
    name="factotum",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[
        "click==8.3.0",
        "openai==2.2.0",
        "pyperclip==1.9.0",
        "pydantic==2.10.6",
        "rich==14.2.0",
    ],
    entry_points={
        "console_scripts": [
            "fac=src.cli:main",
        ],
    },
    python_requires=">=3.10",
)
