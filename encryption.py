from Cryptodome.Cipher import AES

# Core 6.1 | Vol 3, Part H 2.2.1 Security function e
# Core 6.1 | Vol 6 5.1.3.1 Encryption Start Procedure
# Core 6.1 | Vol 6, Part E 2 CCM
# Core 6.1 | Vol 6, Part E 1 Encryption Sample Data (p3235)

LE = 'little'
BE = 'big'

LTK = 0x4C68384139F574D836BCF34E9DFB01BF
EDIV = 0x2474
RAND = 0xABCDEF1234567890
SKD_C = 0xACBDCEDFE0F10213
SKD_P = 0x0213243546576879
IV_C = 0xBADCAB24
IV_P = 0xDEAFBABE

def hexdump(b) :
    return ':'.join(['%02X'%(x) for x in b])

def le16(int128) :
    return int128.to_bytes(16,LE)

def be16(int128) :
    return int128.to_bytes(16,BE)

IV = (IV_P << 32) | IV_C
print('IV: %016x, %s'%(IV,hexdump(IV.to_bytes(8,LE))))

SKD = (SKD_P << 64) | SKD_C
print('SKD: %032x, %s'%(SKD,hexdump(le16(SKD))))
print('LTK: %032x, %s'%(LTK,hexdump(le16(LTK))))

cipher = AES.new(be16(LTK), AES.MODE_ECB)
ciphertext = cipher.encrypt(be16(SKD))
print('ciphertext: %s'%(hexdump(ciphertext)))
SK = int.from_bytes(ciphertext,LE)

class CCM :
    def __init__(self, isCentral, IV) :
        self.packetCounter = 0
        self.IV = IV
        if isCentral :
            self.directionBit = 1
        else :
            self.directionBit = 0
    def nonce(self) :
        pcdb = self.packetCounter & 0x7ffffffff
        pcdb |= self.directionBit << 39
        return pcdb.to_bytes(5,LE) + IV.to_bytes(8,LE)
    def B0(self, Length) :
        return bytes([0x49]) + self.nonce() + (Length & 0xff).to_bytes(2,BE)
    def B1(self,AAD) :
        return bytes([0x00,0x01,AAD,0,0,0,0,0,0,0,0,0,0,0,0,0])
    def Ai(self,i) :
        return bytes([0x01]) + self.nonce() + (i & 0xffff).to_bytes(2,BE)

# RSP1 p3238
ccm = CCM(1,IV)
print("B0: %s"%(hexdump(ccm.B0(1))))
print("B1: %s"%(hexdump(ccm.B1(3))))
print("A0: %s"%(hexdump(ccm.Ai(0))))
print("A1: %s"%(hexdump(ccm.Ai(1))))
print("nonce: %s"%(hexdump(ccm.nonce())))

cipher = AES.new(le16(SK), AES.MODE_CCM, nonce=ccm.nonce(), mac_len=4)
cipher.update(bytes([3]))
ciphertext,tag = cipher.encrypt_and_digest(bytes([6]))
print("ciphertext: %s"%(hexdump(ciphertext)))
print("tag: %s"%(hexdump(tag)))

# RSP2 p3239
ccm = CCM(0,IV)
print("B0: %s"%(hexdump(ccm.B0(1))))
print("B1: %s"%(hexdump(ccm.B1(3))))
print("A0: %s"%(hexdump(ccm.Ai(0))))
print("A1: %s"%(hexdump(ccm.Ai(1))))
print("nonce: %s"%(hexdump(ccm.nonce())))

cipher = AES.new(le16(SK), AES.MODE_CCM, nonce=ccm.nonce(), mac_len=4)
cipher.update(bytes([3]))
ciphertext,tag = cipher.encrypt_and_digest(bytes([6]))
print("ciphertext: %s"%(hexdump(ciphertext)))
print("tag: %s"%(hexdump(tag)))
