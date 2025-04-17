import subprocess
from PIL import Image, ImageTk

def compressImg(desiredComp, inputPath, outputPath):

    importedImage = Image.open(inputPath)
    importedImage.save(outputPath, optimize=True, quality=desiredComp)