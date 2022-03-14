import datetime
import csv

import cv2
import array as arr
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

image = cv2.imread("images/chart1.png")
image_height = image.shape[0]
image_width = image.shape[1]
money_steps = [100000, 1000000, 10000000]

pixel_money = []


def is_line(pixel_color):
    return pixel_color < 254


def iterate_pixel_money():
    pixel_count = 0
    section = 0
    sub_section = 8
    section_amount = [100000, 100000, 1000000, 10000000]

    line_start = 95
    line_end = 647
    for y in range(0, line_end - line_start):
        height = line_end - y
        if (is_line(image[height, 114][2])):
            for ___i in range(0, pixel_count):
                prev_index_money = 0
                try:
                    prev_index_money = pixel_money[pixel_money.__len__() - 1]
                except:
                    pass
                pixel_money.append(prev_index_money + section_amount[section] / pixel_count)

            pixel_count = 0
            sub_section += 1
            if (sub_section % 9 == 0):
                sub_section = 0
                section += 1
        else:
            pixel_count += 1


def get_cash_mula_for_pixel_height(hight_key):
    return round(pixel_money[hight_key], 2)


iterate_pixel_money()

# example:
# use get_cash_mula_for_pixel_height(74) returns 100000.0 rounded to 2 decimals
# money indexes go from 0 to 551
# height of the pixel relative to the baseline of the graph is the respected money for that pixel
print("75:" + str(get_cash_mula_for_pixel_height(74)) + "$")


def getpixeldate(input: float) -> datetime:
    x, y = 102, 649
    found = True
    B, G, R = 255, 255, 255

    arrayXs = arr.array("i", [0])
    arrayDatesNPixel = []
    startDate = dt(2017, 12, 31)
    finalDate = dt(2017, 12, 31)

    while found:
        if x >= 1252:
            break
        b, g, r = (image[y][x])
        print(f"{x},{y}")
        if [b, g, r] != [B, G, R]:
            arrayXs.append(x)
            startDate += relativedelta(months=3)
            arrayDatesNPixel.append([x, startDate])
        x = x + 1
    newX = 0
    counter = 1
    for i in range(0, len(arrayDatesNPixel)):
        (xCord, date_1) = arrayDatesNPixel[i]
        delta = date_1 - finalDate
        finalDate = date_1
        print(delta)
        for i2 in range(0, delta.days):
            newX = newX + (xCord / delta.days)
            date_1 += relativedelta(days=1)
            arrayDatesNPixel.insert(counter, [newX, date_1])
            counter += 1
    print(arrayXs)
    print(arrayDatesNPixel)


    for i in range(0, len(arrayDatesNPixel) - 1):
        (cord, datum) = arrayDatesNPixel[i]
        if input is cord:
            return datum

def toCsv(num1, num2):      
    data = [num1, num2]

    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(data)
        f.close()

#Test 1 Methoden-Aufruf