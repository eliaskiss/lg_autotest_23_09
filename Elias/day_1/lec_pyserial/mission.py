from lec_pyserial_class import MySerial

# Echo Program

RETURN_CODE = b'\x0d'
ser = MySerial()
ser.openSerial('COM2')

print('Program is running...')

# while True:
#     # Enter키가 입력될때까지의 데이터를 읽기
#     readed = ser.read()
#
#     # 읽어온 데이터 출력
#     print('Readed byte string:', readed)
#
#     # byte array -> Unicode decoding
#     # 문자열(Unicode)로 디코딩을 해야만 문자열 관련 함수 사용가능
#     readed = readed.decode()
#
#     print('Readed Unicode String:', readed)
#
#     response = readed
#
#     ser.writePortUnicode(response)
#     print('Response:', response)



while True:
    # 'COM2'로부터 라인단위로 읽어서 그 데이터를 다시 쓰기
    # exit 입력시 종료
    while True:
        # Enter키가 입력될때까지의 데이터를 읽기
        readed = ser.readuntilExitCode(RETURN_CODE)
        print('#' * 100)

        # 읽어온 데이터 출력
        print('Readed byte string:', readed)

        # byte array -> Unicode decoding
        # 문자열(Unicode)로 디코딩을 해야만 문자열 관련 함수 사용가능
        readed = readed.decode()

        print('Readed Unicode String:', readed)

        # 프로그램 종료조건 : EXIT
        if readed == 'exit':
            print('Done')
            break

        response = readed + '\r\n'
        ser.writePortUnicode(response)
        print('Response:', response)