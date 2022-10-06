from astropy.io import fits
import os


def f_Loop(aFolderListItem,HeaderTagName):
    aFolderItemDir = ''
    item = ''
    fName1 = os.path.split(aFolderListItem)[1]
    fName = os.path.splitext(fName1)[0]

    if not os.path.isfile(aFolderListItem):
        aFolderItems = os.listdir(aFolderListItem) 
        for item in aFolderItems:
            aFolderItemDir = os.path.join(aFolderListItem, item)
            if os.path.isdir(aFolderItemDir):
                print ("Folder dir: %s in %s"% (aFolderItemDir, aFolderListItem))
                f_Loop(aFolderItemDir,HeaderTagName) # recursion 
            else:
                if aFolderItemDir.lower().endswith(('.fits')):
                    print ("File %s will get tag: %s"% (aFolderItemDir, fName))
                    add_header(aFolderItemDir, HeaderTagName, fName)               

def f_MainLoop(rootDir,HeaderTagName):
	root_items = os.listdir(rootDir)
	for rItem in root_items:
		rootElement = os.path.join(rootDir,rItem)
		if os.path.isdir(rootElement):
			print ("Folder in root level: %s in %s"% (rootElement, rootDir))
			f_Loop(rootElement,HeaderTagName)
	

def add_header(aFileName, aTagKey, aTagValue):
    #get file name , open it create header tag with aTagKey and assign aTagValue
    
    fits_image = fits.open(aFileName, mode='update')
    fits_hdr = fits_image[0].header
    #check if aTagKey exist
    if aTagKey in fits_hdr.keys():
        print("Tag %s exist in file:%s"%(aTagKey,aFileName)) #add decision check update or leave old value
    else:
        print("Tag %s will be added"%aTagKey)
        fits_hdr.set(aTagKey,aTagValue)
    

    fits_image.flush()
    fits_image.close()

def main():
    # get current directory path
    current_dir =  os.path.abspath(os.getcwd())
    # configure header tag name

    aHeaderTagName = 'ORLEN'
    f_MainLoop(current_dir,aHeaderTagName)

if __name__ == '__main__':
	main()