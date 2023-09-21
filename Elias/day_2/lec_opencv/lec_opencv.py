import cv2
from icecream import ic
from datetime import datetime

class WebCam:
    def __init__(self, portNum=None):
        self.port_num = portNum

    ###############################################################
    # Set port number
    ###############################################################
    def set_port(self, portNum):
        self.port_num = portNum

    ###############################################################
    # Get Webcam list
    ###############################################################
    def get_valid_camera_list(self, max_port_num=3):
        camera_port_list = []

        for index in range(max_port_num):
            cap = cv2.VideoCapture(index)
            ret, frame = cap.read()

            if ret is True and frame is not None:
                camera_port_list.append(index)
            else:
                break

            cap.release()

        return camera_port_list

    ###############################################################
    # Capture Webcam Image
    ###############################################################
    def capture_image(self, file_name, width=1280, heigh=720):
        # 웹캠 객체생성
        cap = cv2.VideoCapture(self.port_num, cv2.CAP_DSHOW)

        # 웹캠 옵션설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, heigh)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

        # 카메라 이미지 캡쳐
        _, frame = cap.read()

        # 캡쳐된 이미지를 파일로 저장
        ret = cv2.imwrite(file_name, frame)

        # 핸들 릴리즈
        cap.release()

        return ret, file_name

    ###############################################################
    # Capture Video Stream Until 'q' quit
    ###############################################################
    def capture_video(self, width=1280, height=720, isMono=False, flip=None):
        # 웹캠 객체생성
        cap = cv2.VideoCapture(self.port_num, cv2.CAP_DSHOW)

        # 웹캠 옵션설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

        while True:
            ret, frame = cap.read()

            if ret is False:
                break

            if isMono is True:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            if flip is not None:
                # flip: 0 -> bottom to top, flip: 1 -> left to right
                frame = cv2.flip(frame, flip)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) == ord('q'):  # 1 ---> 1/1000 sec
                break

        cap.release()
        cv2.destroyWindow('frame')

    ###############################################################
    # Record Video Stream with AVI Codec
    ###############################################################
    def record_video(self, video_file_name, width=1280, height=720, flip=None, fps=24):
        # 웹캠 객체생성
        cap = cv2.VideoCapture(self.port_num, cv2.CAP_DSHOW)

        # 웹캠 옵션설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

        # fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')

        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        out = cv2.VideoWriter(video_file_name + '.avi', fourcc, fps, frame_size)

        while cap.isOpened():
            ret, frame = cap.read()

            if ret is True:
                if flip is not None:
                    frame = cv2.flip(frame, flip)

                # 동영상파일에 이미지를 저장
                out.write(frame)

                # 현재화면 출력
                cv2.imshow('frame', frame)

                if cv2.waitKey(int(1000/fps)) == ord('q'):
                    break

            else:
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    ###############################################################
    # Play Video File
    ###############################################################
    def play_video(self, file_name):
        cap = cv2.VideoCapture(file_name)
        fps = cap.get(cv2.CAP_PROP_FPS)
        ic(fps)

        while cap.isOpened():
            ret, frame = cap.read()

            if ret is True:
                cv2.imshow('frame', frame)

                if cv2.waitKey(int(1000/fps)) == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = WebCam()

    port_list = cam.get_valid_camera_list()
    ic(port_list)

    # 웹캠이 하나라도 있으면
    if len(port_list) > 0:
        # 첫번째 웹캠을 선택
        portNum = port_list[0]
        cam.set_port(portNum)
        ic(portNum)

        ###############################################################################################
        # Capture Image(Snapshot)
        ###############################################################################################
        file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '.png' # 2023_08_25_09_38_10.png
        ic(cam.capture_image(file_name, 1920, 1080))

        ##############################################################################################
        # Capture Video Stream
        ##############################################################################################
        cam.capture_video()
        cam.capture_video(isMono=True)
        cam.capture_video(flip=0)
        cam.capture_video(flip=1)
        cam.capture_video(isMono=True, flip=0)

        ###############################################################################################
        # Record Video Stream
        ###############################################################################################
        file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        cam.record_video(file_name)

        ###############################################################################################
        # Play Video File
        ###############################################################################################
        cam.play_video('2023_08_25_10_19_29.avi')



