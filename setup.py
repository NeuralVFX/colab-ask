from setuptools import setup, find_packages

setup(
    name="colab-ask",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["lisette", "mistune", "pillow", "litellm"],
    author="NeuralVFX",
    description="LLM assistant magic for Colab",
)