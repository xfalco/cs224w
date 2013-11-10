import csv
import re

INPUT_FILE="network_python2.csv"
OUTPUT_FILE="network_python2.graph"

outputFile = open(OUTPUT_FILE, 'wb')
inputFile = open(INPUT_FILE, 'rU')
# read first line to ignore headers
reader = csv.reader(inputFile)
next(reader, None)
for list in reader :
  list[3] = "\"" + list[3] + "\""    # Q_CreationDate
  list[13] = "\"" + list[13] + "\""  # A_CreationDate
  pass
  # Q_Tags
  tags = list[18]  
  tagString = ','.join(re.findall(r"[\w']+", tags))
  tagString = "\"" + tagString + "\""
  list[18] = tagString
  pass
  outputFile.write((','.join(list))+'\n')

inputFile.close()
outputFile.close()
