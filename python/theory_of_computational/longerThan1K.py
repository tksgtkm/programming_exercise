import utils
from utils import readFile

def longerThan1K(inString):
    if len(inString) > 1000:
        return 'yes'
    else:
        return 'no'

def testlongerThan1K():
    testVals = [
        (1001*'x', 'yes'),
        (400*'xyz', 'yes'),
        ('', 'no'),
        (1000*'x', 'no'),
    ]
    for (inString, solution) in testVals:
        val = longerThan1K(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

# print(testlongerThan1K())