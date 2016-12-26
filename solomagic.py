#!/usr/bin/env python3

import argparse

class Block:
    entries = []

    def __init__(self, entries = []):
        self.entries = entries

    def getEntry(self, name):
        for v in self.entries:
            if v[0] == name:
                return v
        raise "Scheisse"

    def setEntry(self, name, value):
        assert value[0] == name
        print(self.entries)
        for idx, v in enumerate(self.entries):
            if v[0] == name:
                self.entries[idx] = value
                return
        raise "Scheisse"

    def doPrint(self):
        for entry in self.entries:
            print(" ".join(entry))

class FileInstance:
    blocks = []

    def addBlock(self, block):
        self.blocks.append(block)

    def doPrint(self):
        for block in self.blocks:
            block.doPrint()

def parse(f):
    currentBlock = Block()
    ret = FileInstance()

    for line in f:
        line = line.rstrip()
        if len(line) == 0:
            ret.addBlock(currentBlock)
            currentBlock = Block()
        else:
            currentBlock.entries.append(line.split())

    ret.addBlock(currentBlock)
    return ret

def specialReplace(word, a, b):
    if "question" in word:
        return word
    else:
        return word.replace(a, b)

def createMa(block):
    mtEntry = block.getEntry("\\mt")
    maEntry = ["\\ma"] + [word for word in mtEntry[1:] if word != '/']
    block.entries.append(maEntry)
    return block

blockOperations = {
    "QtoApostrophe": lambda block: Block([ [specialReplace(word, "q", "'") for word in entry ] for entry in block.entries]),
    "IvenaToIvaEna": lambda block: Block([ [word.replace("ivena", "iva ena") for word in entry ] for entry in block.entries]),
    "createMa": createMa
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input text file")
    parser.add_argument('rules', metavar='rule', type=str, nargs='*', help='one of these: ' +", ".join(blockOperations.keys()))
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        instance = parse(f)
        for rule in args.rules:
            cosa = [blockOperations[rule](block) for block in instance.blocks]
            instance.blocks = cosa
        instance.doPrint()
