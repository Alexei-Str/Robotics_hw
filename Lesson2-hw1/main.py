import cv2
import numpy as np


# Делим изображение на части в 300x300 пикселей
def task1():
    img = cv2.imread("Resources/sci-fi-art1.jpg")
    image_copy = img.copy()
    imgheight = img.shape[0]
    imgwidth = img.shape[1]

    M = 300
    N = 300
    x1 = 0
    y1 = 0
    count = 1

    for y in range(0, imgheight, M):
        for x in range(0, imgwidth, N):
            y1 = y + M
            x1 = x + N
            if y1 >= imgheight:
                y1 = imgheight - 1
            if x1 >= imgwidth:
                x1 = imgwidth - 1
            tiles = image_copy[y:y + M, x:x + N]
            cv2.imwrite('saved_patches/' + str(count) + 'tile' + str(x) + '_' + str(y) + '.jpg', tiles)
            count += 1
            cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)


# Поворачиваем\ искажаем выделенный фрагмент изображения (двойной клик лкм -> прожатие s, так 4 точки по часовой;
# y - сохранить фрагмент; n - сбросить точки, для выбора новых)

def task2():
    img_warp = cv2.imread("Resources/task2_img.jpg")

    def draw_circle(event, x, y, flags, param):
        global mouseX, mouseY
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(img_warp, (x, y), 3, (25, 255, 0), -1)
            mouseX, mouseY = x, y

    cv2.imshow("task2", img_warp)
    cv2.setMouseCallback('task2', draw_circle)
    x = []
    i = 0

    while (True):
        cv2.imshow('task2', img_warp)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        if k == ord('s'):
            x.append((mouseX, mouseY))
            print(x[i])
            i = i + 1

        if k == ord('y'):
            if len(x) == 4:
                break
        if k == ord('n'):
            print("clear")
            x = []
            i = 0

    width, height = 250, 350
    pts1 = np.float32([[x[0]], [x[1]], [x[2]], [x[3]]])
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img_warp, matrix, (width, height))

    cv2.imshow("Output", imgOutput)
    cv2.waitKey(0)


# Сохраняем видео-фрагмет с камеры на компьютер (прожатием q)
def task3():
    # заменив путь на 0 можно перейти на работу с камерой
    vid_cap = cv2.VideoCapture("Resources/TestVid.mp4")

    w = int(vid_cap.get(3))
    h = int(vid_cap.get(4))
    frame_size = (w, h)
    fps = 24
    # При работе с роликом я выставил "*'mp4v'", для работы с камерой нужно заменить на "*'XVID'"
    output = cv2.VideoWriter('saved_video/vid.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)

    while (vid_cap.isOpened()):
        res, frame = vid_cap.read()
        if res == True:
            output.write(frame)
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(50)
            if key == ord('q'):
                break
        else:
            break
    vid_cap.release()
    output.release()
    cv2.destroyAllWindows()

# проверенные методы я закомментировал, с нужного снять коммент
# task1()
# task2()
task3()
