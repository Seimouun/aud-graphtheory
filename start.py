import datetime

import cv2
import array as arr
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

image = cv2.imread("chart.png") 
image_height = image.shape[0]
image_width = image.shape[1]
money_steps = [100000, 1000000, 10000000]

pixel_money = []

pixel_since_last_line = 0
line_count = 0
money_per_line = []

line_start = 95
line_end = 647

for y in range(line_start, line_end):
    pixel_height = line_end + line_start - 1 - y;
    if image[pixel_height, 114][2] < 254:
        print(pixel_since_last_line)
        for count in range(0, pixel_since_last_line + 1):
            last_moneten = 0
            if y - line_start > 0:
                print(str(len(pixel_money)) + ", " + str(y));
                last_moneten = pixel_money[y - line_start -1]
            pixel_money.append(last_moneten + money_steps[int(line_count / 10)] / pixel_since_last_line);
        line_count+=1;
        pixel_since_last_line = 0

    image[pixel_height, 114] = [0,0,255]
    pixel_since_last_line+=1;

def get_cash_mula_for_pixel_height(hight_key):
    return pixel_money[hight_key]

print("mula fo 76: " + str(get_cash_mula_for_pixel_height(76)))


def getPixelDate(x):
    img = cv2.imread("chart.png")

    x, y = 57, 577
    found = True
    B, G, R = 255, 255, 255

    arrayXs = arr.array("i", [0])
    arrayDatesNPixel = []
    startDate = dt(2018, 2, 1)


    _finalYPoint = 576

    while found:
        if x >= 1206:
            break
        b, g, r = (img[y][x])
        print(f"{x},{y}")
        if [b, g, r] != [B, G, R]:
            arrayXs.append(x)
            startDate += relativedelta(months=1)
            arrayDatesNPixel.append([x, startDate])
        x = x + 1

    for i in range(0, len(arrayDatesNPixel) - 1):
        date_1 = arrayDatesNPixel[i][1]
        delta = date_1 - startDate
        for i2 in range(0, delta.days):
            arrayDatesNPixel[i][i2] = date_1
            date_1 = date_1 + datetime.timedelta(days=1)

    print(arrayDatesNPixel)
    print(arrayXs)

    return arrayDatesNPixel
