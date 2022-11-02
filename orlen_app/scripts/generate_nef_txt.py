import os
from pathlib import Path

def f_Loop(aFolderListItem):
    aFolderItemDir = ''
    item = ''
    fName = os.path.splitext(os.path.split(aFolderListItem)[1])[0]
    names = []
    fileTypes = []

    if not os.path.isfile(aFolderListItem):
        aFolderItems = os.listdir(aFolderListItem) 
        for item in aFolderItems:
            aFolderItemDir = os.path.join(aFolderListItem, item)
            if os.path.isdir(aFolderItemDir):
                print ("Folder dir: %s in %s"% (aFolderItemDir, aFolderListItem))
                #f_Loop(aFolderItemDir,template_file_name) # recursion commented to list just top folder files
            else:
               # if aFolderItemDir.lower().endswith(('.nef')):
                print ("File %s will be parsed under : %s directory"% (aFolderItemDir, fName))
                names.append(os.path.split(aFolderItemDir)[1].upper())
                if aFolderItemDir.split('.')[-1] not in fileTypes:
                    fileTypes.append(aFolderItemDir.split('.')[-1])
                    #parse_file(template_file_name,aFolderItemDir) #removed to just generate txt filenames list 
    return names, fileTypes                           

def parse_file(template_file_name,nef_file_name):
    output_file_name = os.path.split(nef_file_name)[1].upper().replace('.NEF','.txt') #you can add subfolder for new files here
    with open(template_file_name) as f:
        with open(output_file_name, 'a') as o:
            lines = f.readlines()
            for line in lines:
                if line.rstrip().lower().endswith('.nef'):
                    new_line = line[:line.rfind('\\',0,len(line))+1]+output_file_name+line[line.upper().rfind('.NEF',0,len(line))+4:]
                    o.write(new_line)
                else:
                    o.write(line)

def generate_files(file_names_list, template_file_name,out_folder,file_types_list):
    with open(template_file_name) as f:
        lines = f.readlines()
        f.close()
    for file in file_names_list[0]:
        #check file extension and compare with file_type_list
        file_extension = file.rsplit('.',1)[1]
        print(file_extension)
        if file_extension.upper() in file_types_list:
            with open(os.path.join(out_folder,file.replace(file_extension,'txt')), 'a') as o:
                for line in lines:
                    if line.rstrip().upper().endswith(file_extension):
                            new_line = line[:line.rfind('\\',0,len(line))+1]+file+line[line.upper().rfind(file_extension,0,len(line))+4:]
                            o.write(new_line)
                    else:
                        o.write(line)
