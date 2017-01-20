#!/usr/bin/env python3

import argparse

class Record:
    tiers = []
    emptyLines = {}

    def __init__(self, t = []):
        self.tiers = t
        self.emptyLines = {}

    def getTier(self, name):
        for v in self.tiers:
            if v[0] == name:
                return v
        return None

    def setTier(self, name, value):
        assert value[0] == name
        for idx, v in enumerate(self.tiers):
            if v[0] == name:
                self.tiers[idx] = value
                return
        if len(self.tiers) in self.emptyLines:
            self.emptyLines[len(self.tiers)+1] = self.emptyLines.pop(len(self.tiers))
        self.addTier(value)

    def addTier(self, tier):
        self.tiers.append(tier)

    def doPrint(self):
        i = 0
        for tier in self.tiers:
            blanklines = self.emptyLines.get(i, 0)
            for j in range(0, blanklines):
                print()
            i += 1
            print(" ".join(tier))

        blanklines = self.emptyLines.get(i, 0)
        for j in range(0, blanklines):
            print()

    def __repr__(self):
        return "Record(%s tiers)" % len(self.tiers)

class FileInstance:
    records = []

    def addRecord(self, record):
        self.records.append(record)

    def doPrint(self):
        first = True
        for record in self.records:
            record.doPrint()
            first = False

def parse(f):
    currentRecord = Record()
    ret = FileInstance()

    i = 0
    for line in f:
        line = line.rstrip()
        #print("line", line, not line, i, currentRecord.emptyLines)
        if not line:
            if not i in currentRecord.emptyLines:
                currentRecord.emptyLines[i] = 1
            else:
                currentRecord.emptyLines[i] += 1
            continue
        elif line.startswith("\\ref") and currentRecord.tiers:
            ret.addRecord(currentRecord)
            #print("xxx", currentRecord.emptyLines)
            currentRecord = Record([])
            i = 0

        i += 1
        currentRecord.addTier(line.split())

    if currentRecord.tiers:
        ret.addRecord(currentRecord)
    return ret

def specialReplace(word, a, b):
    if "question" in word:
        return word
    else:
        return word.replace(a, b)

def createMa(record, function = None):
    mtTier = record.getTier("\\mt")
    if not mtTier:
        return record
    maTier = ["\\ma"] + [word for word in mtTier[1:] if word != '/']
    if function:
        maTier = function(maTier)
    record.setTier("\\ma", list(maTier))
    return record

recordOperations = {
    "QToApostrophe": lambda record: Record([ [specialReplace(word, "q", "'") for word in tier ] for tier in record.tiers]),
    "ApostropheToQ": lambda record: createMa(record, lambda tier: (word.replace("'", "q") for word in tier)),
    "IvenaToIvaEna": lambda record: createMa(record, lambda tier: ("iva ena" if word=="ivena" else word for word in tier)),
    "createMa": createMa
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input text file")
    parser.add_argument('rules', metavar='rule', type=str, nargs='*', help='one of these: ' +", ".join(recordOperations.keys()))
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        instance = parse(f)
        for rule in args.rules:
            cosa = [recordOperations[rule](record) for record in instance.records]
            instance.records = cosa
        instance.doPrint()
