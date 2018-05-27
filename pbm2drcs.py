import sys, getopt

helpstring ="""Converts an ascii coded .pbm file into mode 0 teletext DRCS PTUs.

usage: pbm2drcs.py -i <inputfile> -o <outputfile> [-r]

optional arguments:
  -r  invert pixels"""

def main():
	inputfile = ''
	outputfile = ''
	
	invert = False
	
	try:
		opts, args = getopt.getopt(sys.argv[1:],"i:o:r")
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)

	for opt, arg in opts:
		if opt in ('-i'):
			inputfile = arg
		elif opt in ('-o'):
			outputfile = arg
		elif opt in ('-r'):
			invert = True

	if (inputfile == '' or outputfile == ''):
		print(helpstring)
		sys.exit()
	
	infile = open(inputfile, 'r')
	filedata = infile.read().splitlines()
	
	if filedata[0] != 'P1':
		print ("This is not an ascii pbm file.")
		sys.exit()
	
	line = 0
	while True:
		# skip past any comment lines
		line += 1
		if filedata[line][0] != '#':
			break
	
	size = filedata[line].split()
	w = int(size[0])
	h = int(size[1])
	line += 1
	
	if (w % 12 != 0) or (h % 10 != 0):
		print ("Image must be a multiple of 12 pixels wide and a multiple of 10 pixels tall")
		sys.exit()
	
	bitmap = ""
	
	while line < len(filedata):
		bitmap += filedata[line].replace(" ", "")
		line += 1
	
	x = int(w / 12)
	y = int(h / 10)
	step = (x*12)
	
	xormask = (0x00,0x3f)[invert]
	
	outfile = open(outputfile, 'w')
	outfile.write("DRCS mode 1 PTUs converted from {}\n".format(inputfile))
	
	for v in range (0,y):
		for h in range (0,x):
			for r in range (0,10):
				offset = ((v * 10 + r) * step) + (h * 12)
				outfile.write(chr((int(bitmap[offset:offset+6],2)^xormask)+0x40))
				outfile.write(chr((int(bitmap[offset+6:offset+12],2)^xormask)+0x40))
			outfile.write("\n")

if __name__ == "__main__":
    main()