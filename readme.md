# pbm2drcs
A python script to convert ascii pbm files to mode 0 teletext DRCS PTUs.

## Invocation
`pbm2drcs.py -i <inputfile> -o <outputfile> [-r]`

`inputfile` should contain an ascii encoded pbm file (netpbm P1) an exact multiple of 12 pixels wide, and an exact multiple of 10 pixels high.

The `-r` flag inverts all pixels