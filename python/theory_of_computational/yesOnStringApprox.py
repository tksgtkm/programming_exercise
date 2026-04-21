import utils
from utils import readFile
from containsGAGA import containsGAGA
from longerThan1K import longerThan1K
from maybeLoop import maybeLoop
from yes import yes

def yesOnStringApprox(progString, inString):
    if progString == readFile('containsGAGA.py'):
        return containsGAGA(inString)
    elif progString == readFile('longerThan1K.py'):
        return longerThan1K(inString)
    elif progString == readFile('yes.py'):
        return yes(inString)
    elif progString == readFile('maybeLoop.py'):
        if not 'secret sauce' in inString: 
            return 'no'
        else:
            return maybeLoop(inString)
    else:
        return 'unknown'

def testyesOnStringApprox():
    testvals = [
        ('containsGAGA.py', 'TTTTGAGATT', 'yes'),
        ('containsGAGA.py', 'TTTTGAGTT', 'no'),
        ('longerThan1K.py', 1500*'x', 'yes'),
        ('longerThan1K.py', 'xyz', 'no'),
        ('yes.py', 'xyz', 'yes'),
        ('maybeLoop.py', '', 'no'),
        ('maybeLoop.py', 'asdfhjksd', 'no'),
        ('maybeLoop.py', 'secret sauce', 'yes'),
        ('maybeLoop.py', 'xsecret sauce', 'no'),
        ('maybeLoop.py', 'xsecret saucex', 'yes'),
    ]
    for (filename, inString, solution) in testvals:
        val = yesOnStringApprox(readFile(filename), inString)
        utils.tprint(filename + ":", val)
        assert val == solution

# print(yesOnStringApprox(readFile('longerThan1K.py'), readFile('longerThan1K.py')))
# print(yesOnStringApprox(readFile('maybeLoop.py'), readFile('maybeLoop.py')))
print(yesOnStringApprox(readFile('longerThan1K.py')))