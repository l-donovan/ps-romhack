from __future__ import print_function

#
# LHExtractor
# HIP/HOP extractor using LIP/LOP manifests
# (c) 2016 Luke Donovan
#
# Usage: "python LHExtractor.py file [-v / --verbose]"
# "file" can be any LIP, LOP, HIP, or HOP file
#

import sys
import re
import os

regString = r'AID: 0x([0-9a-fA-F]{8})\s+\((\w+)\)\r\n{\r\n\s+Type:\s+(\w+)\r\n\s+Size:\s+(\d+)\r\n\s+Offset:\s+(\d+)\r\n\s+Plus:\s+(\d+)\r\n\s+Check:\s+0x([0-9a-fA-F]{8})\r\n\s+Filename:\s+([^\s]+)\r\n\s+Flags:\s+(.+)\r\n}'
outObjects = []

lpfile = sys.argv[1][:-3] + 'L' + sys.argv[1][-2] + 'P'
hpfile = lpfile[:-3] + 'H' + lpfile[-2] + 'P'

if ('--verbose' in sys.argv or '-v' in sys.argv): verbose = True
else: verbose = False

if (verbose): print('Starting extraction of ' + lpfile)

if (verbose): print('Reading L file', end=' ')
with open(lpfile, 'r+b') as f:
    fileData = f.read()
if (verbose): print('[DONE]')

if (verbose): print('Storing object data', end=' ')
outData = re.findall(regString, fileData)
for i in range(0, len(outData)):
    outObjects.append({
        'id': outData[i][0],
        'name': outData[i][1],
        'type': outData[i][2],
        'size': outData[i][3],
        'offset': outData[i][4],
        'plus': outData[i][5],
        'check': outData[i][6],
        'filename': outData[i][7],
        'flags': outData[i][8]
    })
if (verbose): print('[DONE]')

if (verbose): print('Beginning object extraction')
with open(hpfile, 'r+b') as inf:
    for i in range(0, len(outObjects)):
        if (outObjects[i]['filename'] != "N/A" and outObjects[i]['filename']):
            filepath = outObjects[i]['filename'].replace('\\\\', './source/').replace('\\', '/')
        else:
            filepath = './source/unsorted/' + outObjects[i]['name']
        if verbose:
            print("Extracting {} {} from 0x{} for {} Bytes".format(
                outObjects[i]['type'],
                filepath,
                outObjects[i]['offset'],
                outObjects[i]['size']
            ), end=' ')
        if not os.path.exists(filepath.rsplit('/', 1)[0]):
            os.makedirs(filepath.rsplit('/', 1)[0])
        with open(filepath, 'a+') as otf:
           inf.seek(int(outObjects[i]['offset']))
           otf.write(inf.read(int(outObjects[i]['size'])))
        if verbose: print("[DONE]")
if (verbose): print('Finished object extraction')

print('All done!')
