class Attribute :
    def __init__(self, length, data) :
        opcode = data[0]
        self.Method = opcode & 0x1f
        self.CommandFlag = (opcode >> 6) & 1
        self.AuthenticationSignatureFlag = (opcode >> 7) & 1
        if self.AuthenticationSignatureFlag :
            self.AttributeParameters = data[1:-12]
        else :
            self.AttributeParameters = data[1:]
    def __str__(self) :
        return 'Attribute: Method:0x%x'%(self.Method)
