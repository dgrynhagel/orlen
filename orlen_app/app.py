import PySimpleGUI as sg
import os
import scripts.generate_nef_txt as g

def Collapsible(layout, key, title='', arrows=(sg.SYMBOL_DOWN, sg.SYMBOL_UP), collapsed=False):
    """
    User Defined Element
    A "collapsable section" element. Like a container element that can be collapsed and brought back
    :param layout:Tuple[List[sg.Element]]: The layout for the section
    :param key:Any: Key used to make this section visible / invisible
    :param title:str: Title to show next to arrow
    :param arrows:Tuple[str, str]: The strings to use to show the section is (Open, Closed).
    :param collapsed:bool: If True, then the section begins in a collapsed state
    :return:sg.Column: Column including the arrows, title and the layout that is pinned
    """
    return sg.Column([[sg.T((arrows[1] if collapsed else arrows[0]), enable_events=True, k=key+'-BUTTON-'),
                       sg.T(title, enable_events=True, key=key+'-TITLE-')],
                      [sg.pin(sg.Column(layout, key=key, visible=not collapsed, metadata=arrows))]], pad=(0,0))

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

    layout = [
        [sg.Text("Welcome in Orlen app tools set ", font = ("Arial", 24))],
        [sg.Text('_' * 80)],
        [sg.Text("Create txt files for each NEF", font = ("Arial", 18))],
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
        [sg.Text("Add tag to FITS file", font = ("Arial", 18))],
        [sg.Radio('Single file processing', "bulk", default=False, size=(20,1), k='single', enable_events=True, key='R1'), sg.Radio('Bulk action', "bulk", default=False, size=(20,1), k='bulk',enable_events=True, key='R1')],
        [sg.Text('Tag name:',  justification='left'), sg.Input("ORLEN", key='tagname')],
        [Collapsible(fitsfolder, SEC1_KEY,  '', ('+','-'),collapsed=True)],
        [Collapsible(singlefile, SEC2_KEY,  '',  ('+','-'),collapsed=True)],
        [sg.Text('_' * 80)],
        [sg.Button('Close')]
    ]
    
    window = sg.Window('Orlen app', layout, finalize=True)

    while True:
        event,values = window.read()
      #  print(event, values)
        if event == 'Close' or sg.WIN_CLOSED:
            break
        if event == 'List':
            fo = values['nef_folder']
            output_list = g.f_Loop(fo)
            for file in output_list:
                window['filenamelist'].print(file)  
        if event == 'Generate':
            fo = values['nef_folder']
            output_list = g.f_Loop(fo)
            template = values['txt_file']
            output_dir = values['txt_folder']
            try:
                g.generate_files(output_list,template,output_dir)
                sg.Popup('Txt files generated successfully.')
            except Exception:
                sg.Popup('Failed to generate files.')
        if event =='R12':
            window[SEC1_KEY].update(visible=not window[SEC1_KEY].visible)
            window[SEC1_KEY+'-BUTTON-'].update(window[SEC1_KEY].metadata[0] if window[SEC1_KEY].visible else window[SEC1_KEY].metadata[1])
        
        if event == 'R1':
            window[SEC2_KEY].update(visible=not window[SEC1_KEY].visible)
            window[SEC2_KEY+'-BUTTON-'].update(window[SEC2_KEY].metadata[0] if window[SEC2_KEY].visible else window[SEC2_KEY].metadata[1])
      
        elif event in ('Exit', None):
            break

    window.close()


if __name__ == '__main__':
    main()