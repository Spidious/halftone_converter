# halftone_converter
Converts images into CMYK halftone dot images

HEIC currently not supported

Requires PIL to be installed :   python3 -m pip install --upgrade Pillow

Change these settings in IMAGE SETTINGS for easy final image alteration
INPUT_FILE -    (in quotations) the name of the original file to be imported
SIZE       -    the diameter of the maximum size of a circle (in pixels)
OVER       -    increases radius size, allows overlap (set to 0 to ignore)

Smaller Size creates higher definition. Smaller numbers will be slower, you may have to wait

Currently KEY (black) does not work I don't know why. The image returns empty

The text files generated can be ignored and deleted. They are meant for being used by other programs to read and decode.
CLEAR_TXT  -    text filees can be deleted by changing to True, kept by changing to False 
