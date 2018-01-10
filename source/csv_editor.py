import csv

readCSV = csv.reader(open('Wood_data.csv', 'rt'), delimiter=",")
with open('data.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    out = readCSV
    for row in out:
        if row[3] != "DensityMin":
            row[3] = str((float(row[3]) + float(row[4])) / 2)
            if row[6] != "":
                row[6] = str((float(row[6]) + float(row[7])) / 2)
        writer.writerow(row)
