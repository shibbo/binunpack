import struct, sys, os

offsets = []
isLast = False

def parseBIN(count):
    # offset is always 0x10 so no need for calculations
    i = 0
    j = 0
    offset = 16 # 0x10
    while j < count:
        fileOffset, = struct.unpack_from('>I', data, offset + i)
        offsets.append(fileOffset)
        i+=4
        j+=1

def dumpData(src, offset, index):
    # this is to make sure we don't read OOB
    # attempt to read an index further
    try:
        index+=1
        nextOffset = offsets[index]
        isLast = False
    except:
        nextOffset = None
        isLast = True

    if (isLast):
        end = len(src)
        bytesToRead = end - offset
    else:
        end = nextOffset
        bytesToRead = end - offset

    dataToWrite = struct.unpack_from('>%dB' % bytesToRead, data, offset)

    # now we determine the name of the folder we put the data in
    folderName = os.path.basename(sys.argv[1]).rstrip('.bin')

    # and we create it
    if not os.path.exists(folderName):
        os.makedirs(folderName)
        
    toWrite = data[offset : offset + bytesToRead]
    
    with open(folderName + '/%04d.bin' % index, 'wb') as f:
        print('Writing file %04d.bin...' % index)
        f.write(toWrite)

if len(sys.argv) == 2:
    with open(sys.argv[1], 'rb') as f:
        data = f.read()
else:
    print('Bin Extractor v0.1 by shibboleet')
    print('Syntax: binextractor.py <infile>')
    sys.exit()

# the rest is padding, we only need to read the first 4 bytes
try:
    count, = struct.unpack_from('>I', data, 0)
except:
    print('File is not a valid archive!')
    sys.exit()

parseBIN(count)

k = 0
for offset in offsets:
    dumpData(data, offset, k)
    k+=1

print('Done!')
