import datetime
import math
import csv
from xmlrpc.client import DateTime

import cv2
import os
import array as arr
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

if (os.path.exists("data.csv")):
    os.remove("data.csv")

image = cv2.imread("images/chart1.png")
print(image)
image_height = image.shape[0]
image_width = image.shape[1]

graph_start_x_left = -1
graph_start_y_bottom = -1
graph_height = -1
graph_width = -1

arrayDatesNPixel_res = []
pixel_money = []


def is_line(pixel_color):
    return pixel_color < 254


def is_graph_line_horizontal(x, y):
    for yDown in range(0, 30):
        # print(x)
        if (y + yDown < image_height and image[y + yDown, x][2] < 210):
            continue;
        else:
            return False
    return True


def is_graph_line_vertical(y, x):
    for xRight in range(0, 30):
        if (x + xRight < image_width and image[y, x + xRight][2] < 210):
            continue;
        else:
            return False
    return True









#Julian Thanner

def set_graph_dimensions():
    global graph_height
    global graph_width
    global graph_start_x_left
    global graph_start_y_bottom

    for x in range(0, image_width):
        for y in range(0, image_height):
            if (is_line(image[y, x][2]) and is_graph_line_horizontal(y, x)):
                graph_start_x_left = x
                break
        else:
            continue
        break
    for y in range(0, image_height):
        if (is_line(image[y, graph_start_x_left][2]) and is_graph_line_vertical(y, graph_start_x_left)):
            graph_start_y_bottom = y
            break
    size_x_temp = -1
    for x in range(graph_start_x_left, image_width):
        if image[graph_start_y_bottom, x][2] < 210:
            size_x_temp += 1
        else:
            break

    graph_width = size_x_temp
    size_y_temp = -1
    for y in range(0, graph_start_y_bottom):
        actual_y = graph_start_y_bottom - y
        if image[actual_y, graph_start_x_left][2] < 210:
            size_y_temp += 1
        else:
            break

    graph_height = size_y_temp








#Simon Reitmann

# checks if a line has a number and how much 0's the given number has
def get_zeros(width, height):
    count = 0
    x = width
    zeros = 0
    while count < 13:
        if (image[height, x][2] < 250 and image[height, x - 4][2] < 250):
            image[height, x] = [0, 0, 255]
            zeros += 1
            x -= 4
            count = 5
        x -= 1
        count += 1

    return zeros


# checks between 2 endlines what each pixel is "worth"
#   returns: height of the first endline,
#            how many 0's the first line has,
#            the "worth" of each pixel between those lines
def gen_pixel_height(start, end):
    first_value = -1
    first_value_height = -1

    pixel_count = 0

    pos_x = graph_start_x_left - 1

    for y in range(0, end - start):
        height = end - y
        # find line
        if (is_line(image[height, pos_x][2])):
            zeros_count = get_zeros(pos_x, height)
            image[height, pos_x] = [255, 0, 0]
            # check if line has number & first_value not set yet
            if (zeros_count > 0):
                # find first line
                if (first_value < 0):
                    first_value = zeros_count
                    first_value_height = height
                # if first line already there get second one and do the math thingy
                elif (first_value > 0):
                    zeros_diff = zeros_count - first_value
                    print(first_value)
                    return first_value, first_value_height, zeros_diff / pixel_count
                pixel_count = 0
        pixel_count += 1


def iterate_pixel_money():
    set_graph_dimensions()
    print('gr_width: ' + str(graph_width))
    print('gr_height: ' + str(graph_height))
    print('gr_start_x: ' + str(graph_start_x_left))
    print('gr_start_y: ' + str(graph_start_y_bottom))


    start_value, start_height, pixel_height = gen_pixel_height(graph_start_y_bottom - graph_height, graph_start_y_bottom)


    # print(pixel_height)

    # cv2.imshow('ImageWindow', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    for y in range(0, graph_height):
        height = graph_start_y_bottom - y
        relative_to_start = start_height - height
        # 10^5 = 100 000
        # 10^6 = 1 000 000
        # iterate between 5 and 6 with pixel_height
        # relative_to_start respects that start_height isn't always the first pixel on the graphs y axis
        money_to_append = math.pow(10, start_value + pixel_height * relative_to_start)
        pixel_money.append(money_to_append)


def get_cash_mula_for_pixel_height(hight_key):
    return round(pixel_money[hight_key], 2)









##Lucas Kronlachner

def getpixeldate():
    x, y = (graph_start_x_left + 1), (graph_start_y_bottom + 1)
    found = True
    B, G, R = 255, 255, 255

    arrayXs = arr.array("i", [0])
    arrayDatesNPixel = []
    arrayDeltaDays = []
    startDate = dt(2017, 12, 1)
    finalDate = dt(2018, 3, 1)

    arrayDatesNPixel.append([x, startDate])
    arrayXs.append(x)

    while found:
        if x > graph_width + graph_start_x_left:
            arrayXs.append(graph_start_x_left + graph_width)
            startDate += relativedelta(months=3)
            arrayDatesNPixel.append([x, startDate])
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

    counterX = 0
    newX = 0
    perDay = 0
    counter = 0

    print(arrayDeltaDays)
    print(arrayXs)
    print(arrayDatesNPixel)

    for i in range(0, len(arrayDeltaDays) - 1):
        delta = arrayDeltaDays[i]
        xCord = arrayXs[i + 1]
        counterX = xCord - counterX
        newX = xCord
        (dummy, date_1) = arrayDatesNPixel[i]
        for i2 in range(0, abs(delta.days)):
            perDay = (counterX / abs(delta.days))
            newX = newX + perDay
            #date_1 += relativedelta(days=1)
            #arrayDatesNPixel_res.insert(counter, [int(newX), date_1])
            #counter += 1
            date_1 += relativedelta(days=1)
            arrayDatesNPixel_res.insert(counter, [round(newX), date_1])
            counter += 1
        counterX = xCord


iterate_pixel_money()
getpixeldate()
print(arrayDatesNPixel_res)

print("264:" + str(get_cash_mula_for_pixel_height(264)) + "$")


# Just Call if getpixeldate was already called
def getDateForPixel(input: float) -> datetime:
    for i in range(0, len(arrayDatesNPixel_res)):
        (cord, datum) = arrayDatesNPixel_res[i]
        if input == cord:
            return datum







##Julian Thanner

def toCsv(num1, num2):
    data = [num1, num2]

    with open('data.csv', 'a', encoding='UTF8', newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(data)
        f.close()









##Elias Ruttinger & Rafael Peterstorfer

def find_blue_pixels():
    x_start, x_end = graph_start_x_left, graph_width + graph_start_x_left
    y_start, y_end = graph_start_y_bottom - graph_height, graph_start_y_bottom
    B_Min, G_Min, R_Min = 200, 100, 50
    B_Max, G_Max, R_Max = 210, 110, 60
    image_for_blues = image.copy()

    prev_x = -1
    prev_x_same_amount = 1

    for x in range(x_start, x_end):
        for y_temp in range(y_start, y_end):
            y = y_end - y_temp
            # declare pixels of potential data-point
            b, g, r = image_for_blues[y][x]
            b1, g1, r1 = image_for_blues[y - 1][x + 1]
            b2, g2, r2 = image_for_blues[y][x + 1]
            b3, g3, r3 = image_for_blues[y + 1][x + 1]
            b4, g4, r4 = image_for_blues[y][x + 2]

            # check if bgr-value of pixels is in-between color-range
            if ([B_Min, G_Min, R_Min] <= [b, g, r] <= [B_Max, G_Max, R_Max] and
                    [B_Min, G_Min, R_Min] <= [b1, g1, r1] <= [B_Max, G_Max, R_Max] and
                    [B_Min, G_Min, R_Min] <= [b2, g2, r2] <= [B_Max, G_Max, R_Max] and
                    [B_Min, G_Min, R_Min] <= [b3, g3, r3] <= [B_Max, G_Max, R_Max] and
                    [B_Min, G_Min, R_Min] <= [b4, g4, r4] <= [B_Max, G_Max, R_Max]):

                # get_cash_mula_for_pixel_height() goes from bottom up with the lowest value being at index 0
                # find_blue_pixels() starts from the top, so subtract y
                pixel_date = getDateForPixel(x + 1)
                prev_pixel_time = getDateForPixel(prev_x)
                if (pixel_date is None):
                    print("!!!   missing date (ignoring): x-" + str(x))
                else:
                    if(prev_x == x):
                        prev_pixel_time += relativedelta(hours=prev_x_same_amount)
                        prev_x_same_amount += 1
                    else:
                        prev_x_same_amount = 1
                    #if(prev_pixel_time is None):
                        #prev_pixel_time = dt.now()
                    toCsv(pixel_date.strftime("%d.%m.%Y") + ", " + (prev_pixel_time.strftime("%H:%M") if prev_pixel_time is not None else "00:00"), get_cash_mula_for_pixel_height(y_end - y))
                    prev_x = x

                # color the used pixels of a data-point white since they've already been handled
                image_for_blues[y][x] = [255, 255, 255]
                image_for_blues[y - 1][x + 1] = [255, 255, 255]
                image_for_blues[y][x + 1] = [255, 255, 255]
                image_for_blues[y + 1][x + 1] = [255, 255, 255]
                image_for_blues[y][x + 2] = [255, 255, 255]


# Test Methoden-Aufruf
print("starting")
find_blue_pixels()
print("finished")