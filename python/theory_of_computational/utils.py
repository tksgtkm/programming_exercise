import sys

def readFile(fileName):
    fileContents = ''
    with open(fileName) as inputFile:
        fileContents = inputFile.read()
    return fileContents

rf = readFile

VERBOSE_TESTS = True

def tprint(*args, **kwargs):
    if VERBOSE_TESTS:
        print(*args, **kwargs)
        sys.stdout.flush()