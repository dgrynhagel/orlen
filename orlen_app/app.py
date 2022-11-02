import PySimpleGUI as sg
import os
import scripts.generate_nef_txt as g

def main():
    sg.theme('Topanga')
    current_dir =  os.path.abspath(os.getcwd())
    SEC1_KEY = '-SECTION1-'
    SEC2_KEY = '-SECTION2-'
    fitsfolder = [[sg.Text('Your FITS Folder', size=(15, 1), justification='right'),
            sg.InputText('...FITS folder...', key='fits_folder'), sg.FolderBrowse(initial_folder=current_dir)],
            [sg.Button('Bulk Generate')]]

    singlefile = [[sg.Text('Browse for FITS file:', size=(15, 1), justification='right'),
            sg.InputText('', key='fits_file'), sg.FileBrowse(initial_folder=current_dir, file_types=(("FITS files", "*.fits"),))],
            [sg.Button('Generate one')]
            ]
    left_list = [
        [sg.MLine(default_text='', size=(35, 10), key='filenamelist')]
    ]
    right_list = [
        [sg.Text("Choose file extension for edit", font = ("Arial", 14))]
    ]
    layout = [
        [sg.Text("Welcome in Orlen app tools set ", font = ("Arial", 24))],
        [sg.Text('_' * 80)],
        [sg.Text("Create txt files for each NEF", font = ("Arial", 18))],
        [sg.Text('Your NEF Folder', size=(15, 1), justification='right'),
            sg.InputText('...NEF folder...', key='nef_folder'), sg.FolderBrowse(initial_folder=current_dir)],
        [sg.Button('List')],    
        [sg.Column(left_list, expand_x=True, expand_y=True, key='left'),
        sg.VSeperator(),
        sg.Column(right_list, expand_x=True, expand_y=True, key='right_column'),
        ],
        [sg.Text('Your TXT Folder', size=(15, 1), justification='right'),
            sg.InputText('...TXT folder...', key='txt_folder'), sg.FolderBrowse(initial_folder=current_dir)],
        [sg.Text('Template file:', size=(15, 1), justification='right'),
            sg.InputText('', key='txt_file'), sg.FileBrowse(initial_folder=current_dir, file_types=(("TXT files", "*.txt"),))],
        [sg.Button('Generate')],  
        [sg.Text('_' * 80)],
        [sg.Text("Add tag to FITS file", font = ("Arial", 18))],
        [sg.Text('Tag name:',  justification='left'), sg.Input("ORLEN", key='tagname')],
        [sg.Text('Your FITS Folder', size=(15, 1), justification='right'),
            sg.InputText('...FITS folder...', key='fits_folder'), sg.FolderBrowse(initial_folder=current_dir)],
        [sg.Button('Bulk Generate')],
        [sg.Text('_' * 80)],
        [sg.Button('Close')]
    ]
    
    window = sg.Window('Orlen app', layout, finalize=True,resizable=True)

    while True:
        event,values = window.read()
        print(event, values)
        if event == 'Close' or sg.WIN_CLOSED:
            break
        if event == 'List':
            fo = values['nef_folder']
            output_list = g.f_Loop(fo)[0]
            file_type_list = g.f_Loop(fo)[1]
            print(g.f_Loop(fo)[1])
            for file in output_list:
                window['filenamelist'].print(file)  
            new_items = [[sg.Checkbox(f"{item[1].upper()}", key=('-FILE-',item[1].upper()), default=True)] for item in enumerate(file_type_list)]
            window.extend_layout(window['right_column'], new_items)
            window.refresh()

        if event == 'Generate':
            filetype_choice = []
            for k in values.keys():
                if k[0] == '-FILE-' and values[k]:
                    filetype_choice.append(k[1])

            print(filetype_choice)
            fo = values['nef_folder']
            output_list = g.f_Loop(fo)
            template = values['txt_file']
            output_dir = values['txt_folder']
            g.generate_files(output_list,template,output_dir,filetype_choice)
         #   try:
         #       g.generate_files(output_list,template,output_dir,filetype_choice)
         #       sg.Popup('Txt files generated successfully.')
         #   except Exception:
         #       sg.Popup('Failed to generate files.')
        if  event in file_type_list:
            sg.Popup('Jeb!')
            
        
        elif event in ('Exit', None):
            break

    window.close()


if __name__ == '__main__':
    main()