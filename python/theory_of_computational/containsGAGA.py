from utils import tprint
from utils import readFile

def containsGAGA(inString):
    if 'GAGA' in inString:
        return 'yes'
    else:
        return 'no'

def testContainsGAGA():
    testVals = [
        ('GAGA', 'yes'),
        ('CCCGAGA', 'yes'),
        ('AGAGAGAAGAAGAGAAA', 'yes'),
        ('GAGACCCCC', 'yes'),
        ('', 'no'),
        ('CCCCCCCCGAGTTTT', 'no'),
    ]
    for (inString, solution) in testVals:
        val = containsGAGA(inString)
        tprint(inString, ':', val)
        assert val == solution

# testContainsGAGA()

longstring = readFile('data/geneticString.txt')
print('long string result: ', containsGAGA(longstring))