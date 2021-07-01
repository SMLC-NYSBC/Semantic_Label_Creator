#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['click>=7.0', ]

test_requirements = []

setup(
    author="Robert Kiewisz",
    author_email='robert.kiewisz@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python package to decode Amira 3D coordinate spatial graphs into semantic label mask",
    entry_points={
        'console_scripts': [
            'slcpy=slcpy.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='slcpy',
    name='slcpy',
    packages=find_packages(include=['slcpy', 'slcpy.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/RRobert92/Semantic_Label_Creator',
    version='0.1.0',
    zip_safe=False,
)
