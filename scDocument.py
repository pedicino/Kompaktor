import subprocess
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

gswin64cpath = resource_path('gswin64c.exe')

def compressPDF(desiredComp, inputPath, outputPath):

    subprocess.run(gswin64cpath + ' -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
        -dPDFSETTINGS=/screen -dEmbedAllFonts=true -dSubsetFonts=true -dColorImageDownsampleType=/Bicubic \
        -dColorImageResolution='+str(desiredComp)+' -dGrayImageDownsampleType=/Bicubic \
        -dGrayImageResolution='+str(desiredComp)+' -dMonoImageDownsampleType=/Bicubic \
        -dMonoImageResolution='+str(desiredComp)+' -sOutputFile='+outputPath+' '+inputPath)