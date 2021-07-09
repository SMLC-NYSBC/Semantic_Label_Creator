#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from slcpy.version import version

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['click==8.0.1',
                'setuptools==57.1.0',
                'scikit-image==0.18.2',
                'numpy==1.21.0',
                'tifffile==2021.7.2',
                'tqdm == 4.61.1',
                'imagecodecs == 2021.6.8',
                ]

test_requirements = []

setup(
    author="Robert Kiewisz",
    author_email='robert.kiewisz@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
    long_description_content_type='text/x-rst',
    long_description=readme,
    include_package_data=True,
    keywords='slcpy',
    name='slcpy',
    packages=find_packages(include=['slcpy', 'slcpy.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/RRobert92/Semantic_Label_Creator',
    version=version,
    zip_safe=False,
)
