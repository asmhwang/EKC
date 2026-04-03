import csv

with open('water_potability.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data_list = list(csv_reader)
    print([row[2] for row in data_list])
    print([row[5] for row in data_list])
    