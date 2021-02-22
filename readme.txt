How to use:
0) Install opencv-python pillow numpy piexif packages with pip
["pip install opencv-python pillow numpy piexif packages with pip" or "pip install --user opencv-python pillow numpy piexif packages with pip"]
1) Take a completely black and then white photo
2) Move this files to ./_detect/ directory
3) Run script with "detect" parameter in your favorite terminal (ex. "python.exe .\__main__.py detect" (this may take five minutes, wait)
4) Move photos to be processed to ./_input/ directory
5) Run script with "fix" parameter
6) Processed files will be appear in ./_output/ directory


//"detect" parameters
[default: disabled] --highlight = create duplicate files from ./_detect/ directory with highlighting bad pixels ("python.exe .\__main__.py detect --highlight")
[default: 10] --threshold <N> = threshold for marking a pixel as bad (N in [0; 255]. recommended 7-15) ("python.exe .\__main__.py detect --threshold 10")

//"fix" parameters
[default: disabled] --replace = replace files in ./_input/ directory, don't copy to ./_output/
[default: TELEA] --algorithm <NS|TELEA> = algorithm selection for photos inpainting (NS or TELEA. recommended TELEA) ("python.exe .\__main__.py detect --algorithm NS")

//"emulation"
you can emulate bad pixels after generating hotpixels map (photos will be taken from ./_input/ directory, hotpixels map will be taken from ./_detect/ and "spoiled" photos will be moved to ./emulated/)
