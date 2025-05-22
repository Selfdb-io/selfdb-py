from setuptools import setup, find_packages

setup(
    name="selfdb",
    version="0.1.0",
    description="Python client library for SelfDB",
    author="SelfDB Contributors",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.6",
)