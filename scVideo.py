import subprocess
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

ffmpegpath = resource_path('ffmpeg.exe')

def compressMP4(desiredComp, inputPath, outputPath):
    subprocess.run(ffmpegpath + ' -i '+inputPath+' -vcodec libx264 -crf '+desiredComp+' '+outputPath)
