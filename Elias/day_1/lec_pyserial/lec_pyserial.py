import serial
from icecream import ic
import time

ic.configureOutput(includeContext=True)

#############################################################
# Open Serial
#############################################################
def openSerial(port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False,
               dsrdtr=False):
    # 시리얼 포트객체 생성
    ser = serial.Serial()

    # 시리얼 포트설정
    ser.port = port             # Port Name: COM2, COM3, ...
    ser.baudrate = baudrate     # Baudrate 속도
    ser.bytesize = bytesize     # Data Bit
    ser.parity = parity         # Check Parity
    ser.stopbits = stopbits     # Stopbits
    ser.timeout = timeout       # None: 무한대기, 0: Non-blocking mode, n: n초 대기
    ser.xonxoff = xonxoff       # SW Flow Control
    ser.rtscts = rtscts         # RTS/CTS Flow Control
    ser.dsrdtr = dsrdtr         # DSR/DTR Flow Control

    # 시리얼 포트 열기
    ser.open()

    # 객체생성과 동시에 포트열기
    # ser = serial.Serial(port, baudrate, ...)

    return ser

#############################################################
# Write Port
#############################################################
def writePort(ser, data):
    ser.write(data)

def writePortUnicode(ser, data):
    ser.write(data.encode())

#############################################################
# Read Port
#############################################################
def read(ser, size=1, timeout=None):
    ser.timeout = timeout
    readed = ser.read(size)
    return readed


if __name__ == '__main__':
    ser = openSerial('COM2')

    # # 포트 쓰기
    # writePort(ser, 'HelloWorld\r\n'.encode())
    # writePortUnicode(ser, 'HelloWorld\r\n')

    # # 포트 읽기
    # # Read 1byte : 1byte만 읽고서 return
    # ic(read(ser))

    # # Read 10byte : 10byte 읽고서 return
    # ic(read(ser, 10))

    # Read with timeout 5 seconds : 5초 대기한 후에 데이터가 없으면 return
    ic(read(ser, 1, 5))
    # ic(read(ser, timeout=5, size=1))













