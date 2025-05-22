from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
    name="selfdb",
    version="0.1.0",
    description="Python client library for SelfDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rodgers",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.6",
)