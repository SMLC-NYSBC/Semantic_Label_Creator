"""

	Class module to load 3D .tif file

	:param str src_tif: source of the 3D .tif file
	:param str src_am: source of the spatial graph for corresponding 3D .tif

	Done: Collect information about input et (image_size, file_name)
	Done: Build empty .tif file for semantic labels
	TODO: Load ASCI .am file with 3D coordinates
	TODO: for loop -> for each MT spline -> Define position of spline, build cylinder around it 25 nm -> add 1 to a matrix
		the area with a cylinder
	TODO: save it in the indicated location

	:author Robert Kiewisz
	
"""
import numpy as np
from skimage import io


class SemanticLabelFromAmira:
	def __init__(self, src_tiff, src_am, pixel_size=None):
		self.src_tiff = src_tiff
		self.src_am = src_am
		self.pixel_size = pixel_size
		
		self.image = io.imread(self.src_tiff)
		self.spatial_graph = open(
			src_am,
			"r",
			encoding="iso-8859-1"
		).read().split("\n")
		
	def semantic_label(self):
		return np.zeros(self.image.shape)
	
	def read_tiff_transformation(self):
		# This method read the header of ET (.am) file and determines global
		# transformation for all coordinates
		
		et = open(
			self.src_tiff[:-3] + "am",
			"r",
			encoding="iso-8859-1"
		)
		
		lines_in_et = et.read().split("\n")
		transformation_list = str([
			word for word in lines_in_et if word.startswith('    BoundingBox')
		]).split(" ")
		
		trans_x, trans_y, trans_z = float(transformation_list[5]), \
		                            float(transformation_list[7]), \
		                            float(transformation_list[9])
		return trans_x, trans_y, trans_z
	
	def find_segments(self):
		# Find line define VERTEX ... <- number indicate number of segments
		# Find line starting with EDGE { int NumEdgePoints }
		# Find in the line directory that starts with @..
		# Find line that start with the directory @.. and select last one
		# Select all lines between @.. (-1) and number of segments
		# return an array of number of points belonged to each segment
		segment_at = str([
			word for word in self.spatial_graph if word.startswith('POINT { float[3] EdgePointCoordinates }')
		])
		segment_at = "".join((ch if ch in "0123456789" else " ") for ch in segment_at)
		segment_at = [int(i) for i in segment_at.split()]
		segment_at = self.spatial_graph.index("@" + str(segment_at[1])) + 1
		
		
		return "empty"
	
	def find_points(self):
		# Find line define POINT ... <- number indicate number of points
		# Find line starting with POINT { float[3] EdgePointCoordinates }
		# Find in the line directory that starts with @..
		# Find line that start with the directory @.. and select last one
		# Select all lines between @.. (-1) and number of points
		# return an array of all points coordinates in pixel
		
		return "empty"
	
	def pixel_size_in_et(self):
		if self.pixel_size is None:
			# Get max value from Z coordinates after transformation, and
			# divided by self.image[1]
			
			return pixel_size
		else:
			return self.pixel_size
