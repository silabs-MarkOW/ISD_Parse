import scheduling
import data
import advertising

class Connection :
    def __init__(self, request) :
        print("Connection.__init__(%s)"%(type(request)))
        self.request = request
        self.state = 'first'
        if advertising.AUX_CONNECT_REQ == type(request) :
            delay = 2.5e-3 # not true for Coded PHY
            anchor = request.timestamp
        elif advertising.CONNECT_IND == type(request) :
            delay = 1.25e-3
            anchor = scheduling.now
        else :
            raise RuntimeError(type(request))
        self.anchor = anchor + delay + request.LLData.WinOffset
        self.anchor_instant = 0
        self.count = 0
        self.interval = request.LLData.Interval
        self.timeout = request.LLData.Timeout
        if advertising.CONNECT_IND == type(request) :
            self.schedule()
    def schedule(self) :
        print("Connection.schedule")
        scheduling.schedule(self.anchor - scheduling.now,self.request.LLData.WinSize,self)
    def process(self,packet,channel,aa,window) :
        if aa != self.request.LLData.AA :
            return None
        if 'First' == window.label :
            self.state = 'first'
        scheduling.schedule(scheduling.length+150e-6-50e-6,100e-6,self)
        if 'first' == self.state :
            delta = scheduling.now - self.anchor
            intervals = int(round(delta / self.interval))
            print('Connection.process: delta:',delta)
            if 0 == self.count :
                self.anchor = scheduling.now - self.interval * intervals
                print("Updated anchor: %f"%(self.anchor))
            self.state = 'connected'
            print('------------------------------')
            print('self.interval: ',self.interval)
            print(self.anchor)
            scheduling.schedule(self.anchor - scheduling.now + self.interval * (intervals+1)-100e-6,500e-6,self,label='First')
            self.count += 1
        return data.PDU(packet)
    def on_missed(self) :
        pass
    #raise RuntimeError(scheduling.now,scheduling.now-self.anchor)
