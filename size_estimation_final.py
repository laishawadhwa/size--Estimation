
#imports
from sizeEstimationUtility import *

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, help="path to input directory")
ap.add_argument("-o", "--output", type=str, help="path to output directory to write the files")
ap.add_argument("-len", "--length", type=float, help="Actual length of the reference object(in inch/cm)")
args = vars(ap.parse_args())


directory=args["input"] +'/'
filenames=[]
count=0


for file in os.listdir(directory):
    if file[-4:]=='.jpg':
        filenames.append(file[:-4])



# Create directory
if not os.path.exists(args['output']):
    os.makedirs(args['output'])

#iterate over all files in input directory
for fil in filenames:
	filepath=directory + fil + '.xml'
	image=cv2.imread(directory + fil + '.jpg')

	tree = ET.parse(filepath)
	root = tree.getroot()

	objco=[]
	refer=[]
	for obj in tree.iter('object'):
		    for elem in obj.iter():
		        if elem.tag=='name':
		            objtype=elem.text
		            print(objtype)
		        if elem.tag=='segment_polygons':
		            for subtag in elem.iter():
		                
		                if subtag.tag=='point':
		                    vals=subtag.findall('value')
		                    for v in vals:
		                        if objtype=='object':
		                            objco.append(int(v.text))
		                        elif objtype=='reference':
		                            refer.append(int(v.text))


	it = iter(objco)
	objco=list(zip(it, it))
	it2=iter(refer)
	refer=list(zip(it2, it2))
	print('reference coords: ',refer,'\n','object coords: ',objco)
	#calling test function
	objectSizeEstimation(image,objco,refer, args["output"] + 'Image' + str(count) + '.jpg',args['length'])
	count+=1

