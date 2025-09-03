from utils import rf, tprint
from multiplyAll import multiplyAll

def testmultiplyAll():
    testVals = [
        ('', '1'),
        ('1', '1'),
        ('2', '2'),
        ('1 5', '5'),
        ('2 5', '10'),
        ('10 20 30', '6000'),
        ('10 10 10 10 10 10 10 10 10 10', '10000000000')
    ]
    for (inString, solution) in testVals:
        val = multiplyAll(inString)
        tprint(inString, ':', val)
        assert val == solution

testmultiplyAll()