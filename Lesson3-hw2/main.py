import copy

import cv2
import numpy as np


# Построение маршрута по щелчку мыши, расчёт длины пути в метрах
class Task1():

    def __init__(self):
        self.first_point = True
        self.hasALine = False
        self.img = cv2.imread("Resources/Map1.png")
        self.last_point = 0
        self.thePathIsLaid = False
        self.pixelsToMeters = 0.675
        self.pathLength = 0

    def task1(self):
        def draw_path(event, x, y, flags, param):

            if event == cv2.EVENT_LBUTTONDBLCLK and not self.thePathIsLaid:
                self.img = self.noInfImg
                self.prev_point = self.last_point
                self.last_point = [x, y]
                self.cache_img = copy.deepcopy(self.img)

                if self.first_point:
                    cv2.circle(self.img, (x, y), 10, (255, 0, 0), 8)
                    self.first_point = False

                else:
                    cv2.line(self.img, self.prev_point, (x, y), (0, 0, 0), 3)
                    cv2.circle(self.img, (x, y), 4, (0, 180, 255), 4)
                    self.hasALine = True
                    self.pathLength = self.pathLength + round(((((self.last_point[1] - self.prev_point[1]) ** 2 +
                                                                 (self.last_point[0] - self.prev_point[
                                                                     0]) ** 2) ** 0.5) * self.pixelsToMeters), 2)
                self.noInfImg = copy.deepcopy(self.img)
                draw_info()

        def draw_info():
            font = cv2.FONT_HERSHEY_COMPLEX
            if self.pathLength != 0:
                local_path_l = round(((((self.last_point[1] - self.prev_point[1]) ** 2 +
                                        (self.last_point[0] - self.prev_point[0]) ** 2) ** 0.5) * self.pixelsToMeters),
                                     2)
            else:
                local_path_l = 0.0

            text = 'Управление: \nдвойной щелчок л.к.м.- создать точку' \
                   '\nbackspace- удалить последний отрезок' \
                   '\nпробел- закончить построение пути' \
                   '\nd- начать построение пути с начала' \
                   '\nesc- выйти из программы' \
                   '\n\nИнформация:' \
                   '\nдлина всего пути: %f м.' \
                   '\nдлина последнего отрезка: %f м.' % (self.pathLength, local_path_l)
            y0, dy = 35, 18
            for i, line in enumerate(text.split('\n')):
                y = y0 + i * dy
                cv2.putText(self.img, line, (10, y), font, 0.6, (200, 0, 0), 1, cv2.LINE_AA)

            cv2.imshow("task1", self.img)

        self.noInfImg = copy.deepcopy(self.img)
        draw_info()
        cv2.setMouseCallback('task1', draw_path)

        while True:
            cv2.imshow('task1', self.img)
            k = cv2.waitKey(1) & 0xFF

            if k == 27:
                break

            if k == ord('d'):
                self.img = cv2.imread("Resources/Map1.png")
                self.first_point = True
                self.hasALine = False
                self.thePathIsLaid = False
                self.pathLength = 0
                cv2.imshow('task1', self.img)
                self.noInfImg = copy.deepcopy(self.img)
                draw_info()

            if not self.thePathIsLaid:

                if k == 8 and self.hasALine and self.first_point is False:
                    self.pathLength = self.pathLength - ((((self.last_point[1] - self.prev_point[1]) ** 2 +
                                                           (self.last_point[0] - self.prev_point[
                                                               0]) ** 2) ** 0.5) * self.pixelsToMeters)
                    self.img = copy.deepcopy(self.cache_img)
                    self.last_point = self.prev_point
                    cv2.imshow('task1', self.img)
                    self.hasALine = False
                    self.noInfImg = copy.deepcopy(self.img)
                    draw_info()

                if k == 32 and self.hasALine and self.first_point is False:
                    cv2.imshow('task1', self.img)
                    cv2.line(self.img, self.prev_point, self.last_point, (0, 0, 0), 3)
                    cv2.circle(self.img, self.last_point, 5, (0, 180, 255), 10)
                    cv2.line(self.img, (self.last_point[0] - 10, self.last_point[1] - 10),
                             (self.last_point[0] + 10, self.last_point[1] + 10), (255, 255, 255), 5)
                    cv2.line(self.img, (self.last_point[0] - 10, self.last_point[1] + 10),
                             (self.last_point[0] + 10, self.last_point[1] - 10), (0, 0, 0), 5)
                    self.thePathIsLaid = True


# Добавление аннотации на видеоряд, сохранение изменённого ролика
class Task2():

    def __init__(self):
        self.video = cv2.VideoCapture('Resources/Car_drive_time_lapse.mp4')

    def writeAnnotation(self):
        line = "Car driving in Scotland"
        output = cv2.VideoWriter('saved_video/vid.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
                                 self.video.get(cv2.CAP_PROP_FPS), (int(self.video.get(3)), int(self.video.get(4))))
        while self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                cv2.line(frame, (15, int(self.video.get(4)) - 53), (305, int(self.video.get(4)) - 53), (200, 0, 0), 1)
                cv2.putText(frame, line, (20, int(self.video.get(4)) - 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (200, 0, 0),
                            1, cv2.LINE_4)
                cv2.imshow('Frame', frame)
                output.write(frame)
                if cv2.waitKey(25) & 0xFF == 27:
                    break
            else:
                break
        else:
            print("Video playback error")


# Изменение угла обзора в видео
class Task3():
    def __init__(self):
        self.video = cv2.VideoCapture('Resources/Night_city_traffic_timelapse.mp4')
        self.angleSet = False
        self.matrix = None

    def writeAnnotation(self):
        output = cv2.VideoWriter('saved_video/vid(task3).mp4', cv2.VideoWriter_fourcc(*'mp4v'),
                                 self.video.get(cv2.CAP_PROP_FPS), (int(self.video.get(3)), int(self.video.get(4))))
        while self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                if not self.angleSet:
                    cv2.imshow('Frame', frame)
                    img_warp = frame
                    pointArr = []

                    text = '2*  / \  3*' \
                           '\n   / ! \ ' \
                           '\n1*/  !  \ 4*' \
                           '\n\ny - save \nn - reset \nesc -close'
                    y0, dy = 35, 18
                    for i, line in enumerate(text.split('\n')):
                        y = y0 + i * dy
                        cv2.putText(img_warp, line, (10, y), cv2.FONT_HERSHEY_COMPLEX, 0.6, (200, 0, 0), 1, cv2.LINE_AA)

                    def draw_circle(event, x, y, flags, param):
                        if event == cv2.EVENT_LBUTTONDBLCLK:
                            cv2.circle(img_warp, (x, y), 3, (25, 255, 0), -1)
                            cv2.line(img_warp, (0, y), (int(self.video.get(3)), y), (25, 255, 0), 1)
                            pointArr.append(list((x, y)))

                    cv2.setMouseCallback('Frame', draw_circle)

                    while True:
                        cv2.imshow('Frame', img_warp)
                        k = cv2.waitKey(20) & 0xFF
                        if k == 27:
                            break
                        if k == ord('y'):
                            if len(pointArr) >= 4:
                                break
                        if k == ord('n'):
                            print("clear")
                            pointArr = []
                            cv2.imshow('Frame', frame)

                    width, height = int(self.video.get(3)), int(self.video.get(4))

                    indent = (width - (pointArr[2][0] - pointArr[1][0]))/2
                    if indent > width/4:
                        pointArr[2][0] = width - width/4
                        pointArr[1][0] = width - pointArr[2][0]
                        indent = width/4
                    else:
                        pointArr[2][0] = width
                        pointArr[1][0] = 0

                    indentR = width - indent

                    pts1 = np.float32([[pointArr[1]], [pointArr[0]], [pointArr[3]], [pointArr[2]]])
                    pts2 = np.float32([[0, 0], [indent, height], [indentR, height], [width, 0]])

                    self.matrix = cv2.getPerspectiveTransform(pts1, pts2)
                    self.angleSet = True

                warpOutput = cv2.warpPerspective(frame, self.matrix, (int(self.video.get(3)), int(self.video.get(4))))
                cv2.imshow('Frame2', warpOutput)
                output.write(warpOutput)

                if cv2.waitKey(25) & 0xFF == 27:
                    break
            else:
                break
        else:
            print("Video playback error")


# Task1().task1()
# Task2().writeAnnotation()
Task3().writeAnnotation()
