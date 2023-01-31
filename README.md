# halftone_converter<br />
Converts images into CMYK halftone dot images<br />
<br />
HEIC not supported<br />
<br />
Requires PIL to be installed :   python3 -m pip install --upgrade Pillow<br />
<br />
Change these settings in IMAGE SETTINGS for easy final image alteration<br />
`INPUT_FILE` -    (in quotations) the name of the original file to be imported<br />
`SIZE`       -    the diameter of the maximum size of a circle (in pixels)<br />
`OVER`       -    increases radius size, allows overlap (set to 0 to ignore)<br />

Smaller `Size` creates higher definition. Smaller numbers will be slower, you may have to wait a moment depending on your computers processing power<br />
<br />
The text files generated can be ignored and deleted. They are meant for being used by other programs to read.<br />
CLEAR_TXT  -    text filees can be automatically deleted by changing to True, kept by changing to False <br />
