import cv2

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