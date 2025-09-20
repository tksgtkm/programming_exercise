import utils
from utils import readFile
from yesOnStringApprox import yesOnStringApprox

def notYesOnSelfApprox(progString):
    val = yesOnStringApprox(progString)
    if (val == 'yes'):
        return 'no'
    elif (val == 'no'):
        return 'yes'
    else:
        return 'unknown'

def testnotYesOnSelfApprox():
    testvals = [
        ('containsGAGA.py', 'no'),
        ('longerThan1K.py', 'yes'),
        ('yes.py', 'no'),
    ]
    for (filename, solution) in testvals:
        val = notYesOnSelfApprox(readFile(filename))
        utils.tprint(filename + ":", val)
        assert val == solution

print(testnotYesOnSelfApprox())