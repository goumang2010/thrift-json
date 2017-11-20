class DataType:
    STOP = 0
    VOID = 1
    BOOL = 2
    BYTE = 3
    I08 = 3
    DOULE = 4
    I16 = 6
    I32 = 8
    I64 = 10
    STRING = 11
    UTF7 = 11
    STRUCT = 12
    MAP = 13
    SET = 14
    LIST = 15
    UTF8 = 16
    UTF16 = 17

    VALUES_TO_NAMES = ('STOP',
                       'VOID',
                       'BOOL',
                       'I08',
                       'DOUBLE',
                       None,
                       'I16',
                       None,
                       'I32',
                       None,
                       'I64',
                       'STRING',
                       'STRUCT',
                       'MAP',
                       'SET',
                       'LIST',
                       'UTF8',
                       'UTF16')

    VALUES_TO_TYPES = (None,
                       None,
                       bool,
                       bytes,
                       float,
                       None,
                       int,
                       None,
                       int,
                       None,
                       int,
                       unicode,
                       dict,
                       dict,
                       set,
                       list,
                       unicode,
                       unicode
                       )

    basicDataIndex = [2, 3, 4, 6, 8, 10, 11]
    basicDataType = [BOOL, BYTE, I08, DOULE, I16, I32, I64, STRING]


class MessageType:
    CALL = 1
    REPLY = 2
    EXCEPTION = 3
    ONEWAY = 4


class TransportType:
    TFramedTransport = "TFramedTransport"
    TBufferedTransport = "TBufferedTransport"