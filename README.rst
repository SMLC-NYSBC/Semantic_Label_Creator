================================
Semantic Label Converter [slcpy]
================================

.. image:: https://img.shields.io/github/v/release/SMLC-NYSBC/Semantic_Label_Creator
        :target: https://img.shields.io/github/v/release/SMLC-NYSBC/Semantic_Label_Creator

.. image:: https://github.com/SMLC-NYSBC/Semantic_Label_Creator/actions/workflows/python-publish_PyPi.yml/badge.svg
        :target: https://github.com/SMLC-NYSBC/Semantic_Label_Creator/actions/workflows/python-publish_PyPi.yml

.. image:: https://readthedocs.org/projects/semantic-label-creator/badge/?version=latest
        :target: https://semantic-label-creator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

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
* Cut and stitch images/masks withe predefined settings
* Convert semantic label mask to 3D point cloud


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

    $ git clone git://github.com/SMLC-NYSBC/Semantic_Label_Creator
    $ python setup.py install

or install is with pip:

.. code-block:: console

    $ pip install slcpy


.. _Github repo: https://github.com/SMLC-NYSBC/Semantic_Label_Creator
.. _tarball: https://github.com/SMLC-NYSBC/Semantic_Label_Creator/tarball/master

=====
Usage
=====

To use Semantic_Label_Creator in a project::

    from slcpy.main import slcpy
    _, label_mask = slcpy_semantic(dir_path,
                                   mask=Ture,
                                   pixel_size=None, 
                                   circle_size=250,
                                   multi_layer=True, 
                                   trim_mask=False, 
                                   trim_size=64)
                                   
    point_could = slcpy_graph(dir_path=label_mask,
                              filter_img=5,
                              down_sampling=Ture)

or with terminal to build semantic label::

    slcpy_semantic -dir C:/... -o C:/.../output 

 string [-dir] Directory of the folder that contain data.
    [-default] os.getcwd() + r'\data'
 string [-o]   Output directory to the folder where all of converted filed are stored.
    [-default] os.getcwd() + r'\data' + r'\output'
 bool   [-m]   Indicate if mask is included.
    [-default] True
 float  [-px]  Images pixel size in Angstrom. If None pixel size is calculated from image metadata
    [-default] None
 int    [-d]   Diameter in Angstrom of a circle that would be drawn a semantic mask
    [-default] 250
 bool   [-l]   Specified if lines should have independent labeling
    [-default] False
 bool   [-t]   Specified if the input image has to be trim to fit labels.
    [-default] True
 int    [-xy]  Define size in pixels of output images.
    [-default] 64
 int    [-z]  Define size in pixels of output images.
    [-default] 64
 bool   [-f]  If True only images containing any data are saved.
    [-default] True
 int    [-s]  Overlay size used for trimming images.
    [-default] 25

with terminal to stitch images::

    slcpy_stitch -dir C:/... -o C:/.../output -m True -pf mask -b True
 string [-dir] Directory of the folder that contain data.
    [-default] os.getcwd() + r'\data'
 string [-o]   Output directory to the folder where all of converted filed are stored.
    [-default] os.getcwd() + r'\data' + r'\output'
 bool   [-m]   If True output images are treated as mask not images.
    [-default] True
 string [-pf]  Additional prefix name for each image.
    [-default] None
 bool   [-b]   If True output stitched image as binary mask.
    [-default] True
 string [-dt]   Output numpy data type.
    [-default] int8

with terminal to build point cloud from image::

    slcpy_graph -dir C:/... -o C:/.../output -f 6 -c 3 -s cvs 
 string [-dir] Directory of the folder that contain data.
    [-default] os.getcwd() + r'\data'
 string [-o]   Output directory to the folder where all of converted filed are stored.
    [-default] os.getcwd() + r'\data' + r'\output'
 int    [-f]   Filter size matrix for denoising.
    [-default] 6
 bool   [-d]   Down-sample point cloud by the factor of.
    [-default] True
 string [-s]   Define format of output point cloud.
    [-default] all
    [-option] all, csv, numpy
