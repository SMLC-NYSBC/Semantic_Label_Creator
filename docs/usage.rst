.. highlight:: shell

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
