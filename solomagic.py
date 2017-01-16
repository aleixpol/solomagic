#!/usr/bin/env python3

import argparse

class Block:
    def __init__(self, t = []):
        self.tiers = t

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
        for tier in self.tiers:
            print(" ".join(tier))

    def __repr__(self):
        return "Block(%s tiers)" % len(self.tiers)

class FileInstance:
    blocks = []

    def addBlock(self, block):
        self.blocks.append(block)

    def doPrint(self):
        first = True
        for block in self.blocks:
            if not first:
                print()
            block.doPrint()
            first = False

def parse(f):
    currentBlock = Block()
    ret = FileInstance()

    for line in f:
        line = line.rstrip()
        if not line:
            continue
        elif line.startswith("\\ref") and currentBlock.tiers:
            ret.addBlock(currentBlock)
            currentBlock = Block([])

        currentBlock.tiers.append(line.split())

    if currentBlock.tiers:
        ret.addBlock(currentBlock)
    return ret

def specialReplace(word, a, b):
    if "question" in word:
        return word
    else:
        return word.replace(a, b)

def createMa(block, function = None):
    mtTier = block.getTier("\\mt")
    maTier = ["\\ma"] + [word for word in mtTier[1:] if word != '/']
    if function:
        maTier = function(maTier)
    block.tiers.append(maTier)
    return block

blockOperations = {
    "QToApostrophe": lambda block: Block([ [specialReplace(word, "q", "'") for word in tier ] for tier in block.tiers]),
    "ApostropheToQ": lambda block: Block([ [word.replace("'", "q") for word in tier ] for tier in block.tiers]),
    "IvenaToIvaEna": lambda block: createMa(block, lambda tier: (word.replace("ivena", "iva ena") for word in tier)),
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
