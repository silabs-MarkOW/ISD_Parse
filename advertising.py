def is_primary_channel(channel) :
    if 0 == channel or 12 == channel or 39 == channel :
        return True
    return False

class ADV_IND :
    def __init__(self,data) :
        self.AdvA = data[:6]
        self.AdvData = data[6:]

class SCAN_REQ :
    def __init__(self,data) :
        self.ScanA = data[:6]
        self.AdvA = data[6:]
    
class AUX_SCAN_REQ :
    def __init__(self,data) :
        self.ScanA = data[:6]
        self.AdvA = data[6:]
    
class SCAN_RSP :
    def __init__(self,data) :
        self.AdvA = data[:6]
        self.ScanRspData = data[6:]

class LLData :
    def __init__(self,data) :
        self.AA = data[:4]
        self.CRCInit = data[4:7]
        self.WinSize = data[7]
        self.WinOffset = int.from_bytes(data[8:10],'little')
        self.Interval = int.from_bytes(data[10:12],'little')
        self.Latency = int.from_bytes(data[12:14],'little')
        self.Timeout = int.from_bytes(data[14:16],'little')
        self.ChM =  int.from_bytes(data[16:21],'little')
        self.Hop = data[21] & 0x1f
        self.SCA = data[21] >> 5
        print('Offset:%d, Size:%d, Interval: %.1f ms, Timeout: %d ms'%(self.WinOffset, self.WinSize,self.Interval*1.25,self.Timeout*10))
class CONNECT_IND :
    def __init__(self,data,callback) :
        self.InitA = data[:6]
        self.AdvA = data[6:12]
        self.LLData = LLData(data[12:])
        callback(self)
        if 34 != len(data) :
            raise RuntimeError(data)

class PDU :
    def __init__(self,data,channel,callback) :
        self.header = int.from_bytes(data[:2],'little')
        self.payload = data[2:]
        pdu_type = self.header & 0xf
        self.length = self.header >> 8
        if 0 == pdu_type and is_primary_channel(channel) :
            self.content = ADV_IND(self.payload)
        elif 1 == pdu_type and is_primary_channel(channel) :
            self.content = ADV_DIRECT_IND(self.payload)
        elif 2 == pdu_type and is_primary_channel(channel) :
            self.content = ADV_NONCONN_IND(self.payload)
        elif 3 == pdu_type and is_primary_channel(channel) :
            self.content = SCAN_REQ(self.payload)
        elif 3 == pdu_type and not is_primary_channel(channel) :
            self.content = AUX_SCAN_REQ(self.payload)
        elif 4 == pdu_type and is_primary_channel(channel) :
            self.content = SCAN_RSP(self.payload)
        elif 5 == pdu_type and is_primary_channel(channel) :
            self.content = CONNECT_IND(self.payload,callback)
        elif 7 == pdu_type and is_primary_channel(channel) :
            self.content = ADV_EXT_IND(self.payload)
            
        else :
            raise RuntimeError('channel:%d, type:%d'%(channel,pdu_type))
