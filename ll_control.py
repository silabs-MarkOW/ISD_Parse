class LL_Control :
  def __str__(self) :
    pairs = []
    for key in self.__dict__:
      pairs.append('%s:%s'%(key,self.__dict__[key].__str__()))
    return type(self).__name__ + ': '+', '.join(pairs)
  
class LL_CONNECTION_UPDATE_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CHANNEL_MAP_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_TERMINATE_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_ENC_REQ(LL_Control) :
  def __init__(self, data) :
    self.Rand = int.from_bytes(data[:8],'little')
    self.EDIV = int.from_bytes(data[8:10],'little')
    self.SKD_C = int.from_bytes(data[10:18],'little')
    self.IV_C = int.from_bytes(data[18:22],'little')
  def __str__(self) :
    return 'LL_ENC_REQ: Rand:0x%016x, EDIV:0x%04x, SKD_C:0x%016x, IV_C:0x%08x'%(self.Rand,self.EDIV,self.SKD_C,self.IV_C)
  
class LL_ENC_RSP(LL_Control) :
  def __init__(self, data) :
    self.SKD_P = int.from_bytes(data[:8],'little')
    self.IV_P = int.from_bytes(data[8:12],'little')
  def __str__(self) :
    return 'LL_ENC_RSP: SKD_P:0x%016x, IV_P:0x%08x'%(self.SKD_P,self.IV_P)

class LL_START_ENC_REQ(LL_Control) :
  def __init__(self, data) :
    pass
  def __str__(self) :
    return 'LL_START_ENC_REQ'  

class LL_START_ENC_RSP(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_UNKNOWN_RSP(LL_Control) :
  def __init__(self, data) :
    self.UnknownType = data[0]

class LL_FEATURE_REQ(LL_Control) :
    def __init__(self,data) :
        self.FeatureSet = int.from_bytes(data[:8],'little')
        
class LL_FEATURE_RSP(LL_Control) :
    def __init__(self,data) :
        self.FeatureSet = int.from_bytes(data[:8],'little')

class LL_PAUSE_ENC_REQ(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_PAUSE_ENC_RSP(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_VERSION_IND(LL_Control) :
  def __init__(self, data) :
        self.Version = data[0]
        self.Company_Identifier = int.from_bytes(data[1:3],'little')
        self.Subversion = int.from_bytes(data[3:5],'little')
        print('Version:%d, Company_Identifier:0x%x, Subversion:%d'%(self.Version, self.Company_Identifier, self.Subversion))


class LL_REJECT_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_PERIPHERAL_FEATURE_REQ(LL_Control) :
    def __init__(self,data) :
        self.FeatureSet = int.from_bytes(data[:8],'little')
        
class LL_CONNECTION_PARAM_REQ(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CONNECTION_PARAM_RSP(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_REJECT_EXT_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_PING_REQ(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_PING_RSP(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_LENGTH_REQ(LL_Control) :
  def __init__(self, data) :
    self.MaxRxOctets = int.from_bytes(data[:2],'little')
    self.MaxRxTime = int.from_bytes(data[2:4],'little')
    self.MaxTxOctets = int.from_bytes(data[4:6],'little')
    self.MaxTxTime = int.from_bytes(data[6:8],'little')

class LL_LENGTH_RSP(LL_Control) :
  def __init__(self, data) :
    self.MaxRxOctets = int.from_bytes(data[:2],'little')
    self.MaxRxTime = int.from_bytes(data[2:4],'little')
    self.MaxTxOctets = int.from_bytes(data[4:6],'little')
    self.MaxTxTime = int.from_bytes(data[6:8],'little')

class LL_PHY_REQ(LL_Control) :
  def __init__(self, data) :
    self.TX_PHYS = data[0]
    self.RX_PHYs = data[1]

class LL_PHY_RSP(LL_Control) :
  def __init__(self, data) :
    self.TX_PHYS = data[0]
    self.RX_PHYs = data[1]

class LL_PHY_UPDATE_IND(LL_Control) :
  def __init__(self, data) :
    self.PHY_C_TO_P = data[0]
    self.PHY_P_TO_C = data[1]

class LL_MIN_USED_CHANNELS_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CTE_REQ(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CTE_RSP(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_PERIODIC_SYNC_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CLOCK_ACCURACY_REQ(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CLOCK_ACCURACY_RSP(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CIS_REQ(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CIS_RSP(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CIS_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CIS_TERMINATE_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_POWER_CONTROL_REQ(LL_Control) :
  def __init__(self, data) :
    self.PHY = data[0]
    self.Delta = data[1]
    self.TxPower = data[2]
    print('%s: PHY:%d, Delta:%d, TxPower:%d'%(type(self).__name__,self.PHY,self.Delta,self.TxPower))


class LL_POWER_CONTROL_RSP(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_POWER_CHANGE_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_SUBRATE_REQ(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_SUBRATE_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CHANNEL_REPORTING_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CHANNEL_STATUS_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_PERIODIC_SYNC_WR_IND(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))

class LL_FEATURE_EXT_REQ(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))

class LL_FEATURE_EXT_RSP(LL_Control) :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))

class LL_CS_SEC_RSP(LL_Control) :
  def __init__(self, data) :
    self.CS_IV_P = int.from_bytes(data[:8],'little')
    self.CS_IN_P = int.from_bytes(data[8:12],'little')
    self.CS_PV_P = int.from_bytes(data[12:20],'little')

def bit(i,value) :
  return (value >> i) & 1

class LL_CS_CAPABILITIES(LL_Control) :
  def __init__(self, data) :
    self.Mode_Types = data[0]
    self.RTT_Capability = data[1]
    self.RTT_AA_Only_N = data[2]
    self.RTT_Sounding_N = data[3]
    self.RTT_Random_Sequence_N = data[4]
    self.NADM_Sounding_Capability = int.from_bytes(data[5:7],'little')
    self.NADM_Random_Capability = int.from_bytes(data[7:9],'little')
    self.CS_SYNC_PHY_Capability = data[9]
    self.Num_Ant = data[10] & 0xf
    self.Max_Ant_Path = (data[10] >> 4) & 0xf
    self.Role = data[11] & 3
    self.No_FAE = bit(3,data[11])
    self.Channel_Selection_number3C = bit(4,data[11])
    self.Sounding_PCT_Estimate = bit(5,data[11])
    self.Num_Configs = data[12]
    self.Max_Procedures_Supported = int.from_bytes(data[13:15],'little')
    self.T_SW = data[15]
    self.T_IP1_Capability = int.from_bytes(data[16:18],'little')
    self.T_IP2_Capability = int.from_bytes(data[18:20],'little')
    self.T_FCS_Capability = int.from_bytes(data[20:22],'little')
    self.T_PM_Capability = int.from_bytes(data[22:24],'little')
    self.TX_SNR_Capability = data[24] >> 1

class LL_CS_CAPABILITIES_REQ(LL_CS_CAPABILITIES) :
  def d__init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))

class LL_CS_CAPABILITIES_RSP(LL_CS_CAPABILITIES) :
  def d__init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))

class LL_CS_CONFIG_REQ(LL_Control) :
  def __init__(self, data) :
    self.Config_ID = data[0] & 0x3f
    self.Action = (data[0] >> 6) & 3
    self.ChM = int.from_bytes(data[1:11])
    self.ChM_Repetition = data[11]
    self.Main_Mode = data[12]
    self.Sub_Mode = data[13]
    self.Main_Mode_Min_Steps = data[14]
    self.Main_Mode_Max_Steps = data[15]
    self.Main_Mode_Repetition = data[16]
    self.Mode_0_Steps = data[17]
    self.CS_SYNC_PHY = data[18]
    self.RTT_Type = data[19] & 0xf
    self.Role = (data[19] >> 4) & 3
    self.ChSel = data[20] & 0xf
    self.Ch3cShape = (data[20] >> 4) & 0xf
    self.T_IP1 = data[21]
    self.T_IP2 = data[22]
    self.T_FCS = data[23]
    self.T_PM = data[24]
    
class LL_CS_CONFIG_RSP :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CS_REQ :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CS_RSP :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CS_IND :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CS_TERMINATE_REQ :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CS_FAE_REQ :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CS_FAE_RSP :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CS_CHANNEL_MAP_IND :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_CS_SEC_REQ(LL_Control) :
  def __init__(self, data) :
    self.CS_IV_C = int.from_bytes(data[:8],'little')
    self.CS_IN_C = int.from_bytes(data[8:12],'little')
    self.CS_PV_C = int.from_bytes(data[12:20],'little')

class LL_CS_TERMINATE_RSP :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_FRAME_SPACE_REQ :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))


class LL_FRAME_SPACE_RSP :
  def __init__(self, data) :
    raise RuntimeError('%s not implemented'%(type(self).__name__))

LL_Control_PDUs = {
  0x00: LL_CONNECTION_UPDATE_IND,
  0x01: LL_CHANNEL_MAP_IND,
  0x02: LL_TERMINATE_IND,
  0x03: LL_ENC_REQ,
  0x04: LL_ENC_RSP,
  0x05: LL_START_ENC_REQ,
  0x06: LL_START_ENC_RSP,
  0x07: LL_UNKNOWN_RSP,
  0x08: LL_FEATURE_REQ,
  0x09: LL_FEATURE_RSP,
  0x0a: LL_PAUSE_ENC_REQ,
  0x0b: LL_PAUSE_ENC_RSP,
  0x0c: LL_VERSION_IND,
  0x0d: LL_REJECT_IND,
  0x0e: LL_PERIPHERAL_FEATURE_REQ,
  0x0f: LL_CONNECTION_PARAM_REQ,
  0x10: LL_CONNECTION_PARAM_RSP,
  0x11: LL_REJECT_EXT_IND,
  0x12: LL_PING_REQ,
  0x13: LL_PING_RSP,
  0x14: LL_LENGTH_REQ,
  0x15: LL_LENGTH_RSP,
  0x16: LL_PHY_REQ,
  0x17: LL_PHY_RSP,
  0x18: LL_PHY_UPDATE_IND,
  0x19: LL_MIN_USED_CHANNELS_IND,
  0x1a: LL_CTE_REQ,
  0x1b: LL_CTE_RSP,
  0x1c: LL_PERIODIC_SYNC_IND,
  0x1d: LL_CLOCK_ACCURACY_REQ,
  0x1e: LL_CLOCK_ACCURACY_RSP,
  0x1f: LL_CIS_REQ,
  0x20: LL_CIS_RSP,
  0x21: LL_CIS_IND,
  0x22: LL_CIS_TERMINATE_IND,
  0x23: LL_POWER_CONTROL_REQ,
  0x24: LL_POWER_CONTROL_RSP,
  0x25: LL_POWER_CHANGE_IND,
  0x26: LL_SUBRATE_REQ,
  0x27: LL_SUBRATE_IND,
  0x28: LL_CHANNEL_REPORTING_IND,
  0x29: LL_CHANNEL_STATUS_IND,
  0x2a: LL_PERIODIC_SYNC_WR_IND,
  0x2b: LL_FEATURE_EXT_REQ,
  0x2c: LL_FEATURE_EXT_RSP,
  0x2d: LL_CS_SEC_RSP,
  0x2e: LL_CS_CAPABILITIES_REQ,
  0x2f: LL_CS_CAPABILITIES_RSP,
  0x30: LL_CS_CONFIG_REQ,
  0x31: LL_CS_CONFIG_RSP,
  0x32: LL_CS_REQ,
  0x33: LL_CS_RSP,
  0x34: LL_CS_IND,
  0x35: LL_CS_TERMINATE_REQ,
  0x36: LL_CS_FAE_REQ,
  0x37: LL_CS_FAE_RSP,
  0x38: LL_CS_CHANNEL_MAP_IND,
  0x39: LL_CS_SEC_REQ,
  0x3a: LL_CS_TERMINATE_RSP,
  0x3b: LL_FRAME_SPACE_REQ,
  0x3c: LL_FRAME_SPACE_RSP
}
