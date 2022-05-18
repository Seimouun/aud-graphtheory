import datetime
from glob import glob
import math
import csv
from re import I
from xmlrpc.client import DateTime

import cv2
import os
import array as arr
from datetime import datetime as dt
from cv2 import log
from dateutil.relativedelta import relativedelta

csv_name = "data_chart5.csv"

if (os.path.exists(csv_name)):
    os.remove(csv_name)

image = cv2.imread("chart-default.png")
image_height = image.shape[0]
image_width = image.shape[1]

graph_start_x_left = -1
graph_start_y_bottom = -1
graph_height = -1
graph_width = -1

arrayDatesNPixel_res = []
pixel_money = []

def start_program_with_chart(chart_path, chart_name):
    print(chart_name)
    global csv_name
    global image
    global image_height
    global image_width
    global arrayDatesNPixel_res
    global pixel_money
    global graph_start_x_left
    global graph_start_y_bottom
    global graph_height
    global graph_width

    csv_name = chart_name.replace(".png",".csv")

    if (os.path.exists(csv_name)):
        os.remove(csv_name)
    
    image = cv2.imread(chart_path + "/" + chart_name)
    image_height = image.shape[0]
    image_width = image.shape[1]

    graph_start_x_left = -1
    graph_start_y_bottom = -1
    graph_height = -1
    graph_width = -1

    arrayDatesNPixel_res = []
    pixel_money = []

    iterate_pixel_money()
    get_pixel_date_new()

    print("264:" + str(get_cash_mula_for_pixel_height(264)) + "$")

    print("starting with " + chart_path + "/" + chart_name)
    find_blue_pixels()
    print("finished")




def is_line(pixel_color):
    return pixel_color < 254


def is_graph_line_horizontal(x, y):
    for yDown in range(0, 40):
        if (y + yDown < image_height and image[y + yDown, x][2] < 210):
            continue;
        else:
            return False
    return True


def is_graph_line_vertical(y, x):
    for xRight in range(0, 40):
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
                image[y, x] = [255,0,0]
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
                    return first_value, first_value_height, zeros_diff / pixel_count
                pixel_count = 0
        pixel_count += 1

def gen_pixel_height_new(start, end):
    print("moiga")
    first_value = -1
    first_value_height = -1

    pixel_count = 0

    pos_x = graph_start_x_left - 1

    print(end - start)
    for y in range(0, end - start):
        print("ayo")
        height = end - y
        # find line
        print(image[height, pos_x][2])
        if (is_line(image[height, pos_x][2])):
            print("found line")
            zeros_count = get_zeros(pos_x, height)
            # check if line has number & first_value not set yet
            if (zeros_count > 0 and first_value < 0):
                print("firtval: ", first_value)
                first_value = zeros_count
                first_value_height = height
                # if first line already there get second one and do the math thingy
            elif (first_value > 0):
                val_diff = math.log10(math.pow(10,first_value) * 2) - first_value
                print("valdiff:", val_diff)
                return first_value, first_value_height, val_diff / pixel_count
        
        if(first_value > 0):
            pixel_count += 1

def iterate_pixel_money():
    set_graph_dimensions()

    print(graph_start_y_bottom)
    print(graph_height)

    # start_value, start_height, pixel_height = gen_pixel_height_new(graph_start_y_bottom - graph_height, graph_start_y_bottom)

    gen_pixel_height_new(graph_start_y_bottom - graph_height, graph_start_y_bottom)

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





def get_pixel_date_new():
    image[graph_start_y_bottom + 1, graph_start_x_left + graph_width] = [192, 192, 192]
    found = True
    start = graph_start_x_left
    end = graph_start_x_left + graph_width
    start_date = dt(2017, 12, 1)
    while (found):
        found = False
        end_date = start_date + relativedelta(months=3)
        days_delta = (end_date-start_date).days
        pix_to_line = 0
        
        if(start < end - 1):
            for x in range(start, end):
                if(pix_to_line > 0 and is_line(image[graph_start_y_bottom + 1, x][2]) or x == end - 1):
                    found = True
                    start += pix_to_line
                    break
                else:
                    pix_to_line += 1
        
        if(found):
            for i in range(start - pix_to_line, start):
                pix_value = pix_to_line/days_delta
                start_date += relativedelta(days=pix_value)
                arrayDatesNPixel_res.append([int(i), start_date])



            



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
    counter = arrayXs[1]

    counterX = arrayXs[1]
    for i in range(1, len(arrayDeltaDays) - 1):
        delta = arrayDeltaDays[i]
        xCord = arrayXs[i + 1]
        newX = counterX
        counterX = xCord - counterX
        (dummy, date_1) = arrayDatesNPixel[i]
        for i2 in range(0, abs(delta.days)):
            perDay = (counterX / abs(delta.days))
            newX = newX + perDay
            #date_1 += relativedelta(days=1)
            #arrayDatesNPixel_res.insert(counter, [int(newX), date_1])
            #counter += 1
            date_1 += relativedelta(days=1)
            arrayDatesNPixel_res.insert(counter, [int(newX), date_1])
            #if(counter < 500):
            #print(counter)
            counter += 1
        #print(xCord)
        counterX = xCord





# Just Call if getpixeldate was already called
def getDateForPixel(input: float) -> datetime:
    for i in range(0, len(arrayDatesNPixel_res)):
        (cord, datum) = arrayDatesNPixel_res[i]
        if input == cord:
            return datum







##Julian Thanner

def toCsv(num1, num2):
    data = [num1, num2]

    with open(csv_name, 'a', encoding='UTF8', newline="") as f:
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

    prev_pixel_time = None
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
                #print("prev ",prev_pixel_time)
                if (pixel_date is None):
                    print("!!!   missing date (ignoring): x-" + str(x))
                else:
                    if(prev_pixel_time is not None and prev_pixel_time.date() == pixel_date.date()):
                        #print("prevPix: ",prev_pixel_time)
                        pixel_date += relativedelta(minutes=prev_x_same_amount)
                        prev_x_same_amount += 1
                    else:
                        prev_x_same_amount = 1
                    
                    toCsv(pixel_date.strftime("%d.%m.%Y, %H:%M"), get_cash_mula_for_pixel_height(y_end - y))
                    prev_pixel_time = pixel_date

                # color the used pixels of a data-point white since they've already been handled
                image_for_blues[y][x] = [255, 255, 255]
                image_for_blues[y - 1][x + 1] = [255, 255, 255]
                image_for_blues[y][x + 1] = [255, 255, 255]
                image_for_blues[y + 1][x + 1] = [255, 255, 255]
                image_for_blues[y][x + 2] = [255, 255, 255]


# Test Methoden-Aufruf
def generate_from_directory(images_dir):
    for (dirpath, dirnames, filenames) in os.walk(images_dir):
        for f in filenames:
            if(".png" in f):
                start_program_with_chart(images_dir, f)
        break

start_program_with_chart("images", "00.0-11.0-27.0-86.0-19.0-41.0-00.0-17.0-21.0-10000.0-11.0-NONE.png")