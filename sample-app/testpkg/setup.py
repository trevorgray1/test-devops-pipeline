from setuptools import setup, find_packages

setup(
    name="testpkg",
    version="0.1.0",
    description="A test Python package for Cloudsmith upload.",
    author="trevorgray1",
    packages=find_packages(),
    python_requires='>=3.6',
)
