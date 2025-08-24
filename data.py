import ll_control
import attribute
import scheduling

class LL_Control :
    def __init__(self,data) :
        self.opcode = data[0]
        self.CtrlData = data[1:]
        cls = ll_control.LL_Control_PDUs.get(self.opcode)
        if None == cls :
            raise RuntimeError(scheduling.now, 'LL_Control.opcode: 0x%02x'%(self.opcode))
        self.content = cls(self.CtrlData)
    def __str__(self) :
        return self.content.__str__()
    
class Empty_PDU :
    def __str__(self) :
        return 'Empty PDU'

class L2CAP :
    def __init__(self,data) :
        self.Length = int.from_bytes(data[:2],'little')
        self.Channel_ID = int.from_bytes(data[2:4],'little')
        if len(data) != self.Length + 4 :
            raise RuntimeError
        if 4 == self.Channel_ID :
            self.content = attribute.Attribute(self.Length, data[4:])
    
class PDU :
    def __init__(self,data) :
        header = int.from_bytes(data[:3],'little')
        self.LLID = header & 3
        self.NESN = (header >> 3) & 1
        self.SN = (header >> 4) & 1
        self.MD = (header >> 5) & 1
        self.CP = (header >> 6) & 1
        self.Length = (header >> 8) & 0xff
        bits = 'MD:%d, CP:%d, Length:%d'%(self.MD,self.CP,self.Length)
        if self.CP :
            self.header = data[:3]
            self.CteInfo = header >> 16
            self.payload = data[3:][:self.Length]
        else :
            self.header = data[:2]
            self.payload = data[2:][:self.Length]
        name = '!'
        if 0 == self.LLID :
            raise RuntimeError
        elif 1 == self.LLID :
            if 0 == self.Length :
                self.content = Empty_PDU()
            else :
                raise RuntimeError
        elif 2 == self.LLID :
            self.content = L2CAP(self.payload)
        elif 3 == self.LLID :
            self.content = LL_Control(self.payload)
        print(self.content.__str__())
