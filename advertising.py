import scheduling
import connection

def is_primary_channel(channel) :
    if 0 == channel or 12 == channel or 39 == channel :
        return True
    return False

class ADV_IND :
    def __init__(self,data) :
        self.AdvA = data[:6]
        self.AdvData = data[6:]

class ADV_NONCONN_IND :
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
        self.AA = int.from_bytes(data[:4],'little')
        self.CRCInit = int.from_bytes(data[4:7],'little')
        self.WinSize = data[7]*1.25e-3
        self.WinOffset = int.from_bytes(data[8:10],'little')*1.25e-3
        self.Interval = int.from_bytes(data[10:12],'little')*1.25e-3
        self.Latency = int.from_bytes(data[12:14],'little')
        self.Timeout = int.from_bytes(data[14:16],'little')*10e-3
        self.ChM =  int.from_bytes(data[16:21],'little')
        self.Hop = data[21] & 0x1f
        self.SCA = data[21] >> 5
        print('AA: 0x%08x, Offset:%.1f ms, Size:%.1f ms, Interval: %.1f ms, Timeout: %d ms'%(self.AA, 1e3*self.WinOffset, 1e3*self.WinSize,1e3*self.Interval,1e3*self.Timeout))

class CONNECT_IND :
    def __init__(self,data) :
        self.InitA = data[:6]
        self.AdvA = data[6:12]
        self.LLData = LLData(data[12:])
        self.connection = connection.Connection(self)
        #delay = 1.25e-3
        #scheduling.schedule(self.LLData.WinOffset + delay,self.LLData.WinSize,self.connection)

class AUX_CONNECT_REQ :
    def __init__(self,data) :
        self.InitA = data[:6]
        self.AdvA = data[6:12]
        self.LLData = LLData(data[12:])
        self.timestamp = scheduling.now
        print('AUX_CONNECT_REQ')
        self.connection = connection.Connection(self)
        scheduling.schedule(150e-6,150e-6,self)
    def process(self,data,channel,SyncWord,window) :
        if SyncWord != 0x8e89bed6 :
            return None
        obj = PDU(data,channel,SyncWord)
        if None != obj :
            self.connection.schedule()
        return obj
        
class AuxPtr :
    def __init__(self,data) :
        self.Channel_index = data[0] & 0x3f
        self.CA = (data[0] >> 6) & 1
        if data[0] & 0x80 :
            self.OffsetUnits = 300e-6
        else :
            self.OffsetUnits = 30e-6
        self.AuxOffset = int.from_bytes(data[1:],'little') & 0x1fff
        self.AuxPhy = (data[2] >> 5) & 7
        if self.AuxPhy > 2 :
            raise RuntimeError(self.AuxPhy)

class SyncInfo :
    def __init__(self,data) :
        self.OffsetBase = data[0] | ((data[1] & 0x1f) << 8)
        if data[1] & 0x20 :
            self.OffsetUnits = 300e-6
        else :
            self.OffsetUnits = 30e-6
        self.OffsetAdjust = (data[1] >> 7) & 1
        Interval = int.from_bytes(data[2:4],'little')
        self.ChM = int.from_bytes(data[4:9]) & 0x1fffffffff
        self.SCA = data[8] >> 5
        self.AA = int.from_bytes(data[9:13],'little')
        self.CRCInit = int.from_bytes(data[13:16],'little')
        self.PeriodicEventCounter = int.from_bytes(data[16:18],'little')
    def syncPacketWindowOffset(self) :
        s = self.OffsetBase * self.OffsetUnits
        if self.OffsetAdjust :
            s += 2.4576
        return s
    def __str__(self) :
        return 'Offset: {:f} ms, ChM: {:037b}, AA: 0x{:08x}, Counter: {:d}'.format(1e3*self.syncPacketWindowOffset(),self.ChM,self.AA,self.PeriodicEventCounter) 
        
def P(x) :
    return ' '.join(['%02x'%(x) for x in list(x)])

class AdvDataInfo :
    def __init__(self, data) :
        word = int.from_bytes(data,'little')
        self.DID = word & 0x0fff
        self.SID = word >> 12
    def __str__(self) :
        return 'Advertising Data ID: %d, Advertising Set ID: %d'%(self.DID,self.SID)
    
class ExtendedHeader :
    def __init__(self,data) :
        #print("class ExtendedHeader.__init__(",list(data))
        flags = data[0]
        data = data[1:]
        #print('flags: {:08b}'.format(flags))
        if flags & 1 :
            self.AdvA = int.from_bytes(data[:6],'little')
            data = data[6:]
        else :
            self.AdvA = None
        if flags & 2 :
            self.TargetA = int.from_bytes(data[:6],'little')
            data = data[6:]
        else :
            self.TargetA = None
        if flags & 4 :
            self.CTEInfo = data[0]
            #print('CTEInfo:',CTEInfo)
            data = data[1:]
        else :
            self.CTEInfo = None
        if flags & 8 :
            self.AdvDataInfo = AdvDataInfo(data[:2])
            #print('AdvDataInfo:',self.AdvDataInfo)
            data = data[2:]
        else :
            self.AdvDataInfo = None
        if flags & 0x10 :
            self.AuxPtr = AuxPtr(data[:3])
            #print('AuxPtr:',self.AuxPtr)
            data = data[3:]
        else :
            self.AuxPtr =  None
        if flags & 0x20 :
            self.SyncInfo = SyncInfo(data[:18])
            #print('SyncInfo:',self.SyncInfo)
            data = data[18:]
        else :
            self.SyncInfo = None
        if flags & 0x40 :
            self.TxPower = data[0]
            data = data[1:]
        else :
            self.TxPower = None
        self.ACAD = data
        
class CommonExtendedAdvertisingPayload :
    def __init__(self,data) :
        self.ExtendedHeaderLength = data[0] & 0x3f
        self.AdvMode = (data[0] >> 6) & 3
        self.ExtendedHeader = ExtendedHeader(data[1:][:self.ExtendedHeaderLength])
        self.AdvData = data[1:][self.ExtendedHeaderLength:]
        
class ADV_EXT_IND :
    def __init__(self,data) :
        self.Payload = CommonExtendedAdvertisingPayload(data)
        AuxPtr = self.Payload.ExtendedHeader.AuxPtr
        if None != AuxPtr :
            offset = AuxPtr.AuxOffset * AuxPtr.OffsetUnits
            scheduling.schedule(offset, AuxPtr.OffsetUnits, self)
    def process(self,data,channel,SyncWord,window) :
        print('ADV_EXT_IND.process(',data,')','SyncWord:0x%08x'%(SyncWord))
        #try :
        obj = PDU(data,channel,SyncWord)
        #except :
        #    return None
        return obj
    def on_missed(self) :
        pass

class AUX_ADV_IND :
    def __init__(self,data) :
        self.Payload = CommonExtendedAdvertisingPayload(data)
        SyncInfo = self.Payload.ExtendedHeader.SyncInfo
        if None != SyncInfo :
            offset = SyncInfo.syncPacketWindowOffset()
            scheduling.schedule(offset, SyncInfo.OffsetUnits, self)
    def process(self,data,channel,SyncWord,window) :
        print('AUX_ADV_IND.process(',data,')','SyncWord:0x%08x'%(SyncWord))
        #try :
        obj = PDU(data,channel,SyncWord)
        #except :
        #    return None
        return obj
    def on_missed(self) :
        pass

class AUX_SYNC_IND :
    def __init__(self,data) :
        self.Payload = CommonExtendedAdvertisingPayload(data)
        AuxPtr = self.Payload.ExtendedHeader.AuxPtr
        if None != AuxPtr :
            offset = AuxPtr.AuxOffset * AuxPtr.OffsetUnits
            scheduling.schedule(offset, AuxPtr.OffsetUnits, self)
    def process(self,data,channel,SyncWord,window) :
        print('AUX_SYNC_IND.process(',data,')','SyncWord:0x%08x'%(SyncWord))
        #try :
        obj = PDU(data,channel,SyncWord)
        #except :
        #    return None
        return obj
    def on_missed(self) :
        pass

class AUX_CONNECT_RSP :
    def __init__(self,data) :
        self.Payload = CommonExtendedAdvertisingPayload(data)
        if 0x00 != self.Payload.AdvMode :
            raise RuntimeError
        if None == self.Payload.ExtendedHeader.AdvA :
            raise RuntimeError
        if None == self.Payload.ExtendedHeader.TargetA :
            raise RuntimeError
    
class PDU :
    def __init__(self,data,channel,SyncWord) :
        self.header = int.from_bytes(data[:2],'little')
        self.payload = data[2:]
        pdu_type = self.header & 0xf
        self.length = self.header >> 8
        self.content = None
        if SyncWord == 0x8e89bed6 :
            if 0 == pdu_type :
                self.content = ADV_IND(self.payload)
            elif 1 == pdu_type :
                self.content = ADV_DIRECT_IND(self.payload)
            elif 2 == pdu_type :
                self.content = ADV_NONCONN_IND(self.payload)
            elif 3 == pdu_type :
                if is_primary_channel(channel) :
                    self.content = SCAN_REQ(self.payload)
                else :
                    self.content = AUX_SCAN_REQ(self.payload)
            elif 4 == pdu_type :
                self.content = SCAN_RSP(self.payload)
            elif 5 == pdu_type :
                if is_primary_channel(channel) :
                    self.content = CONNECT_IND(self.payload)
                else :
                    self.content = AUX_CONNECT_REQ(self.payload)
            elif 7 == pdu_type :
                if is_primary_channel(channel) :
                    self.content = ADV_EXT_IND(self.payload)
                else :
                    self.content = AUX_ADV_IND(self.payload)
            elif 8 == pdu_type :
                self.content = AUX_CONNECT_RSP(self.payload)
        else :
            if 7 == pdu_type :
                self.content = AUX_SYNC_IND(self.payload)
        if None == self.content :
            raise RuntimeError('%f: channel:%d, type:%d'%(scheduling.now, channel,pdu_type))
