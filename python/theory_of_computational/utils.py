import sys
import re
import threading
import os
import queue
import random

haltComputation = threading.Event()

aRandom = random.Random()

inf = float('inf')

def readFile(fileName):
    fileContents = ''
    with open(fileName) as inputFile:
        fileContents = inputFile.read()
    return fileContents

rf = readFile

def invokeAndStoreResult(fn, q, done, *inString):
    """
    関数を呼び出し、戻り値を与えられたqueueに格納する
    """
    ret = fn(*inString)
    q.put(ret)
    done.set()

def runWithTimeout(timeout, fn, *inString):
    if timeout == None:
        timeout = TEST_TIMEOUT
    
    q = queue.Queue()
    done = threading.Event()

    t = threading.Thread(target=invokeAndStoreResult, args=(fn, q, done) + inString)
    t.start()

    done.wait(timeout)

    haltComputation.set()

    haltComputation.clear()

    if q.empty():
        retVal = None
    else:
        retVal = q.get()
    
    return retVal

VERBOSE_TESTS = True
BRIEF_TESTS = True
NUMBRIEF_TESTS = 1
TEST_TIMEOUT = 10.0

def tprint(*args, **kwargs):
    if VERBOSE_TESTS:
        print(*args, **kwargs)
        sys.stdout.flush()