import utils
from utils import readFile

def maybeLoop(inString):
    if not 'secret sauce' in inString:
        i = 0
        while i >= 0:
            i = i + 1
    else:
        if len(inString) % 2 == 0:
            return 'yes'
        else:
            return 'no'

def testmaybeLoop():
    testVals = [
        ('', None),
        ('sdfjkhask', None),
        ('secret sauce', 'yes'),
        ('xsecret sauce', 'no'),
        ('xsecret saucex', 'yes'),
    ]
    for (inString, solution) in testVals:
        val = utils.runWithTimeout(None, maybeLoop, inString)
        utils.tprint(inString, ':', val)
        assert val == solution

# print(testmaybeLoop())