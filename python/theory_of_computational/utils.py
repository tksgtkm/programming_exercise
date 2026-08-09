import sys

def readFile(fileName):
    fileContents = ''
    with open(fileName) as inputFile:
        fileContents = inputFile.read()
    return fileContents

rf = readFile

class WcbcException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

VERBOSE_TESTS = True

def tprint(*args, **kwargs):
    if VERBOSE_TESTS:
        print(*args, **kwargs)
        sys.stdout.flush()

