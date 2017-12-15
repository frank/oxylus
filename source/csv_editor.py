# import csv
# readCSV = csv.reader(open('Wood_data.csv', 'rb'), delimiter=",")
# out = csv.writer(open('data.csv', 'rb'), delimiter=",")
# out = readCSV
# for row in out:
# 	out.writerow(row)
# for row in out:
# 	if row[8] == 'E':
# 		row[8] = 1
# 	if row[8] == 'M':
# 		row[8] = 1
# 	if row[8] == 'D':
# 		row[8] = 1
# 	for x in range(9):
# 		if row[9+x] == None:
# 			row[9+x] = False
# 		if row[9+x] == 'X':
# 			row[9+x] = True
import csv

with open('Wood_data.csv', 'rb') as readFile, open('data.csv', 'rb') as writeFile:
	for row in readFile:
		if row[8] == 'E':
			row[8] = 1
		if row[8] == 'M':
			row[8] = 2
		if row[8] == 'D':
			row[8] = 3
		for x in range(9):
			if row[9+x] == None:
				row[9+x] = False
			if row[9+x] == 'X':
				row[9+x] = True
		writeFile.write(row)
