import sys
import getopt

class Help :
    def __init__(s) :
        s.switches = []
        s.descs = []
        s.params = []
        s.defaults = []
    def add(s,sw,desc,param=None,default=None) :
        s.switches.append(sw)
        s.descs.append(desc)
        if None == param :
            s.params.append('')
            s.defaults.append('')
        else :
            if '-' == sw[1] :
                s.params.append('=%s'%(param))
            else :
                s.params.append(' %s'%(param))
        if None == default :
            s.defaults.append('')
        else :
            s.defaults.append('(default:%s)'%(default))
    def maxlen(s,array) :
        max = 0
        for i in array :
           l = len(i)
           if l > max :
               max = l
        return max
    def render(s) :
        print('Options:')
        format = '%%%ds%%%ds : %%-%ds %%%ds'%(s.maxlen(s.switches)+5,s.maxlen(s.params),s.maxlen(s.descs),s.maxlen(s.defaults))
        for i in range(len(s.switches)) :
            print(format%(s.switches[i],s.params[i],s.descs[i],s.defaults[i]))
        
def exit_help(prognam,error=None) :
    if None != error :
        print('Error: %s'%(error))
    print('Usage: %s [ options ] <isd-log-file>:'%(prognam))
    help = Help()
    help.add('--supress-pti','suppress rendering of unexceptional data')
    help.add('-h','show this help')
    help.render()
    quit(0)

verbose_pti = True
opts,params = getopt.getopt(sys.argv[1:],'-h',['suppress-pti'])
for opt,param in opts :
    if '--suppress-pti' == opt :
        verbose_pti = False
    if '-h' == opt :
        exit_help(sys.argv[0])

if 1 == len(params) :
    fh = open(params[0],'r')
    text = fh.read()
    fh.close()
elif 0 == len(params) :
    exit_help(sys.argv[0],'No ISD log file specified')
else :
    exit_help(sys.argv[0],'Only single ISD log file supported, multiple specified:\n\t%s'%(params.__str__()))
    
def verify_crc(ota) :
    bigintstr = ''
    pbits = 8 * len(ota)
    bits = 24
    mask = 0xffffff
    msb  = 0x800000
    polynomial = 0x100065b
    crc = 0x555555
    for hexstrbyte in ota :
        bigintstr = hexstrbyte + bigintstr # reverse bytes
    bigint = int(bigintstr,16)
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
    pti = tokens[2][:-1].split()
    HWstart = int(pti[0],16)
    isTx = (HWstart & 0x4) == 0x4
    ConfigInfo = int(pti[-1],16)
    AppendedInfoLength = (ConfigInfo >> 3) & 7
    OtaEnd = len(pti)-4-AppendedInfoLength
    HWend = int(pti[OtaEnd],16)
    Rssi =  int(pti[OtaEnd+1],16)
    if Rssi > 127 : Rssi-= 256
    Rssi -= 50
    Channel = int(pti[-3],16)
    ota = pti[1:OtaEnd]
    if HWend == 0xff :
        pti_error("partial packet, PTI overrun (%s)"%(pti))
        continue
    elif HWend == 0xfa :
        pti_error("%.6f: RX abort (%s)"%(timestamp,ota))
        continue
    elif HWend == 0xfe :
        pti_error("%.6f: TX abort (%s)"%(timestamp,ota))
    elif HWend != 0xf9 and HWend != 0xfd :
        pti_error('%.6f: Unexpected HWEnd: 0x%02x %s'%(timestamp,HWend,pti))
        continue
    if not verify_crc(ota) :
        print("%.6f: %s CRC FAILURE"%(timestamp,ota))
    if pti[0:4] == ['F8', '07', '07', '46'] :
        print("%d %d dBm (%s)"%(Channel,Rssi,pti[OtaEnd+1]))
              
