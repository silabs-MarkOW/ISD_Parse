now = 0
windows = []
keep_missed = False
missed = []

def timestr(t) :
    if abs(t) < 1e-3 :
        return "%.0f us"%(t*1e6)
    if abs(t) < 1 :
        return "%.3f ms"%(t*1e3)
    return "%.6f s"%(t)

class Window :
    def __init__(self,start,stop,owner,label=None) :
        self.start = start
        self.stop = stop
        self.owner = owner
        self.handled = False
        self.keep_missed = keep_missed
        self.label = label
        print('Window: %.4f - %.4f s'%(start,stop),owner)
    def delta(self,value) :
        if value < self.start :
            return self.start - value
        if value > self.stop :
            return value - self.stop
        return 0
    def below(self,value) :
        return self.stop < value
    def process(self,data,channel,SyncWord,isTx,debug=False) :
        if debug :
            print("window.process: %s (%s)"%(timestr(now),timestr(now-self.start)),self.owner)
        ret = self.owner.process(data,channel,SyncWord,self)
        if None != ret :
            self.handled = True
        return ret
    def __str__(self) :
        s = "%.1f ms to %.1f ms: "%(1000*(self.start-now),1e3*(self.stop-now))
        s += self.owner.__str__()
        if None != self.label :
            s += ', label:%s'
        return s
    
def update(timestamp, duration) :
    global now, length, windows
    print("scheduling.update(timestamp:%s,duration:%s) %s"%(timestr(timestamp),timestr(duration),timestr(timestamp-now)))
    active = []
    pending = []
    now = timestamp
    length = duration
    for window in windows :
        if window.handled : continue
        if window.below(now-500e-6) :
            pending.append(window)
        else :
            active.append(window)
    windows = active
    for window in pending :
        print(window,'missed by',timestr(window.delta(now)))
        window.owner.on_missed()
    if keep_missed :
        missed += pending

def schedule(offset,length,owner,label=None) :
    print("scheduling.schedule(offset:%s,length:%s,%s)"%(timestr(offset),timestr(length),owner.__str__()))
    start = now + offset
    stop = start + length
    windows.append(Window(start,stop,owner,label))
        
def expect(sloppiness) :
    expected = []
    closest = None
    print('windows:',windows)
    for window in windows :
        if not window.handled :
            delta = window.delta(now)
            if 0 == delta :
                expected.append(window)
            else :
                if None == closest :
                    closest  = window
                    cached = delta
                else :
                    if delta < cached :
                        cached = delta
                        closest = window
    if None != closest and cached <= sloppiness :
        print('including',closest)
        expected.append(closest)
    return expected

def get_next(owner) :
    for window in windows :
        if window.owner == owner :
            return window.start
    print(windows)
    raise RuntimeError(owner)
