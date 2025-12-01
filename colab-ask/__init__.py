# colab_ask/__init__.py
from .magic import load_ipython_extension

# This exposes the function to %load_ext colab_ask
__all__ = ['load_ipython_extension']
