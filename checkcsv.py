from datetime import datetime as dt
import os
import csv

dates = []
prev_date_time = None
index = 0

valid = True

if (os.path.exists("data.csv")):
    with open('data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            curr_date_time = dt.strptime(row[0], '%d.%m.%Y, %H:%M')
            if(curr_date_time is not None and prev_date_time is not None and curr_date_time < prev_date_time):
                print(str(index) + ' not valid! (' + str(curr_date_time) + " isn't past " + str(prev_date_time) + ")")
                valid = False
            if(row[0] in dates):
                print(str(index) + ' not valid! (' + row[0] + " exists multiple times)")
                valid = False
            else:
                dates.append(row[0])
            prev_date_time = curr_date_time
            index+=1

print("is valid: " + str(valid))