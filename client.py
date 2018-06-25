from ctypes import util, CDLL, CFUNCTYPE, POINTER, c_void_p, c_char_p
from ctypes import c_bool, c_int
# import ctypes.util
# import ctypes
print(util.find_library('iec60870'))
iec60870 = CDLL('/usr/local/lib/libiec60870.so')


# ASDU_getTypeID
iec60870.ASDU_getTypeID.argtypes = [c_void_p]
iec60870.ASDU_getTypeID.restype = c_void_p


# ASDU_getNumberOfElements
iec60870.ASDU_getNumberOfElements.argtypes = [c_void_p]
iec60870.ASDU_getNumberOfElements.restype = c_int

# TypeID_toString
iec60870.TypeID_toString.argtypes = [c_void_p]
iec60870.TypeID_toString.restype = c_char_p

# ASDU_getElement
iec60870.ASDU_getElement.argtypes = [c_void_p, c_int]
iec60870.ASDU_getElement.restype = c_void_p

# InformationObject_getObjectAddress
iec60870.InformationObject_getObjectAddress.argtypes = [c_void_p]
iec60870.InformationObject_getObjectAddress.restype = c_int

# SinglePointInformation_getValue
iec60870.SinglePointInformation_getValue.argtypes = [c_void_p]
iec60870.SinglePointInformation_getValue.restype = c_bool

# SinglePointInformation_destroy
iec60870.SinglePointInformation_destroy.argtypes = [c_void_p]


def connectionHandler(parameter, con, event):
    if int(event) == 0:
        print(str(event), "Connection established")
    elif int(event) == 1:
        print(str(event), "Connection closed")
    elif int(event) == 2:
        print(str(event), "Connection startDT CON RECEIVED")
    elif int(event) == 3:
        print(str(event), "Connection stopDT CON RECEIVED")


def asduReceivedHandler(parameter, asdu):
    print("In Asdu Handler", iec60870.ASDU_getNumberOfElements(asdu))
    # print("Numbers of Elements:", iec60870.ASDU_getNumberOfElements(asdu))
    # print("Type ID:", iec60870.ASDU_getTypeID(asdu))
    # print("String ID:", iec60870.TypeID_toString(iec60870.ASDU_getTypeID(asdu)))
    asduType = iec60870.TypeID_toString(iec60870.ASDU_getTypeID(asdu))
    asduType = asduType.decode("utf-8")
    if asduType == 'M_SP_NA_1':
        for el in range(iec60870.ASDU_getNumberOfElements(asdu)):
            io = iec60870.ASDU_getElement(asdu, int(el))
            ioa = iec60870.InformationObject_getObjectAddress(io)
            value = iec60870.SinglePointInformation_getValue(io)
            print(ioa, value)
            iec60870.SinglePointInformation_destroy(io)
    # io = iec60870.ASDU_getElement(asdu, c_int(0))
    # print("Object Address", iec60870.InformationObject_getObjectAddress(io), io)
    # print(iec60870.SinglePointInformation_getValue(io))


# asduConnectionHandler Proto:
asduReceivedHandlerProto = CFUNCTYPE(c_bool, POINTER(c_void_p), POINTER(c_void_p))
asduHandler = asduReceivedHandlerProto(asduReceivedHandler)

# T104Connection_setASDUReceivedHandler ini
iec60870.T104Connection_setASDUReceivedHandler.argtypes = [c_void_p, asduReceivedHandlerProto, c_int]

# T104Connection_create init
iec60870.T104Connection_create.argtypes = [c_char_p, c_int]
iec60870.T104Connection_create.restype = c_void_p


# T104Connection_destroy init
iec60870.T104Connection_destroy.argtypes = [c_void_p]

# Thread_sleep init:
iec60870.Thread_sleep.argtypes = [c_int]

# connectionHandler Proto:
conHandlerProto = CFUNCTYPE(c_void_p, POINTER(c_void_p), POINTER(c_void_p), c_int)
handler = conHandlerProto(connectionHandler)

# T104Connection_sendStartDT
iec60870.T104Connection_sendStartDT.argtypes = [c_void_p]

# T104Connection_sendStopDT
iec60870.T104Connection_sendStopDT.argtypes = [c_void_p]

# T104Connection_setConnectionHandler ini
iec60870.T104Connection_setConnectionHandler.argtypes = [c_void_p, conHandlerProto, c_int]

# T104Connection_sendInterrogationCommand init
iec60870.T104Connection_sendInterrogationCommand.argtypes = [c_void_p, c_int, c_int, c_int]
iec60870.T104Connection_sendInterrogationCommand.restype = c_bool

# T104Connection_sendReadCommand
iec60870.T104Connection_sendReadCommand.argtypes = [c_void_p, c_int, c_int]
iec60870.T104Connection_sendReadCommand.restype = c_bool

# T104Connection_sendTestCommand
iec60870.T104Connection_sendTestCommand.argtypes = [c_void_p, c_int]
iec60870.T104Connection_sendTestCommand.restype = c_bool


con = iec60870.T104Connection_create(b'10.151.42.71', 2404)
# iec60870.T104Connection_setConnectionHandler(con, handler, c_int())
# iec60870.T104Connection_setASDUReceivedHandler(con, asduHandler, c_int())
isConnect = iec60870.T104Connection_connect(con)
print(isConnect)
if isConnect:
    iec60870.T104Connection_sendStartDT(con)
    iec60870.Thread_sleep(c_int(3000))
    input("Waiting... ")
# iec60870.T104Connection_sendInterrogationCommand(con, 6, 2, 20)
# iec60870.T104Connection_sendReadCommand(con, 1, 66)
# iec60870.T104Connection_sendTestCommand(con, 1)
# iec60870.Thread_sleep(4000)
iec60870.T104Connection_sendStopDT(con)
iec60870.T104Connection_destroy(con)
