import os

def f_Loop(aFolderListItem, template_file_name):
    aFolderItemDir = ''
    item = ''
    fName = os.path.splitext(os.path.split(aFolderListItem)[1])[0]
    names = []

    if not os.path.isfile(aFolderListItem):
        aFolderItems = os.listdir(aFolderListItem) 
        for item in aFolderItems:
            aFolderItemDir = os.path.join(aFolderListItem, item)
            if os.path.isdir(aFolderItemDir):
                print ("Folder dir: %s in %s"% (aFolderItemDir, aFolderListItem))
                #f_Loop(aFolderItemDir,template_file_name) # recursion commented to list just top folder files
            else:
                if aFolderItemDir.lower().endswith(('.nef')):
                    print ("File %s will be parsed under : %s directory"% (aFolderItemDir, fName))
                    names.append(os.path.split(aFolderItemDir)[1].upper().replace('.NEF','.txt'))
                    #parse_file(template_file_name,aFolderItemDir) #removed to just generate txt filenames list 
    return names
                             

def parse_file(template_file_name,nef_file_name):
    output_file_name = os.path.split(nef_file_name)[1].upper().replace('.NEF','.txt') #you can add subfolder for new files here
    with open(template_file_name) as f:
        with open(output_file_name, 'a') as o:
            lines = f.readlines()
            for line in lines:
                if line.rstrip().lower().endswith('.nef'):
                    new_line = line[:line.rfind('\\',0,len(line))+1]+output_file_name+line[line.upper().rfind('.NEF',0,len(line))+4:]
                    print (new_line)
                    o.write(new_line)
                else:
                    o.write(line)

def generate_files(file_names_list, template_file_name):
    with open(template_file_name) as f:
        lines = f.readlines()
        f.close()
    for file in file_names_list:
        with open(file, 'a') as o:
            for line in lines:
                if line.rstrip().lower().endswith('.nef'):
                        new_line = line[:line.rfind('\\',0,len(line))+1]+file+line[line.upper().rfind('.NEF',0,len(line))+4:]
                        o.write(new_line)
                else:
                    o.write(line)
        


def main():
    # get current directory path
    current_dir =  os.path.abspath(os.getcwd())
    #start loop under path
    names = f_Loop(current_dir+'/1sza noc','template.txt')
   # print(names)
    generate_files(names,'template.txt')
if __name__ == '__main__':
	main()