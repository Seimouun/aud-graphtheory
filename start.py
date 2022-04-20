import datetime
import math
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

pixel_money = []

graph_start_x_left = 101
graph_start_y_bottom = 94
graph_height = 554
graph_width = 1149

def is_line(pixel_color):
    return pixel_color < 254
#checks if a line has a number and how much 0's the given number has
def get_zeros(width, height):
    count = 0
    x = width
    zeros = 0
    while count < 10:
        if(image[height, x][2] < 250 & image[height, x - 4][2] < 250):
            zeros += 1
            x -= 4
            count = 5
        x-=1
        count+=1

    return zeros
#checks between 2 endlines what each pixel is "worth"
#   returns: height of the first endline,
#            how many 0's the first line has,
#            the "worth" of each pixel between those lines
def gen_pixel_height(start, end):
    first_value = -1
    first_value_height = -1

    pixel_count = 0

    line_start = start
    line_end = end

    for y in range(0, line_end - line_start):
        height = line_end - y
        # find line
        if(is_line(image[height, graph_start_x_left][2])):
            zeros_count = get_zeros(graph_start_x_left, height)
            # check if line has number & first_value not set yet
            if(zeros_count > 0):
                # find first line
                if(first_value < 0):
                    first_value = zeros_count
                    first_value_height = height
                # if first line already there get second one and do the math thingy
                elif(first_value > 0):
                    zeros_diff = zeros_count - first_value
                    return first_value, first_value_height, zeros_diff / pixel_count
                pixel_count = 0
        pixel_count += 1

def iterate_pixel_money():
    line_start = graph_start_y_bottom
    line_end = graph_start_y_bottom + graph_height

    start_value, start_height, pixel_height = gen_pixel_height(line_start, line_end)

    for y in range(0, line_end - line_start):
        height = line_end - y
        relative_to_start = start_height - height
        # 10^5 = 100 000
        # 10^6 = 1 000 000
        # iterate between 5 and 6 with pixel_height
        # relative_to_start respects that start_height isn't always the first pixel on the graphs y axis
        money_to_append = math.pow(10, start_value + pixel_height*relative_to_start)
        pixel_money.append(money_to_append)


def get_cash_mula_for_pixel_height(hight_key):
    return round(pixel_money[hight_key], 2)


iterate_pixel_money()

# example:
# use get_cash_mula_for_pixel_height(74) returns 100000.0 rounded to 2 decimals
# money indexes go from 0 to 551
# height of the pixel relative to the baseline of the graph is the respected money for that pixel
print("74:" + str(get_cash_mula_for_pixel_height(74)) + "$")


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
        if [b, g, r] != [B, G, R]:
            arrayXs.append(x)
            startDate += relativedelta(months=3)
            arrayDatesNPixel.append([x, startDate])
        x = x + 1


    for i in range(0, len(arrayDatesNPixel)):
        (dummy, date_1) = arrayDatesNPixel[i]
        delta = date_1 - finalDate
        finalDate = date_1
        arrayDeltaDays.insert(i, delta)

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
            perDay = (counterX / delta.days)
            newX = newX + perDay
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


def toCsv(num1, num2):
    data = [num1, num2]
    

    with open('data.csv', 'a', encoding='UTF8', newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(data)
        f.close()
        
def find_blue_pixels():
    x_start, x_end = graph_start_x_left, graph_width + graph_start_x_left
    y_start, y_end = graph_start_y_bottom, graph_height + graph_start_y_bottom
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
                #find_blue_pixels() starts from the top, so subtract y
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


