=======
History
=======
0.3.0 (2021-10-12)
-------------------
* Remove pixel size calculation interchange to extracting information from (.am) files
* Added module for extracting 3D coordinates for point cloud from semantic label mask
* Added trimming of whole image with stride to calculate overlaying area and
  number or patches in xyz
* Added module to stitch images into one images based on file names (e.g 1_1_1, where
  each number indicates xyz patch position

0.2.1 (2021-08-13)
------------------
* Output data are now split to imgs and mask folder if -xy != None

0.2.0 (2021-08-13)
------------------
* Added trimming of data for multiple images with specific size + recycling of empty labels

0.1.9 (2021-07-17)
------------------
* Added trimming of input data to label mask size
* Added multiple labels

0.1.8 (2021-07-17)
------------------
* Bugfix for drawing horizontal lines

0.1.7 (2021-07-09)
------------------
* Maintenance update

0.1.6 (2021-07-07)
------------------
* Bugfixes for version 0.1.0
* Setup PyPI and conda

0.1.0 (2021-06-30)
------------------
* Standardized project entry with cookecutter
* Set up loading of standard data types *.tiff, *.am
* Transform Amira coordinates into pixel value
* Interpolate pixel coordinates and build semantic label
