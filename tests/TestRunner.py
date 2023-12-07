from os import walk
import sys
from src.YeetscriptRunner import runner

TestsFolder = walk('./tests')

test_files = []

for folder in TestsFolder:
    for file in folder[2]:
        if file[-2:] == '.z':
            test_files.append(file)

for file in test_files:
    print('\n\n-------------------------')
    print(file)
    try:
        runner('./tests/' + file)
    except:
        type, value, traceback = sys.exc_info()
        print(type, value)
        print("ERROR THROWN")
