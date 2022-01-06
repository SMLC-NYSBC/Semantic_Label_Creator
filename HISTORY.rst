=======
History
=======

0.3.5 (2022-01-03)
-------------------
* HotFix for folder selection on MacOS
* Bugfix in graph creation
* Fix patch creation in Z -> not cutting patches in Z for given size

0.3.4 (2021-11-28)
-------------------
* Added point downsamling 
* Bug fix for calculating patch size when z dimension was bigger then image size

0.3.3 (2021-11-28)
-------------------
* Quick changes for 0.3.3 for build graph tool.
  * Added image output after denoising as an option

0.3.3 (2021-11-28)
-------------------
* Added check for spindletorch to select dtype of output from
  slcpy_stitch
  
0.3.2 (2021-11-19)
-------------------
* Bugfixes for version 0.3.1
* Small update to adapt slcpy to spindletorch and ML packages

0.3.1 (2021-10-31)
-------------------
* Maintained update

0.3.0 (2021-10-12)
-------------------
* Remove pixel size calculation interchange to extracting information from (.am) files
* Added module for extracting 3D coordinates for point cloud from semantic label mask
* Added trimming of whole image with stride to calculate overlaying area and
  number or patches in xyz
* Added module to stitch images into one images based on file names (e.g 1_1_1, where
  each number indicates xyz patch position

0.2.1 (2021-08-13)
-------------------
* Output data are now split to imgs and mask folder if -xy != None

0.2.0 (2021-08-13)
--------------------
* Added trimming of data for multiple images with specific size + recycling of empty labels

0.1.9 (2021-07-17)
-------------------
* Added trimming of input data to label mask size
* Added multiple labels

0.1.8 (2021-07-17)
-------------------
* Bugfix for drawing horizontal lines

0.1.7 (2021-07-09)
-------------------
* Maintenance update

0.1.6 (2021-07-07)
-------------------
* Bugfixes for version 0.1.0
* Setup PyPI and conda

0.1.0 (2021-06-30)
-------------------
* Standardized project entry with cookecutter
* Set up loading of standard data types *.tiff, *.am
* Transform Amira coordinates into pixel value
* Interpolate pixel coordinates and build semantic label
