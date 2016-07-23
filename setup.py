from distutils.core import setup
import py2exe

Mydata_files = [('images', ['images/crosshair.png'])]

setup(
    windows = [
        {
            "script": "ghostmidi.py",                    ### Main Python script        
        }       
    ],
    data_files = Mydata_files,
    options = {'py2exe': {
		"bundle_files": 2, # This tells py2exe to bundle everything
	}},
	zipfile = None,
) 