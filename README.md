# Resolution_Change
A code that scales the resolution of a fits image by a specified factor.
The code uses a trick where the same image is opened twice and the header 
of the second image is modified. The reproject_interp function then reprojects
the first image onto the second modified header.

If the header specifications are different for your image, change that 
part of the code.

The user defines the scale of the resolution shift. The code was tested
primarily for downgrading resolution. In this case the "interpolation order"
was shown to be irrelevant.

The folder where the code is located should contain an "Input", "Output" and
"log" folders. Within the "Input" folder there should be a "Galaxy_Images_VLA"
folder (the name can be modified in the code) in which there should be a separate
folder for each image. 
