import csv
import re

INPUT_FILE="network_python.csv"
OUTPUT_FILE="network_python.graph"

outputFile = open(OUTPUT_FILE, 'wb')
inputFile = open(INPUT_FILE, 'rU')
# read first line to ignore headers
reader = csv.reader(inputFile)
next(reader, None)
for list in reader :
  tags = list[7]
  tagString = ','.join(re.findall(r"[\w']+", tags))
  list[7] = tagString
  list.append('\n')
  outputFile.write(' '.join(list))


inputFile.close()
outputFile.close()
