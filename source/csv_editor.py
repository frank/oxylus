import csv

readCSV = csv.reader(open('Wood_data_not_normalized.csv', 'rt'), delimiter=",")
with open('Wood_data.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    out = readCSV
    # Values for the normalization
    maxima = []
    maxima.extend([1040.0, 21.6, 5.0, 3.0, 3.0, 3.0, 2.0, 3.0])
    minima = []
    minima.extend([0, 0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0])
    for i, row in enumerate(out):
        if(i == 0):
            row[4] = "Low wood movement (Nerviosidad)"
        for j, column in enumerate([3, 5, 7, 8, 10, 11, 12, len(row)-2]):
            if i is not 0 and row[column] is not "":
                row[column] = '%.4f' % ((float(row[column]) - minima[j]) / (maxima[j] - minima[j]))
        if i is not 0:
            if(row[len(row)-1] != "FALSE" and row[len(row)-1] != "TRUE"):
                if(int(row[len(row)-1]) == 1):
                    row[len(row)-1] = "FALSE"
                elif(int(row[len(row)-1]) == 2):
                    row[len(row)-1] = "TRUE"
            if(float(row[4])>2):
                row[4] = "FALSE"
            else:
                row[4] = "TRUE"
            if(float(row[6])>3):
                row[6] = "TRUE"
            else:
                row[6] = "FALSE"
        writer.writerow(row)

