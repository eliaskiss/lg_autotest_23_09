from lec_pyserial_class import MySerial

# Echo Program

RECODE_CODE = b'\x0d'
ser = MySerial()
ser.openSerial('COM2')

print('Program is running...')

# while True:
#     # 'COM2'로부터 1byte씩 읽어서 그 데이터를 다시 쓰기
#     pass


while True:
    # 'COM2'로부터 라인단위로 읽어서 그 데이터를 다시 쓰기
    pass