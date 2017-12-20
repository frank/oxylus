import csv

readCSV = csv.reader(open('Wood_data.csv', 'rt'), delimiter=",")
with open('data.csv', 'w') as writeFile:
	writer = csv.writer(writeFile)
	out = readCSV
	for row in out:
		if row[8] == 'E':
			row[8] = 1
		if row[8] == 'M':
			row[8] = 2
		if row[8] == 'D':
			row[8] = 3
		for x in range(9):
			if row[9+x] == '':
				row[9+x] = False
			if row[9+x] == 'X':
				row[9+x] = True
		writer.writerow(row)
