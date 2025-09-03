from utils import tprint
from utils import readFile

def countLines(inString):
    # 改行文字で分割する
    lines = inString.split('\n')
    # 行数を文字列で返す
    return str(len(lines))

def testCountLines():
    testVals = [
        ('', '1'),
        ('abc', '1'),
        ('abc\n', '2'),
        ('\n', '2'),
        ('abc\ndef', '2'),
        ('abc\ndef\nghi', '3'),
        ('abc\ndef\nghi\n', '4'),
    ]
    for (inString, solution) in testVals:
        val = countLines(inString)
        tprint(inString, ':', val)
        assert val == solution

# testCountLines()
longstring = readFile('data/wasteland.txt')
print(countLines(longstring))