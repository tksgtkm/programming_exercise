from utils import readFile
from utils import tprint

def longestWord(inString):
    words = inString.split()
    longest = ''
    lengthOfLongest = 0
    for word in words:
        if len(word) > lengthOfLongest:
            longest = word
            lengthOfLongest = len(word)
    return longest

def testLongestWord():
    testVals = [
        ('', ''),
        ('a', 'a'),
        ('abc', 'abc'),
        ('a bc', 'bc'),
        ('bc a', 'bc'),
        ('x xx xxx xxxx xxxxx xxxx xxx xx x', 'xxxlxx'),
        ('x xx xxx xxxx\nxxxxx xxxx\nxxx xx xxxxxxxx', 'xxxxxxxx'),
    ]
    for (inString, solution) in testVals:
        val = longestWord(inString)
        tprint(inString, ':', val)
        assert val == solution

testLongestWord()