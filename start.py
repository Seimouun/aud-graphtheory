import datetime
import csv

import cv2
import os
import array as arr
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

os.remove("data.csv")
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
    arrayDatesNPixel_res = []
    arrayDeltaDays = []
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


    print(arrayDatesNPixel)
    for i in range(0, len(arrayDatesNPixel)):
        (dummy, date_1) = arrayDatesNPixel[i]
        delta = date_1 - finalDate
        print(f"i: {i}  Date 1: {date_1}  Final_Date: {finalDate}")
        finalDate = date_1
        arrayDeltaDays.insert(i, delta)
    print(arrayXs)

    counterX = 102
    newX = 0
    perDay = 0
    counter = 0
    for i in range(0, len(arrayDeltaDays)):
        delta = arrayDeltaDays[i]
        xCord = arrayXs[i + 1]
        counterX = xCord - counterX
        newX = xCord
        (dummy, date_1) = arrayDatesNPixel[i]
        for i2 in range(0, delta.days):
            print(counterX)
            perDay = (counterX / delta.days)
            newX = newX + perDay
            print(newX)
            date_1 += relativedelta(days=1)
            arrayDatesNPixel_res.insert(counter, [int(newX), date_1])
            counter += 1
            date_1 += relativedelta(days=1)
            arrayDatesNPixel_res.insert(counter, [round(newX), date_1])
            counter += 1
        counterX = xCord


    for i in range(0, len(arrayDatesNPixel_res)):
        (cord, datum) = arrayDatesNPixel_res[i]
        if input == cord:
            return datum

print(getpixeldate(226.0))

def toCsv(num1, num2):
    data = [num1, num2]
    

    with open('data.csv', 'a', encoding='UTF8', newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(data)
        f.close()
        
def find_blue_pixels():
    x_start, x_end = 103, 1252
    y_start, y_end = 95, 646
    B_Min, G_Min, R_Min = 200, 100, 50
    B_Max, G_Max, R_Max = 210, 110, 60
    image_for_blues = image.copy()
    
    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            #declare pixels of potential data-point
            b, g, r = image_for_blues[y][x]
            b1, g1, r1 = image_for_blues[y - 1][x + 1]
            b2, g2, r2 = image_for_blues[y][x + 1]
            b3, g3, r3 = image_for_blues[y + 1][x + 1]
            b4, g4, r4 = image_for_blues[y][x + 2]

            #check if bgr-value of pixels is in-between color-range
            if ([B_Min, G_Min, R_Min] <= [b, g, r] <=  [B_Max, G_Max, R_Max] and
                [B_Min, G_Min, R_Min] <= [b1, g1, r1] <=  [B_Max, G_Max, R_Max] and
                [B_Min, G_Min, R_Min] <= [b2, g2, r2] <=  [B_Max, G_Max, R_Max] and
                [B_Min, G_Min, R_Min] <= [b3, g3, r3] <=  [B_Max, G_Max, R_Max] and
                [B_Min, G_Min, R_Min] <= [b4, g4, r4] <=  [B_Max, G_Max, R_Max]):

                #get_cash_mula_for_pixel_height() goes from bottom up with the lowest value being at index 0
                #find_blue_pixels() starts from the top with the startpoint being 95, so subtract y
                toCsv(getpixeldate(x + 1), get_cash_mula_for_pixel_height(y_end - y))
                
                #color the used pixels of a data-point white since they've already been handled
                image_for_blues[y][x] = [255, 255, 255]
                image_for_blues[y - 1][x + 1] = [255, 255, 255]
                image_for_blues[y][x + 1] = [255, 255, 255]
                image_for_blues[y + 1][x + 1] = [255, 255, 255]
                image_for_blues[y][x + 2] = [255, 255, 255]

#Test Methoden-Aufruf
toCsv(datetime.datetime(2020, 5, 17).strftime('%d.%m.%Y %H:%M'), 2345.408)
find_blue_pixels()


