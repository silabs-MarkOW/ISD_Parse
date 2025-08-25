import data

def process(str) :
    pti = bytes([int(x,16) for x in str.strip().split()])
    HWstart = pti[0]
    isTx = (HWstart & 0x4) == 0x4
    ConfigInfo = pti[-1]
    AppendedInfoLength = (ConfigInfo >> 3) & 7
    RxTx = (ConfigInfo & 0x40) >> 6
    StatusByte = pti[-2]
    ErrorCode = StatusByte >> 4
    ProtoCol = StatusByte & 0x0f
    OtaEnd = len(pti)-4-AppendedInfoLength
    HWend = pti[OtaEnd]
    SyncWord = None
    if ErrorCode :
        raise RuntimeError
    if HWend == 0xff :
        pti_error("partial packet, PTI overrun (%s)"%(pti))
        raise RuntimeError
    elif HWend == 0xfa :
        pti_error("%.6f: RX abort (%s)"%(timestamp,ota))
        raise RuntimeError
    elif HWend == 0xfe :
        pti_error("%.6f: TX abort (%s)"%(timestamp,ota))
        raise RuntimeError
    elif HWend != 0xf9 and HWend != 0xfd :
        pti_error('%.6f: Unexpected HWEnd: 0x%02x %s'%(timestamp,HWend,pti))
        raise RuntimeError
    elif HWend == 0xfd :
        if 5 == AppendedInfoLength :
            SyncWord = int.from_bytes(pti[-8:][:4],'little');
        else :
            raise RuntimeError(timestamp)
    elif HWend == 0xf9 :
        Rssi =  pti[OtaEnd+1]
        if Rssi > 127 : Rssi-= 256
        Rssi -= 50
        if 6 == AppendedInfoLength :
            SyncWord = int.from_bytes(pti[-8:][:4],'little');
        elif 5 == AppendedInfoLength :
            SyncWord = int.from_bytes(pti[-7:][:4],'little');
        else :
            raise RuntimeError(timestamp)
    else :
        raise RuntimeError('HWEnd: 0x%02x'%(HWEnd))
    if None == SyncWord :
        raise RuntimeError(timestamp)
    Channel = pti[-3]
    ota = pti[1:OtaEnd]
    return ota

fh = open(0)
lines = fh.read().strip().split('\n')
payload = []
for line in lines :
    left = line.split('   ')[0]
    payload.append(left)

data.PDU(process(' '.join(payload)))
