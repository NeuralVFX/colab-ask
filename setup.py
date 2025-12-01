from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="colab-ask",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["lisette", "mistune", "pillow", "litellm"],
    author="NeuralVFX",
    description="LLM assistant magic for Colab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeuralVFX/colab-ask",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)