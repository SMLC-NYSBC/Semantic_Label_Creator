from setuptools import setup, find_packages

name = "SLCpy"
version = "0.1"

description = "Semantic label generator from Amira file output"

author = "Robert Kiewisz"
author_email = "robert.kiewisz@gmail.com"

license = "GPLv3"

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    license=license,

    packages=find_packages(),
    install_requires=[
        "numpy"
    ],
    python_requires=">=3.8",
)
