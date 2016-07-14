from __future__ import print_function

import binascii
import sys

infile = sys.argv[1]

with open(infile, 'rb') as f:
    data = binascii.hexlify(f.read())
data = [data[i:i+2] for i in range(0, len(data), 2)]

offset = 0
def readBytes(byteCount):
    global offset
    _offset = offset
    offset += byteCount
    return data[_offset:_offset+byteCount]

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

archive_header = readBytes(4)                   # [char] Archive Header (HIPA)
offset += 4                                     # [null]
pack_header = readBytes(4)                      # [char] Pack Header (PACK)
pack_header_length = readBytes(4)               # [uint] Pack Header Length

version_header = readBytes(4)                   #   [char] Version Header (PVER)
version_header_length = readBytes(4)            #   [uint] Version Header Length
sub_version = readBytes(4)                      #       [uint] Sub-Version
client_version_major = readBytes(2)             #       [uint] Client Version Major
client_version_minor = readBytes(2)             #       [uint] Client Version Minor
library_version = readBytes(4)                  #       [uint] Library Version

flags_header = readBytes(4)                     #   [char] Flags Header (PFLG)
flags_header_length = readBytes(4)              #   [uint] Flags Header Length
flags = readBytes(4)                            #       [uint] Flags

count_header = readBytes(4)                     #   [char] Count Header (PCNT)
count_header_length = readBytes(4)              #   [uint] Count Header Length
count_assets = readBytes(4)                     #       [uint] Number of Assets
count_layers = readBytes(4)                     #       [uint] Number of Layers
unknown1 = readBytes(4)                         #       [uint] ??? Size of Largest File?
file_data_length = readBytes(4)                 #       [uint] Length of the File Data
unknown2 = readBytes(4)                         #       [uint] ??? Same as unknown1

creation_date_header = readBytes(4)             #   [char] Creation Date Header (PCRT)
creation_date_header_length = readBytes(4)      #   [uint] Creation Date Header Length
creation_date_adbc = readBytes(4)               #       [char] Creation Date AD/BC
creation_date_day = readBytes(4)                #       [char] Creation Date Day
creation_date_month = readBytes(4)              #       [char] Creation Date Month
creation_date_date = readBytes(3)               #       [char] Creation Date Date
creation_date_time_24h = readBytes(9)           #       [char] Creation Date 24 Hours
creation_date_year = readBytes(4)               #       [char] Creation Date Year
offset += 2                                     #       [null]

modification_date_header = readBytes(4)         #   [uint] Modification Date Header
modification_date_header_length = readBytes(4)  #   [uint] Modification Date Header Length
modification_date_adbc = readBytes(4)           #       [char] Modification Date AD/BC

platform_header = readBytes(4)                  #   [char] Platform Header (PLAT)
platform_header_length = readBytes(4)           #   [uint] Platform Header length
o = offset                                      #
platform_name_abbr = readBytes(4)               #       [char] Platform Name Abbreviation
platform_name = readBytes(8)                    #       [char] Platform Name Full
offset += 2                                     #       [null]
platform_gfx_format = readBytes(4)              #       [char] Platform Graphics Format (NTSC)
offset += 2                                     #       [null]
platform_language = readBytes(9)                #       [char] Platform Game Language
offset += 1                                     #       [null]
platform_game_name = readBytesUntilNull()       #       [char] Platform Game Name
B = toInt(platform_header_length) - offset + o  #
offset += B                                     #       [null]

directory_header = readBytes(4)                 # [char] Directory Header
directory_header_length = readBytes(4)          # [uint] Directory Header length
toc_header = readBytes(4)                       #   [char] Table of Contents Header
toc_header_length = readBytes(4)                #   [uint] Table of Contents Length
info_header = readBytes(4)                      #       [char] Information Header
info_header_length = readBytes(4)               #       [uint] Information Header Length
offset += 4                                     #       [null]

print(toChar(info_header))
