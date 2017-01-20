#!/usr/bin/env python3

import argparse
import re

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

    def clean(self):
        self.tiers = map(lambda tier: filter(lambda word: word, tier), self.tiers)
        return self

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
    maTier = record.getTier("\\ma")
    if not maTier or len(maTier)<=1:
        mtTier = record.getTier("\\mt")
        if not mtTier:
            return record
        maTier = ["\\ma"] + [word for word in mtTier[1:] if word != '/']

    if function:
        maTier = function(maTier)
    record.setTier("\\ma", list(maTier))
    return record

recordOperations = {
    #"QToApostrophe": lambda record: Record([ [specialReplace(word, "q", "'") for word in tier ] for tier in record.tiers], record.emptyLines),
    "ApostropheToQ": lambda record: createMa(record, lambda tier: (word.replace("'", "q") for word in tier)),
    "IvenaToIvaEna": lambda record: createMa(record, lambda tier: ("iva ena" if word=="ivena" else word for word in tier)),
    "IvonaToIvaOna": lambda record: createMa(record, lambda tier: ("iva ona" if word=="ivona" else word for word in tier)),
    "IvamangToIvaAmang": lambda record: createMa(record, lambda tier: ("iva amang" if word=="ivamang" else word for word in tier)),
    "IvamaToIvaAmang": lambda record: createMa(record, lambda tier: ("iva amang" if word=="ivama" else word for word in tier)),
    "IvemiaToIvaEmia": lambda record: createMa(record, lambda tier: ("iva emia" if word=="ivemia" else word for word in tier)),
    "IveriaToIvaEria": lambda record: createMa(record, lambda tier: ("iva eria" if word=="iveria" else word for word in tier)),
    "IvavonaToIvaAbuOna": lambda record: createMa(record, lambda tier: ("iva abu ona" if word=="ivavona" else word for word in tier)),
    "IvavenaToIvaAbuEna": lambda record: createMa(record, lambda tier: ("iva abu ena" if word=="ivavena" else word for word in tier)),
    "IvavamangToIvaAbuAmang": lambda record: createMa(record, lambda tier: ("iva abu amang" if word=="ivavamang" else word for word in tier)),
    "IvavamaToIvaAbuAmang": lambda record: createMa(record, lambda tier: ("iva abu amang" if word=="ivavama" else word for word in tier)),
    "IvavemiaToIvaAbuEmia": lambda record: createMa(record, lambda tier: ("iva abu emia" if word=="ivavemia" else word for word in tier)),
    "IvaveriaToIvaAbuEria": lambda record: createMa(record, lambda tier: ("iva abu eria" if word=="ivaveria" else word for word in tier)),

    "AvonaToAbuOna": lambda record: createMa(record, lambda tier: ("abu ona" if word=="avona" else word for word in tier)),
    "AvenaToAbuEna": lambda record: createMa(record, lambda tier: ("abu ena" if word=="avena" else word for word in tier)),
    "AvamaToAbuAmang": lambda record: createMa(record, lambda tier: ("abu amang" if word=="avama" else word for word in tier)),
    "AvamangToAbuAmang": lambda record: createMa(record, lambda tier: ("abu amang" if word=="avamang" else word for word in tier)),
    "AvemiaToAbuEmia": lambda record: createMa(record, lambda tier: ("abu emia" if word=="avemia" else word for word in tier)),
    "AveriaToAbuEria": lambda record: createMa(record, lambda tier: ("abu eria" if word=="averia" else word for word in tier)),

    "XtoAsterisk": lambda record: createMa(record, lambda tier: ("*" if word=="XXX" else word for word in tier)),

    "Veampeu": lambda record: createMa(record, lambda tier: ("veangpeu" if word=="veampeu" else word for word in tier)),
    "VaToIva": lambda record: createMa(record, lambda tier: ("iva" if word=="va" else word for word in tier)),
    "SenaToSoEna": lambda record: createMa(record, lambda tier: ("so ena" if word=="sena" else word for word in tier)),
    "SonaToSoOna": lambda record: createMa(record, lambda tier: ("so ona" if word=="sona" else word for word in tier)),

    "qataToXta": lambda record: createMa(record, lambda tier: ("xta" if re.fullmatch(r"[q'][aeiou]ta", word) else word for word in tier)),
    "NgtaToXta": lambda record: createMa(record, lambda tier: ("xta" if word=="ngta" else word for word in tier)),

    # Getting rid of single question marks surrounded by parentheses
    "DeleteQM": lambda record: createMa(record, lambda tier: (word.replace(r"(?)", "") for word in tier)),

    # Getting rid of all colons
    "DeleteColon": lambda record: createMa(record, lambda tier: (word.replace(":", "") for word in tier)),

    # Getting rid of single characters surrounded by parentheses
    "PhonBrackets": lambda record: createMa(record, lambda tier: (re.sub(r"\((.+)\)", r"\1", word) for word in tier)),

    "createMa": createMa,
    "clean": Record.clean
}

def process(inputFile, rules):
    with open(inputFile, 'r') as f:
        instance = parse(f)
        for rule in rules:
            cosa = [recordOperations[rule](record) for record in instance.records]
            instance.records = cosa
        instance.doPrint()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input text file")
    parser.add_argument('rules', metavar='rule', type=str, nargs='*', help='one of these: ' +", ".join(recordOperations.keys()))
    args = parser.parse_args()

    process(args.input, args.rules)
