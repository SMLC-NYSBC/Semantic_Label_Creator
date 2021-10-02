================================
Semantic Label Converter [slcpy]
================================

.. image:: https://img.shields.io/github/v/release/RRobert92/Semantic_Label_Creator
        :target: https://img.shields.io/github/v/release/RRobert92/Semantic_Label_Creator

.. image:: https://github.com/RRobert92/Semantic_Label_Creator/actions/workflows/python-publish_PyPi.yml/badge.svg
        :target: https://github.com/RRobert92/Semantic_Label_Creator/actions/workflows/python-publish_PyPi.yml

.. image:: https://readthedocs.org/projects/semantic-label-creator/badge/?version=latest
        :target: https://semantic-label-creator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://www.codefactor.io/repository/github/rrobert92/semantic_label_creator/badge
        :target: https://img.shields.io/github/v/release/RRobert92

Python package for converting segmented point cloud to trimmed semantic label masks
as well as converting unsegmented semantic labels into a general point cloud.
The point cloud to semantic conversion is achieved by drawing a circle with fixed diameter
along the line given as points. Additionally the image dataset can be trimmed with or
without padding to indicated size. The semantic to point cloud conversion is done before or
after stitching of images (with or without padding) by selecting at each Z position
all points maxima's and saving their 3D coordinates in array.

* Documentation: https://semantic-label-creator.readthedocs.io/en/latest/

Features
--------
* Convert 3D point cloud from (.am) files to semantic label mask
* Convert semantic label mask to 3D point cloud

ToDo
--------
* Cut label mask with padding
* Convert semantic label mask to point cloud

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
    $ python setup.py install

or install is with pip:

.. code-block:: console

    $ pip install slcpy


.. _Github repo: https://github.com/RRobert92/Semantic_Label_Creator
.. _tarball: https://github.com/RRobert92/Semantic_Label_Creator/tarball/master

=====
Usage
=====

To use Semantic_Label_Creator in a project::

    from slcpy.main import slcpy
    label_mask = slcpy(dir_path,
                       pixel_size=None, circle_size=250,
                       multi_layer=True, trim_mask=True, trim_size=256)

    point_could = slcpy_graph(dir_path)

or with terminal::

    slcpy_semantic -dir C:/... -o C:/.../output -px None -d 250 -l True -t True -xy 256
    slcpy_graph -dir C:/... -o C:/.../output

 string [-dir] directory of the folder that contain data.
    [-default] os.getcwd() + r'\data'
 string [-o] output directory to the folder where all of converted filed are stored.
    [-default] os.getcwd() + r'\data' + r'\output'
 int [-px] anisotropic images pixel size in Angstrom.
    [-default] None  [-type] int
 int [-d] diameter in Angstrom of a circle that would be drawn a semantic mask
    [-default] 250
 int [-l] specified if lines should have independent labeling
    [-default] False
 int [-t] specified if the input image has to be trim to fit labels.
    [-default] True
 int [-xy] define size in pixels of output images.
    [-default] None [-type] int


Credits
-------
This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
