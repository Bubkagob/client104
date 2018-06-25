from ctypes import util, CDLL, CFUNCTYPE, POINTER, c_void_p, c_char_p, c_int
from ctypes import c_bool, c_float

print(util.find_library('iec60870'))
iec60870 = CDLL('/usr/local/lib/libiec60870.so')

# T104Connection_create:
iec60870.T104Connection_create.argtypes = [c_char_p, c_int]
iec60870.T104Connection_create.restype = c_void_p

# T104Connection_connect:
iec60870.T104Connection_connect.argtypes = [c_void_p]
iec60870.T104Connection_connect.restype = c_bool

# Thread_sleep
iec60870.Thread_sleep.argtypes = [c_int]

# connection_handler proto
handler_proto = CFUNCTYPE(
    c_void_p,
    POINTER(c_void_p),
    POINTER(c_void_p),
    c_int
)

# T104Connection_setConnectionHandler ini
iec60870.T104Connection_setConnectionHandler.argtypes = [
    c_void_p,
    handler_proto,
    c_int
]

# ASDU handler Prototype
asdu_handler_proto = CFUNCTYPE(c_bool, POINTER(c_void_p), POINTER(c_void_p))

# T104Connection_setASDUReceivedHandler ini
iec60870.T104Connection_setASDUReceivedHandler.argtypes = [
    c_void_p,
    asdu_handler_proto,
    c_int
]

# T104Connection_sendStartDT
iec60870.T104Connection_sendStartDT.argtypes = [c_void_p]

# ASDU_getTypeID
iec60870.ASDU_getTypeID.argtypes = [c_void_p]
iec60870.ASDU_getTypeID.restype = c_void_p

# ASDU_getElement
iec60870.ASDU_getElement.argtypes = [c_void_p, c_int]
iec60870.ASDU_getElement.restype = c_void_p

# TypeID_toString
iec60870.TypeID_toString.argtypes = [c_void_p]
iec60870.TypeID_toString.restype = c_char_p

# InformationObject_getObjectAddress
iec60870.InformationObject_getObjectAddress.argtypes = [c_void_p]
iec60870.InformationObject_getObjectAddress.restype = c_int

# MeasuredValueScaled_getValue
iec60870.MeasuredValueScaled_getValue.argtypes = [c_void_p]
iec60870.MeasuredValueScaled_getValue.restype = c_int

# MeasuredValueShort_getValue
iec60870.MeasuredValueShort_getValue.argtypes = [c_void_p]
iec60870.MeasuredValueShort_getValue.restype = c_float

# SinglePointInformation_getValue
iec60870.SinglePointInformation_getValue.argtypes = [c_void_p]
iec60870.SinglePointInformation_getValue.restype = c_bool


class Client():
    b_run = False

    def __init__(self, ip, port):
        self.ip = ip.encode()
        self.port = port
        self.isConnect = False
        self.con = False
        self.c_con_handler = handler_proto(self.connection_handler)
        self.c_asdu_handler = asdu_handler_proto(self.asdu_handler)

    def run(self):
        print("Is Connect? :", self.isConnect)
        self.createConnection()
        self.install_handlers()
        self.connect()
        self.start_dt()
        input("Press any key")

    def connection_handler(self, parameter, con, event):
        print("Event ", int(event))
        if int(event) == 1:
            self.isConnect = iec60870.T104Connection_connect(self.con)
            print(self.isConnect)
            print("Catch closed connection")
            self.reconnect()
            self.start_dt()

    def start_dt(self):
        iec60870.T104Connection_sendStartDT(self.con)
        iec60870.Thread_sleep(200)
        self.b_run = True

    def asdu_handler(self, parameter, asdu):
        print("In ASDU Handler")
        asdu_type = iec60870.TypeID_toString(iec60870.ASDU_getTypeID(asdu)).decode("utf-8")
        print("Main Type ---- ", asdu_type)
        if asdu_type == 'M_ME_NC_1':
            io = iec60870.ASDU_getElement(asdu, 0)
            ioa = iec60870.InformationObject_getObjectAddress(io)
            print("Object address :", ioa)
            val = iec60870.MeasuredValueShort_getValue(io)
            print("Value =", val)
        elif asdu_type == 'M_ME_TC_1':
            print("catch Again")
        elif asdu_type == 'M_SP_NA_1':
            io = iec60870.ASDU_getElement(asdu, 0)
            ioa = iec60870.InformationObject_getObjectAddress(io)
            val = iec60870.SinglePointInformation_getValue(io)
            self.v = 1213
            print("Bool ", ioa, val)

    def install_handlers(self):
        print("Install Handlers")
        iec60870.T104Connection_setConnectionHandler(
            self.con,
            self.c_con_handler,
            c_int()
        )
        iec60870.T104Connection_setASDUReceivedHandler(
            self.con,
            self.c_asdu_handler,
            c_int()
        )

    def connect(self):
        self.isConnect = iec60870.T104Connection_connect(self.con)
        if self.isConnect is not True:
            for i in range(13):
                print("Trying ...", i, self.isConnect)
                self.isConnect = iec60870.T104Connection_connect(self.con)
                iec60870.Thread_sleep(1000)
                if self.isConnect:
                    return True
            return False
        return True

    def reconnect(self):
        print("In Reconnect")

    def createConnection(self):
        try:
            self.con = iec60870.T104Connection_create(self.ip, self.port)
        except Exception as e:
            print("Cannot create a new connection", e)
