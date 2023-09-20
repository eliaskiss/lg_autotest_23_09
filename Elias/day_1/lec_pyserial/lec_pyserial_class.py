import serial
from icecream import ic
import sys

ic.configureOutput(includeContext=True)

class MySerial:
    def __init__(self, port=None):
        self.ser = None

        if port is not None:
            self.openSerial(port)

    def __str__(self):
        return f'Port:{self.ser.port}, Baudrate:{self.ser.baudrate}'

    #############################################################
    # Open Serial
    #############################################################
    def openSerial(self, port, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False,
                   dsrdtr=False):
        # 시리얼 포트객체 생성
        self.ser = serial.Serial()

        # 시리얼 포트설정
        self.ser.port = port  # Port Name: COM2, COM3, ...
        self.ser.baudrate = baudrate  # Baudrate 속도
        self.ser.bytesize = bytesize  # Data Bit
        self.ser.parity = parity  # Check Parity
        self.ser.stopbits = stopbits  # Stopbits
        self.ser.timeout = timeout  # None: 무한대기, 0: Non-blocking mode, n: n초 대기
        self.ser.xonxoff = xonxoff  # SW Flow Control
        self.ser.rtscts = rtscts  # RTS/CTS Flow Control
        self.ser.dsrdtr = dsrdtr  # DSR/DTR Flow Control

        # 시리얼 포트 열기
        self.ser.open()

    #############################################################
    # Write Port
    #############################################################
    def writePort(self, data):
        self.ser.write(data)

    def writePortUnicode(self, data):
        self.writePort(data.encode())

    #############################################################
    # Read Port
    #############################################################
    def read(self, size=1, timeout=None):
        self.ser.timeout = timeout
        readed = self.ser.read(size)
        return readed

    #############################################################
    # Read until EOF (putty EOF : Ctrl + J)
    #############################################################
    def readEOF(self):
        readed = self.ser.readline()
        return readed[:-1]

    #############################################################
    # Ctrl + C 가 들어올때까지 Read
    #############################################################
    def readuntilExitCode(self, code=b'\x03'):
        readed = b''
        while True:
            data = self.ser.read()
            ic(data)
            readed += data

            if data == code:
                return readed[:-1]

    #############################################################
    # Close Port
    #############################################################
    def closeSerial(self):
        if self.ser is not None:
            self.ser.close()
            self.ser = None

if __name__ == '__main__':
    ser = MySerial('COM2')
    print(ser)

    # 포트쓰기
    ser.writePortUnicode('안녕 세상아~')

    # 포트 쓰기
    ser.writePort(ser, 'HelloWorld\r\n'.encode())
    ser.writePortUnicode(ser, 'HelloWorld\r\n')
    ser.writePortUnicode(ser, '안녕 세상아~~\r\n')

    # 포트 읽기
    # Read 1byte : 1byte만 읽고 retrun
    ic(ser.read())

    # Read 10 bytes : 10bytes 읽고서 return
    ic(ser.read(10))

    # Read with timeout 5 seconds : 5초 대기한 후에 데이터가 없으면 return
    ic(ser.read(1, 5))
    ic(ser.read(size=1, timeout=5))

    # Read Until EOF
    ic(ser.readEOF())

    # Read Until Exit Code (Ctrl + C)
    ic(ser.readuntilExitCode())

    # 포트 닫기
    ser.closeSerial()

























