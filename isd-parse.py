import zipfile
import argparse
import sys
import getopt
import advertising
import data
import connection

parser = argparse.ArgumentParser()
parser.add_argument('--verbose',action='store_true')
parser.add_argument('--check-crc',action='store_true')
source = parser.add_mutually_exclusive_group(required=True)
source.add_argument('--isd',help='ISD file to parse')
source.add_argument('--event-file',help='unzipped event file to parse')
args = parser.parse_args()
print(args)

if None != args.isd :
    isd = zipfile.ZipFile(args.isd,'r')
    text = ''
    for name in isd.namelist() :
        if 0 == name.find('event') and '.log' == name[-4:] :
            fh = isd.open(name,'r')
            text += fh.read().decode('ASCII')
            fh.close()
else :
    fh = open(args.event_file,'rb')
    text = fh.read()
    fh.close()
    
verbose_pti = args.verbose

def verify_crc(ota) :
    bigintstr = ''
    pbits = 8 * len(ota)
    bits = 24
    mask = 0xffffff
    msb  = 0x800000
    polynomial = 0x100065b
    crc = 0x555555 # this is for DTM
    bigint = int.from_bytes(ota,'little')
    for i in range(pbits) :
        bit = 1 & (bigint >> i)
        if(msb & crc) :
           bit = not bit
        crc = mask & (crc << 1)
        if bit :
           crc ^= (mask & polynomial)
    return crc == 0

def pti_error(msg) :
    if verbose_pti :
        print(msg)

class Window :
    def __init__(self,start,stop,owner) :
        self.start = start
        self.stop = stop
        self.owner = owner
        print('Window: %.4f - %.4f s'%(start,stop))
    def contains(self,value) :
        if value < self.start :
            return False
        if value > self.stop :
            return False
        return True
    def below(self,value) :
        return self.stop < value

windows = []

def schedule(start,stop,owner) :
        windows.append(Window(start,stop,owner))
    
def callback(obj) :
    if type(obj) == advertising.CONNECT_IND :
        conn = connection.Connection(obj,timestamp,schedule)
    else :
        raise RuntimeError

lines = text.split('\n')
for line in lines :
    if 0 == len(line) :
        continue 
    if '#' == line[0] :
        continue
    if '[' != line[0] :
        raise RuntimeError('Unexpected line start: "%s"'%(line))
    tokens = line.split('] [')
    metadata1 = tokens[0][1:].split()
    if 'Packet' != metadata1[3] :
        continue
    timestamp = 1e-6*int(metadata1[0])
    pti = bytes([int(x,16) for x in tokens[2].replace(']','').strip().split()])
    HWstart = pti[0]
    isTx = (HWstart & 0x4) == 0x4
    ConfigInfo = pti[-1]
    AppendedInfoLength = (ConfigInfo >> 3) & 7
    OtaEnd = len(pti)-4-AppendedInfoLength
    HWend = pti[OtaEnd]
    Rssi =  pti[OtaEnd+1]
    if Rssi > 127 : Rssi-= 256
    Rssi -= 50
    Channel = pti[-3]
    ota = pti[1:OtaEnd]
    if HWend == 0xff :
        pti_error("partial packet, PTI overrun (%s)"%(pti))
        continue
    elif HWend == 0xfa :
        pti_error("%.6f: RX abort (%s)"%(timestamp,ota))
        continue
    elif HWend == 0xfe :
        pti_error("%.6f: TX abort (%s)"%(timestamp,ota))
        continue
    elif HWend != 0xf9 and HWend != 0xfd :
        pti_error('%.6f: Unexpected HWEnd: 0x%02x %s'%(timestamp,HWend,pti))
        continue
    if args.check_crc and not verify_crc(ota) :
        print("%.6f: %s CRC FAILURE"%(timestamp,ota))
    if pti[0:4] == [0xF8, 0x07, 0x07, 0x46] :
        print("%d %d dBm (%s)"%(Channel,Rssi,pti[OtaEnd+1]))

    clean = []
    obj = None
    for window in windows :
        if window.contains(timestamp) :
            if connection.Connection == type(window.owner) :
                print(timestamp)
                obj = data.PDU(ota[:-3])
                window.owner.process(obj,timestamp)
            else :
                raise RuntimeError
        elif not window.below(timestamp) :
            clean.append(window)
    if None == obj :
        obj = advertising.PDU(ota[:-3],Channel,callback)
    
