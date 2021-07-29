==============================
Semantic Label Creator [slcpy]
==============================

.. image:: https://img.shields.io/github/v/release/RRobert92/Semantic_Label_Creator
        :target: https://img.shields.io/github/v/release/RRobert92/Semantic_Label_Creator

.. image:: https://github.com/RRobert92/Semantic_Label_Creator/actions/workflows/python-publish_PyPi.yml/badge.svg
        :target: https://github.com/RRobert92/Semantic_Label_Creator/actions/workflows/python-publish_PyPi.yml

.. image:: https://readthedocs.org/projects/semantic-label-creator/badge/?version=latest
        :target: https://semantic-label-creator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://www.codefactor.io/repository/github/rrobert92/semantic_label_creator/badge
        :target: https://img.shields.io/github/v/release/RRobert92

Python package to decode Amira 3D coordinate spatial graphs into semantic label mask.

* Documentation: https://semantic-label-creator.readthedocs.io/en/latest/

Features
--------
* Load Amira spatial graph to transform 3D coordinates into semantic label mask

============
Installation
============


Stable release
--------------

To install Semantic_Label_Creator, run this command in your terminal:

.. code-block:: console

    $ pip install slcpy

This is the preferred method to install Semantic_Label_Creator, as it will always install the most recent stable release.

From sources
------------

The sources for Semantic_Label_Creator can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/RRobert92/Semantic_Label_Creator

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/RRobert92/Semantic_Label_Creator
.. _tarball: https://github.com/RRobert92/Semantic_Label_Creator/tarball/master

=====
Usage
=====

To use Semantic_Label_Creator in a project::

    from slcpy.main import slcpy
    label_mask = slcpy(dir_path, pixel_size=None, circle_size=250)

or with terminal::

    slcpy -dir -o -px -d

 string [-dir] directory of the folder that contain data.
    [-default] os.getcwd() + r'\data'
 string [-o] output directory to the folder where all of converted filed are stored.
    [-default] os.getcwd() + r'\data' + r'\output'
 int [-px] anisotropic images pixel size in Angstrom.
    [-default] None
 int [-d] diameter in Angstrom of a circle that would be drawn a semantic mask
    [-default] 250
 int [-l] specified if lines should have independent labeling
    [-default] False
 int [-t] specified if the input image has to be trim to fit labels.
    [-default] True
    
    
Credits
-------
This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
