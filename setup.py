from setuptools import setup, find_packages
import pathlib

# Robust way to read README (handles paths correctly on all OS)
HERE = pathlib.Path(__file__).parent
long_description = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="colab-ask",
    version="0.1.4",
    description="An LLM assistant magic command for Google Colab notebooks.", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeuralVFX/colab-ask",
    author="NeuralVFX",
    license="MIT",
    
    # Auto-find packages (looks for __init__.py)
    packages=find_packages(),
    
    # Dependencies
    install_requires=[
        "lisette",   
        "mistune",  
        "pillow", 
        "litellm",   
        "ipython", 
    ],

    # 3. Classifiers 
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: IPython",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12", 
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    
    python_requires=">=3.10",
)
