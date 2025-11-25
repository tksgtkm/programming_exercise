import utils
from utils import readFile
import re

class Transition:

    def __init__(self, sourceState, destState, label, writeSymbol, direction):
        self.sourceState = sourceState
        self.destState = destState
        self.label = label
        self.writeSymbol = writeSymbol
        self.direction = direction

    def __str__(self):
        return 'sourceState: %s destState: %s label: %s writeSymbol: %s direction: %s' % \
            (self.sourceState, self.destState, self.label, self.writeSymbol, self.direction)
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def unify(tList):
        assert len(tList) > 0
        first = tList[0]
        unifiedTrans = Transition(first.sourceState, first.destState, None, first.writeSymbol, first.direction)
        for t in tList:
            assert unifiedTrans.isCompartible(t)
        labels = [t.label for t in tList]
        unifiedTrans.label = ''.join(labels)
        return unifiedTrans

    def isCompartible(self, other):
        return self.sourceState == other.sourceState \
            and self.destState == other.destState \
            and self.writeSymbol == other.writeSymbol \
            and self.direction == other.direction
    
    def __eq__(self, other):
        if self is other:
            return True
        if other == None:
            return False
        if not isinstance(other, Transition):
            return False
        return self.sourceState == other.sourceState \
            and self.destState == other.destState \
            and self.label == other.label \
            and self.writeSymbol == other.writeSymbol \
            and self.direction == other.direction
    
    def __ne__(self, other):
        return self == other
    
    def __lt__ (self, other):
        return (self.sourceState, self.destState, self.label, \
                self.writeSymbol, self.direction) \
            < \
            (other.sourceState, other.destState, other.label, \
             other.writeSymbol, other.direction)
    
    def __gt__(self, other):
        return other.__lt__(self)
    
    def getKeyForUnify(self):
        return (self.sourceState, self.destState, self.writeSymbol, self.direction)
    
    @staticmethod
    def reassembleFromUnifyKey(key, label):
        return Transition(key[0], key[1], label, key[2], key[3])
    
class TuringMachine:

    verbose = False
    blockMarker = 'block:'
    maxSteps = 100000
    maxDepth = 1000
    exceedeMaxStepsMsg = 'exceeded maxSteps'
    rightDir = 'R'
    leftDir = 'L'
    stayDir = 'S'
    noStr = 'no'
    yesStr = 'yes'
    blank = '_'
    anySym = '~'
    notSym = '!'
    commentStart = '#'
    actionSeparator = '='
    blockSeparator = '='
    stateSeparator = '->'
    labelSeparator = ':'
    writeSymSeparator = ';'

    validSymbols = {c for c in
        r"""$'"%&()*+-./0123456789<>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}"""
    }
    
    acceptState = 'qA'
    rejectState = 'qR'
    haltState = 'qH'
    startState = 'q0'
    
    def __init__(self, description=None, tapeStr='', depth=0, name=None, allowImplicitReject=True, allowLeftFromCell0=True, keepHistory=False):
        self.transitions = None
        self.depth = depth
        self.name = name
        self.allowImplicitReject = allowImplicitReject
        self.allowLeftFromCell0 = allowLeftFromCell0
        self.blocks = dict()
        self.keepHistory = keepHistory
        self.history = None
        
    def splitTransition(self, line):
        splitRegex = '[' + \
            TuringMachine.labelSeparator + \
            TuringMachine.writeSymSeparator + \
            ']'
        (states, label, actions) = [x.strip() for x in re.split(splitRegex, line)]
        (sourceState, destState) = [x.strip() for x in states.split(TuringMachine.stateSeparator)]
        return (label, actions, sourceState, destState)
    
    def extractTransition(self, line):
        (label, actions, sourceState, destState) = self.splitTransition(line)
        if TuringMachine.actionSeparator in actions:
            (writeSymbol, direction) = [x.strip() for x in actions.split(TuringMachine.actionSeparator)]
        else:
            (writeSymbol, direction) = (None, actions)
        return Transition(sourceState, destState, label, writeSymbol, direction)
    
    @staticmethod
    def stripComments(lines):
        return [x.split(TuringMachine.commentStart)[0] for x in lines]
    
    def read(self, tmString):
        self.transitions = dict()
        tmLines = tmString.split('\n')
        tmLines = TuringMachine.stripComments(tmLines)
        tmLines = [x.strip() for x in tmLines]
        for line in tmLines:
            if len(line) > 0:
                if line.startswith(TuringMachine.blockMarker):
                    self.addBlock(line)
                else:
                    t = self.extractTransition(line)
                    self.addTransition(t)
                    

    def addBlock(self, line):
        if self.depth == TuringMachine.maxDepth:
            message = 'Exceeded max depth when adding block in line "%s"' % line
            raise utils.WcbcException(message)
        line = line[len(TuringMachine.blockMarker):]
        (state, separator, filename) = [x.strip() for x in line.partition(TuringMachine.blockSeparator)]
        if separator != TuringMachine.blockSeparator:
            message = 'Unexpected separator in block description '
            raise utils.WcbcException(message)
        newBlock = TuringMachine(readFile(filename), '', self.depth + 1)
        self.blocks[state] = newBlock

    def addTransition(self, t):
        if self.transitions == None:
            self.transitions = dict()
        transitionList = self.transitions.setdefault(t.sourceState, [])
        transitionList.append(t)