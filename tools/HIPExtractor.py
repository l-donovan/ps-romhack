from __future__ import print_function

#
# HIPExtractor
# HIP/HOP extractor
# (c) 2016 Luke Donovan
#
# Usage: "python HIPExtractor.py file"
# "file" can be any HIP or HOP file
#

import binascii
import os
import sys

infile = sys.argv[1]

offset = 0
def readBytes(byteCount):
    global offset
    _offset = offset
    offset += byteCount
    return data[_offset:_offset+byteCount]

def readBytesAtOffset(offsetDec, byteCount):
    global offset
    _offset = offset
    offset = offsetDec
    out = readBytes(byteCount)
    offset = _offset
    return out

def readBytesUntilNull():
    global offset
    out = []
    while True:
        if (data[offset] == '00'):
            return out
        else:
            out.append(data[offset])
            offset += 1

def toChar(byteArray):
    return ''.join([binascii.unhexlify(c) for c in byteArray])

def toInt(byteArray):
    return int(''.join(byteArray), 16)


print('Loading archive...', end='')
with open(infile, 'rb') as f:
    data = binascii.hexlify(f.read())
data = [data[i:i+2] for i in range(0, len(data), 2)]
print('[DONE]')


print('Processing header information...', end='')

archive_header = readBytes(4)                                       # [char] Archive Header (HIPA)
offset += 4                                                         # [null]
pack_header = readBytes(4)                                          # [char] Pack Header (PACK)
pack_header_length = readBytes(4)                                   # [uint] Pack Header Length

version_header = readBytes(4)                                       #   [char] Version Header (PVER)
version_header_length = readBytes(4)                                #   [uint] Version Header Length
sub_version = readBytes(4)                                          #       [uint] Sub-Version
client_version_major = readBytes(2)                                 #       [uint] Client Version Major
client_version_minor = readBytes(2)                                 #       [uint] Client Version Minor
library_version = readBytes(4)                                      #       [uint] Library Version

flags_header = readBytes(4)                                         #   [char] Flags Header (PFLG)
flags_header_length = readBytes(4)                                  #   [uint] Flags Header Length
flags = readBytes(4)                                                #       [uint] Flags

count_header = readBytes(4)                                         #   [char] Count Header (PCNT)
count_header_length = readBytes(4)                                  #   [uint] Count Header Length
count_assets = readBytes(4)                                         #       [uint] Number of Assets
count_layers = readBytes(4)                                         #       [uint] Number of Layers
unknown1 = readBytes(4)                                             #       [uint] ??? Size of Largest File?
file_data_length = readBytes(4)                                     #       [uint] Length of the File Data
unknown2 = readBytes(4)                                             #       [uint] ??? Same as unknown1

creation_date_header = readBytes(4)                                 #   [char] Creation Date Header (PCRT)
creation_date_header_length = readBytes(4)                          #   [uint] Creation Date Header Length
creation_date_adbc = readBytes(4)                                   #       [char] Creation Date AD/BC
creation_date_day = readBytes(4)                                    #       [char] Creation Date Day
creation_date_month = readBytes(4)                                  #       [char] Creation Date Month
creation_date_date = readBytes(3)                                   #       [char] Creation Date Date
creation_date_time_24h = readBytes(9)                               #       [char] Creation Date 24 Hours
creation_date_year = readBytes(4)                                   #       [char] Creation Date Year
offset += 2                                                         #       [null]

modification_date_header = readBytes(4)                             #   [uint] Modification Date Header (PMOD)
modification_date_header_length = readBytes(4)                      #   [uint] Modification Date Header Length
modification_date_adbc = readBytes(4)                               #       [char] Modification Date AD/BC

platform_header = readBytes(4)                                      #   [char] Platform Header (PLAT)
platform_header_length = readBytes(4)                               #   [uint] Platform Header Length
o = offset                                                          #
platform_name_abbr = readBytes(4)                                   #       [char] Platform Name Abbreviation
platform_name = readBytes(8)                                        #       [char] Platform Name Full
offset += 2                                                         #       [null]
platform_gfx_format = readBytes(4)                                  #       [char] Platform Graphics Format (NTSC)
offset += 2                                                         #       [null]
platform_language = readBytes(9)                                    #       [char] Platform Game Language
offset += 1                                                         #       [null]
platform_game_name = readBytesUntilNull()                           #       [char] Platform Game Name
B = toInt(platform_header_length) - offset + o                      #
offset += B                                                         #       [null]

directory_header = readBytes(4)                                     # [char] Directory Header (DICT)
directory_header_length = readBytes(4)                              # [uint] Directory Header Length
toc_header = readBytes(4)                                           #   [char] Table of Contents Header (ATOC)
toc_header_length = readBytes(4)                                    #   [uint] Table of Contents Length
info_header = readBytes(4)                                          #       [char] Information Header (AINF)
info_header_length = readBytes(4)                                   #       [uint] Information Header Length
offset += 4                                                         #       [null]

files = []
while True:
    header = readBytes(4)
    if (toChar(header) == 'LTOC'): break
    f = {}
    f['file_entry_header'] = header                                 #           [char] File Entry Header (AHDR)
    f['file_entry_length'] = readBytes(4)                           #           [uint] File Entry Header Length
    f['unknown1'] = readBytes(4)                                    #           [????] ????
    f['file_type_code'] = readBytes(4)                              #           [char] File Type Code
    f['file_offset'] = readBytes(4)                                 #           [uint] File Offset
    f['file_size'] = readBytes(4)                                   #           [uint] File Size
    f['file_type_id'] = readBytes(4)                                #           [uint] File Type Code ID
    f['unknown2'] = readBytes(4)                                    #           [????] ????
    f['file_details_header'] = readBytes(4)                         #           [char] File Details Header
    f['file_details_header_length'] = readBytes(4)                  #           [uint] File Details Header Length
    o = offset                                                      #
    offset += 4                                                     #               [null]
    f['file_details_filename'] = readBytesUntilNull()               #               [char] File Details Filename
    offset += 1                                                     #               [null]
    B = toInt(f['file_details_header_length']) - offset + o - 4     #
    f['file_details_padding'] = readBytes(B)                        #               [null] File Details Padding?
    f['file_details_hash'] = readBytes(4)                           #               [uint] File Details Hash
    files.append(f)

ltoc_header = header                                                #       [char] L Table Of Contents Header (LTOC)
ltoc_header_length = readBytes(4)                                   #       [uint] L Table of Contents Header Length
linfo_header = readBytes(4)                                         #           [char] L Information Header (LINF)
linfo_header_length = readBytes(4)                                  #           [uint] L Information Header Length
offset += toInt(linfo_header_length)                                #               [null]

toc_items = []
while True:
    header = readBytes(4)
    if (toChar(header) == 'STRM'): break
    t = {}
    t['l_header'] = header                                          #               [char] L Header
    t['l_header_length'] = readBytes(4)                             #               [uint] L Header Length
    t['unknown1'] = readBytes(toInt(t['l_header_length']) - 12)     #                   [????] ????
    t['l_file_details_header'] = readBytes(4)                       #                   [char] L File Details Header
    t['l_file_details_header_length'] = readBytes(4)                #                   [uint] L File Details Header Length
    offset += 4                                                     #                       [null]
    toc_items.append(t)

strm_header = header                                                # [char] STRM Header (STRM)
strm_header_length = readBytes(4)                                   # [uint] STRM Header Length
dhdr_header = readBytes(4)                                          #   [char] DHDR Header (DHDR)
dhdr_header_length = readBytes(4)                                   #   [uint] DHDR Header Length
offset += toInt(dhdr_header_length)                                 #       [null]
dpak_header = readBytes(4)                                          #   [char] DPAK Header (DPAK)
dpak_header_length = readBytes(4)                                   #   [uint] DPAK Header Length
asset_data = readBytes(toInt(dpak_header_length))                   #       [byte] Asset Data

print('[DONE]')

dirName = infile.rsplit('/', 1)[1].split('.')[0]

print('Extracting assets from archive...', end='')
for i in range(0, len(files)):
    filepath = './' + dirName + '/' + toChar(files[i]['file_details_filename'])
    if not os.path.exists(filepath.rsplit('/', 1)[0]):
        os.makedirs(filepath.rsplit('/', 1)[0])
    with open(filepath, 'a+') as of:
        _offset = toInt(files[i]['file_offset'])
        _size = toInt(files[i]['file_size'])
        of.write(binascii.unhexlify(''.join(readBytesAtOffset(_offset, _size))))
print('[DONE]')
