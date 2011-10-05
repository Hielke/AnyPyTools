# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 16:12:06 2011

@author: melund
"""


import optparse
import re

from xml.dom import minidom

def read_ppfile(filename):
	xmldoc = minidom.parse(filename)
	pointlist = xmldoc.getElementsByTagName('point')
	
	for pointref in pointlist:
		print pointref.attributes["name"]
		print pointref.attributes["x"]
		print pointref.attributes["y"]
		print pointref.attributes["z"]
	
		
def read_landmarks(filename, output):
    fin = open(filename, 'r')
    fout = open(output, 'w')
    names = []
    cnt = 0
    for line in fin:
        m = re.search('<point x="', line)
        if m == None:
            continue
        if cnt == 0:
            fout.write('Points = {\n')
            cnt = cnt + 1
        else:
            fout.write(',\n')
        line = line[:m.start()] + line[m.end():]
        m = re.search('" y="', line)
        line = line[:m.start()] + ' ' + line[m.end():]
        m = re.search('" z="', line)
        line = line[:m.start()] + ' ' + line[m.end():]
        m = re.search('" active="1" name="', line)
        line = line[:m.start()] + ' ' + line[m.end():]
        m = re.search('"/>', line)
        res = line[:m.start()].split() 
        line = '{' + res[0] + ','+ res[1] + ','+ res[2] + '}'
        fout.write(line)
        names.append(res[3])
    fout.write('};\nPointNames = {\n')
    cnt = 0
    for i in xrange(len(names)):
        if cnt == 0:
            cnt = cnt + 1
        else:
            fout.write(',\n')
        nameline = '"' + names[i] + '"'
        fout.write(nameline)
    fout.write('};')
    fin.close()
    fout.close()

if __name__ == '__main__':

    usage = \
"""usage: %prog -r refmarkers -t tgtmarkers -R refsurf -T tgtsurf -p pts -o output [-n nummark]\n
Arguments:
-r refmarkers  : file with reference markers        
-t tgtmarkers  : file with target markers
-R refsurf     : anysurf file with reference surface.
-T tgtsurf     : anysurf file with target surface.
-p pts         : file with (attachment) points to be transformed.
-o output      : output file with transformed (attachment) points. 
-n nummark     : number of autogenerated markers. Default is ~1000.
"""
    cmdparser = optparse.OptionParser(usage = usage)
    
    cmdparser.add_option("-f", "--landmarks", 
                         action="store", type="string", dest="lmfile",
                         help="file with reference markers")
    cmdparser.add_option("-o", "--output", 
                         action="store", type="string", dest="output",
                         help="file with reference markers")
    (options, args) = cmdparser.parse_args()
#    options.lmfile = "L1Seg_uniform_picked_points.pp"   
#    options.output = "output.any" 
    read_landmarks(options.lmfile, options.output)
    
    
    