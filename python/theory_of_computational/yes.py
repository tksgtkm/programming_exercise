import utils
from utils import readFile

def yes(inString):
    return 'yes'

def testYes():
    testVals = [
        ('', 'yes'),
        ('x', 'yes'),
        ('asdf', 'yes'),
        ('GAGAGAGAGAGA', 'yes')
    ]
    for (inString, solution) in testVals:
        val = yes(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

# print(testYes())