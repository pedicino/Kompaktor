import scVideo
import scImage
import scDocument
from tkinter.constants import CENTER
import PySimpleGUI as sg
import os.path
import os
import sys
from PIL import Image, ImageTk

class scMain:
    sg.theme('DarkGrey8')

left_side = [
    [
        sg.Text("File Type:   "),
        sg.Combo(
            ['.PNG/.JPEG/.JPG','.MP4','.PDF'], size=(15,10), key='-FILETYPES-'
        )
    ],
    [
        sg.Text("Import File: "),
        sg.In(size=(24,1), enable_events=True, key="-BROWSER-"),
        sg.FileBrowse()
    ],
    [
        sg.Text("Destination:"),
        sg.In(size=(24,1), enable_events=True, key="-DESTINATION-"),
        sg.FolderBrowse()
    ],
    [
        sg.Text("Compression Amount:")
    ],
    [
        sg.Radio("Low", "radio_group_1", default=False, enable_events=True, key="-LOW-")
    ],
    [
        sg.Radio("Medium", "radio_group_1", default=False, enable_events=True, key="-MEDIUM-")
    ],
    [
        sg.Radio("High", "radio_group_1", default=False, enable_events=True, key="-HIGH-")
    ],
     [
        sg.Radio("Custom", "radio_group_1", default=False, enable_events=True, key="-CUSTOM-")
    ],
    [
       sg.Slider(range = (0, 100), disabled=True, visible=False, orientation = 'h', key="-SLIDER-")
    ],
     [
        sg.Text("Delete Original File?")
    ],
     [
        sg.Radio("Yes", "radio_group_2", default=False, key="-YESDELETE-")
    ],
    [
        sg.Radio("No", "radio_group_2", default=False, key="-NODELETE-")
    ],
]

mediaframe_layout = [
    [sg.Image(key="-IMAGE-", size=(300,200), expand_x=False, expand_y=False)]
]

right_side = [
    [sg.Frame(title='Media Preview', layout = mediaframe_layout, size=(300,200), expand_x= False, expand_y = False, element_justification='center')],
    [sg.Text("Status: Not Started", enable_events=True,size=(30,3), justification='center',key="-STATUSTEXT-")],
    [sg.Button('Compress',key="-COMPRESSBUTTON-")]
]

layout = [
    [
    sg.Column(left_side),
    sg.VSeperator(),
    sg.Column(right_side,element_justification='center')
    ]
]

window = sg.Window('SimpleCompress 1.0.0-beta', layout)

def loadImage():
    previewImage = Image.open(importedMediaPath)
    previewImage.thumbnail((300, 200))
    photo_img = ImageTk.PhotoImage(previewImage)
    window["-IMAGE-"].update(data=photo_img)

def getCompAmt():
    # Low, Medium, and High COMPRESSION 
    # MP4s - Higher the value, the more compressed
    # PNGs/JPGs - Higher the value, the more quality is preserved
    # PDFs - Higher the value, the more quality is preserved
    if(values["-LOW-"] == True):
        if selected_file_type == '.MP4': return str(10)
        if selected_file_type == '.PNG/.JPEG/.JPG': return 90
        if selected_file_type == '.PDF': return 256
    elif(values["-MEDIUM-"] == True):
        if selected_file_type == '.MP4': return str(20)
        if selected_file_type == '.PNG/.JPEG/.JPG': return 60
        if selected_file_type == '.PDF': return 144
    elif(values["-HIGH-"] == True):
        if selected_file_type == '.MP4': return str(50)
        if selected_file_type == '.PNG/.JPEG/.JPG': return 30
        if selected_file_type == '.PDF': return 64
    elif(values["-CUSTOM-"] == True):
        sliderVal = values["-SLIDER-"]
        if selected_file_type == '.MP4': return str(sliderVal)
        if selected_file_type == '.PNG/.JPEG/.JPG': return (100 - sliderVal + 5)
        if selected_file_type == '.PDF': return (300 - 2.7 * sliderVal)
    else:
        return "Error"


def showProcessing():
    window['-STATUSTEXT-'].update("Status: Processing...")
    window['-STATUSTEXT-'].update(text_color='yellow')
    window.refresh()

def showDone():
    window['-STATUSTEXT-'].update("Status: Done!")
    window['-STATUSTEXT-'].update(text_color='green')
    window.refresh()

def checkDelete():
    if(values["-YESDELETE-"] == True):
        if os.path.exists(ipath_raw):
            os.remove(ipath_raw)
        else:
            print("The file does not exist")


def checkDelete():
    if(values["-YESDELETE-"] == True):
        if os.path.exists(ipath_raw):
            os.remove(ipath_raw)
        else:
            print("The file does not exist")


while True:

    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    elif event == "-LOW-" or event == "MEDIUM" or event == "-HIGH-":
        window['-SLIDER-'].update(disabled=True, visible=False)

    elif event == "-CUSTOM-":
        window['-SLIDER-'].update(disabled=False, visible=True)

    elif event == "-COMPRESSBUTTON-":

        #Obtains desired file type from Combo
        selected_file_type = values['-FILETYPES-']

        #Obtains the full input path to the file, no quotes
        ipath_raw = values['-BROWSER-']

        #Adds quotes to full file input path, for ffmpeg usage
        ipath_file_q = '"' + values['-BROWSER-'] + '"'

        #Retrieves the chosen output path
        opath_raw = values['-DESTINATION-']

        #Adds quotes to output path
        opath_file_q = '"' + values['-DESTINATION-'] + '"'

        #Retrieve the filename, with extension (file.ext)
        og_fn_has_extension = os.path.basename(ipath_raw)

        #Retrieve the filename with the extension removed (file)
        og_fn_no_extension = os.path.splitext(og_fn_has_extension)[0]

        #Retrieve the extension to use it as a variable (.ext)
        fn_ext = os.path.splitext(og_fn_has_extension)[1]
        
        #Turns file into simplecompressed_ext
        new_fn_has_extension = og_fn_no_extension + '_s-compress'+fn_ext

        new_fn_no_extension = og_fn_no_extension + '_s-compress'

        # #Correct output path, with quotes and filename for ffmpeg 
        c_opath_q = '"' + opath_raw + '/' + new_fn_has_extension + '"'
        # Output path no quotes
        c_opath_no_q = opath_raw + '/' + new_fn_has_extension

        if(os.path.exists(c_opath_no_q)):
            print("Path exists!")
            c_opath_q = '"' + opath_raw + '/' + new_fn_no_extension + '_new' + fn_ext + '"'
            c_opath_no_q = opath_raw + '/' + new_fn_has_extension + '_new' + fn_ext
        else:
            print("Couldn't find path.")
            c_opath_q = '"' + opath_raw + '/' + new_fn_has_extension + '"'
            c_opath_no_q = opath_raw + '/' + new_fn_has_extension

           
        def detectFileType(fileType):
            match fileType:
                case '.MP4':
                    scVideo.compressMP4(getCompAmt(), ipath_file_q, c_opath_q)
                case '.PNG/.JPEG/.JPG':
                    scImage.compressImg(getCompAmt(), ipath_raw, c_opath_no_q)
                case '.PDF':
                    scDocument.compressPDF(getCompAmt(), ipath_file_q, c_opath_q)

        showProcessing()
        detectFileType(selected_file_type)
        checkDelete()
        showDone()

        
    elif event == "-BROWSER-": 
        try:
            window["-IMAGE-"].update(visible=False)
            importedMediaPath = values["-BROWSER-"]
            loadImage()
            window["-IMAGE-"].update(visible=True)

        except:
            pass


window.close()