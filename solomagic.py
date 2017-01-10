#!/usr/bin/env python3

import argparse

class Block:
    tiers = []

    def __init__(self, tiers = []):
        self.tiers = tiers

    def getTier(self, name):
        for v in self.tiers:
            if v[0] == name:
                return v
        raise "Scheisse"

    def setTier(self, name, value):
        assert value[0] == name
        print(self.tiers)
        for idx, v in enumerate(self.tiers):
            if v[0] == name:
                self.tiers[idx] = value
                return
        raise "Scheisse"

    def doPrint(self):
        for tier in self.tiers:
            print(" ".join(tier))

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
            currentBlock.tiers.append(line.split())

    ret.addBlock(currentBlock)
    return ret

def specialReplace(word, a, b):
    if "question" in word:
        return word
    else:
        return word.replace(a, b)

def createMa(block):
    mtTier = block.getTier("\\mt")
    maTier = ["\\ma"] + [word for word in mtTier[1:] if word != '/']
    block.tiers.append(maTier)
    return block

def potato(block):
    mtTier = block.getTier("\\mt")
    mtTier = ["\\mt"] + ["potato"+word for word in mtTier[1:] ]
    block.setTier("\\mt", mtTier)
    return block

blockOperations = {
    "QtoApostrophe": lambda block: Block([ [specialReplace(word, "q", "'") for word in tier ] for tier in block.tiers]),
    "IvenaToIvaEna": lambda block: Block([ [word.replace("ivena", "iva ena") for word in tier ] for tier in block.tiers]),
    "potato": potato,
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
