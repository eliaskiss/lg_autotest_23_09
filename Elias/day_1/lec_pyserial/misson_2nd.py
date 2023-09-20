# 01. 전원 (Command: k a)
# ▶ 세트의 전원 켜짐/ 꺼짐을 제어합니다.

# Transmission(명령값)
# [k][a][ ][Set ID][ ][Data][Cr]
# Data	00: 꺼짐
#       01: 켜짐
#       ff(FF): 상태값
# ex) ka 01 01, ka 01 00, ka 01 ff

# Acknowledgement(응답값)
# [a][ ][Set ID][ ][OK/NG][Data][x]
# ex) a 01 OK01x, a 01 OK00x, a 01 NG11x
#     a 01 OK01x (켜져있는경우)
#     a 01 OK00x (꺼져있는경우)
# NG인 경우는: 명령어가 잘못된경우, 값이 잘못된경우.
# 처음 시작상태는 poweroff인 상태로 시작
# * 디스플레이의 전원이 완전히 켜진 이후에 정상적인 Acknowledgement 신호가 돌아옵니다.
#
# Extra Mission
# ** Transmission/ Acknowledgement 신호 사이에는 일정시간 지연이 발생할 수 있습니다.
# 'exit'가 입력되면 종료
# 수신된 데이터를 json 포맷으로 저장

# ka 01 00 --> Power Off
# ka 01 01 --> Power On
# ka 01 ff --> Return power status
#
# In terminal
# ka 01 01 --> response a 01 OK01x
# ka 01 00 --> response a 01 OK00x
# ka 01 ff --> response a 01 OK01x or a 01 OK00x

from lec_pyserial_class import MySerial
import json
from datetime import datetime, timedelta

RETURN_CODE = b'\x0d'

ser = MySerial()
is_power_on = False
ser.openSerial('COM2')

print('Program is running...')

while True:
    # Enter키가 입력될때까지의 데이터를 읽기
    readed = ser.readuntilExitCode(RETURN_CODE)
    print('#' * 100)

    # 읽어온 데이터 출력
    print('Readed byte string:', readed)

    # byte array -> Unicode decoding
    # 문자열(Unicode)로 디코딩을 해야만 문자열 관련 함수 사용가능
    readed = readed.decode()
    # ka 01 00 KA 01 00 Ka 01 00 --> 소문자로 변환
    readed = readed.lower()
    print('Readed Unicode String:', readed)

    # 프로그램 종료조건 : EXIT
    if readed == 'exit':
        print('Done')
        break

    # ka 01 01
    # ka : Command
    # 01 : SetID
    # 01 : Value
    datalist = readed.split(' ') # 'ka 01 01' --> ['ka', '01', '01']

    # 커맨드 포맷 점검
    if not(len(readed) == 8 and len(datalist) == 3):
        msg = 'Wrong command format!!!\r\n'
        print(msg)
        ser.writePortUnicode(msg)
        continue

    command = datalist[0]
    setId = datalist[1]
    value = datalist[2]
    print(f'Command: {command}, SetID: {setId}, Value: {value}')

    response = ''

    # 명령어 확인
    if command == 'ka':
        # Power Off
        if value == '00':
            is_power_on = False
            response = f'OK{value}x'  # a 01 OK01x
            print('Changed power status:', is_power_on)
        # Power On
        elif value == '01':
            is_power_on = True
            response = f'OK{value}x'
            print('Changed power status:', is_power_on)
        # Check Power Status
        elif value == 'ff':
            response = 'OK01x' if is_power_on is True else 'OK00x'
            print('Current power status:', is_power_on)
        # Not supported value
        else:
            response = f'NG{value}x'
            print('Wrong Value!!!')

        # a 01 OK01x
        response = f'{command[1]} {setId} {response}\r\n'
    elif command == 'kb':
        # TODO: kb 커맨드 처리필요
        pass
    else:
        print('Not supported command!!!')
        response = 'Not Supported command!!!\r\n'

    # 로그파일 저장
    jsonData = {'command': command, 'setId':setId, 'value':value, 'response':response}
    jsonString = json.dumps(jsonData) # Dictionary Object --> string ('{"commnad":ka, ....
    # jsonData = json.loads(jsonString) # String --> Dictionary Object
    print('JsonString:', jsonString)

    # 현재시간
    now = datetime.now()
    print('Now:', now)

    # https://www.geeksforgeeks.org/python-datetime-strptime-function/
    # datetime object --> string
    now = now.strftime('[%Y-%m-%d %H:%M:%S]') # [2023-08-23 08:30:11]
    # now = datetime.strptime("2023:09:20", "%Y:%m:%d")
    # tomorrow = now + timedelta(days=1)
    # yesterday = now - timedelta(days=1)
    # yesterday = now + timedelta(days=-1)

    # f = open(...)
    # f.write(...)
    # f.close()
    with open('command.log', 'a', encoding='utf8') as f:
        f.write(f'{now} {jsonString}\n')

    ser.writePortUnicode(response)


ser.closeSerial()

