# opens videos.csv and deletes the first 3 rows(except the first row which are labels) and saves the file on the original file. keeps the first label row

import csv

def del_rows(file_name):
    with open(file_name, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        rows = list(csv_reader)
        del rows[1:4]
    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)

del_rows('videos.csv')