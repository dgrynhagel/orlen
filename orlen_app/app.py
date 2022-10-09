import PySimpleGUI as sg
import os
import scripts.generate_nef_txt as g

def main():
    sg.theme('TanBlue')
    current_dir =  os.path.abspath(os.getcwd())
    layout = [
        [sg.Text("Welcome in Orlen app tools set ")],
        [sg.Text('_' * 80)],
        [sg.Text("This part will create txt files for each NEF")],
        [sg.Text('Your NEF Folder', size=(15, 1), justification='right'),
            sg.InputText('...NEF folder...', key='nef_folder'), sg.FolderBrowse(initial_folder=current_dir)],
        [sg.Button('List')],    
        [sg.MLine(default_text='', size=(35, 3), key='filenamelist')], 
        [sg.Text('Your TXT Folder', size=(15, 1), justification='right'),
            sg.InputText('...TXT folder...', key='txt_folder'), sg.FolderBrowse(initial_folder=current_dir)],
        [sg.Text('Template file:', size=(15, 1), justification='right'),
            sg.InputText('', key='txt_file'), sg.FileBrowse(initial_folder=current_dir, file_types=(("TXT files", "*.txt"),))],
        [sg.Button('Generate')],  
        [sg.Text('_' * 80)],
        [sg.Button('Close')]
    ]
    window = sg.Window('Orlen app', layout, finalize=True)

    while True:
        event,values = window.read()
        if event == 'Close' or sg.WIN_CLOSED:
            break
        if event == 'List':
            fo = values['nef_folder']
            output_list = g.f_Loop(fo)
            for file in output_list:
                window['filenamelist'].print(file)  
        if event == 'Generate':
            template = values['txt_file']
            output_dir = values['txt_folder']
            g.generate_files(output_list,template,output_dir)
        elif event in ('Exit', None):
            break

    window.close()


if __name__ == '__main__':
    main()