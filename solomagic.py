#!/usr/bin/env python3

import argparse

class Record:
    def __init__(self, t = []):
        self.tiers = t
        self.emptyLines = []

    def getTier(self, name):
        for v in self.tiers:
            if v[0] == name:
                return v
        raise Exception("GetScheisse")

    def setTier(self, name, value):
        assert value[0] == name
        for idx, v in enumerate(self.tiers):
            if v[0] == name:
                self.tiers[idx] = value
                return
        raise Exception("SetScheisse")

    def doPrint(self):
        i = 0
        for tier in self.tiers:
            if i in self.emptyLines:
                print()
            i += 1
            print(" ".join(tier))

    def __repr__(self):
        return "Record(%s tiers)" % len(self.tiers)

class FileInstance:
    records = []

    def addRecord(self, record):
        self.records.append(record)

    def doPrint(self):
        first = True
        for record in self.records:
            if not first:
                print()
            record.doPrint()
            first = False

def parse(f):
    currentRecord = Record()
    ret = FileInstance()

    i = 0
    for line in f:
        line = line.rstrip()
        if not line:
            currentRecord.emptyLines.append(i)
            continue
        elif line.startswith("\\ref") and currentRecord.tiers:
            if currentRecord.emptyLines and currentRecord.emptyLines[-1] == i:
                currentRecord.emptyLines.pop()
            ret.addRecord(currentRecord)
            currentRecord = Record([])
            i = 0

        i += 1
        currentRecord.tiers.append(line.split())

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
    maTier = ["\\ma"] + [word for word in mtTier[1:] if word != '/']
    if function:
        maTier = function(maTier)
    record.tiers.append(maTier)
    return record

recordOperations = {
    "QToApostrophe": lambda record: Record([ [specialReplace(word, "q", "'") for word in tier ] for tier in record.tiers]),
    "ApostropheToQ": lambda record: Record([ [word.replace("'", "q") for word in tier ] for tier in record.tiers]),
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
