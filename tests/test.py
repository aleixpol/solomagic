import unittest
import subprocess

def callTest(fileNameInput, fileNameOutput = None, extraarg = []):
    if fileNameOutput == None:
        fileNameOutput = fileNameInput
    with open('testfile', 'wb') as f:
        ret = subprocess.check_call(["python3", "solomagic.py", fileNameInput] + extraarg, stdout=f)
        if ret != 0:
            return 1

    # I think whitespace changes don't matter
    return subprocess.check_call(["diff", "-ub", fileNameOutput, "testfile"])

class TestIO(unittest.TestCase):

    def test_invariant(self):
        self.assertEqual(callTest("tests/a.text.in"), 0)
        self.assertEqual(callTest("tests/b.text.in"), 0)
        self.assertEqual(callTest("tests/ivaena.text.in"), 0)

        self.assertEqual(callTest("tests/testapostrophe_mt.txt"), 0)
        self.assertEqual(callTest("tests/testivena_apostrophe_mt.txt"), 0)
        self.assertEqual(callTest("tests/testivena_mt.txt"), 0)
        self.assertEqual(callTest("tests/bv_cs_nihenatuna_pt.txt"), 0)

    def test_process(self):
        self.assertEqual(callTest("tests/a.text.in", "tests/a.text.out", ["QToApostrophe"]), 0)
        self.assertEqual(callTest("tests/b.text.in", "tests/b.text.out", ["createMa", "QToApostrophe"]), 0)

    def test_ivaena(self):
        self.assertEqual(callTest("tests/ivaena.text.in", "tests/ivaena.text.out", ["IvenaToIvaEna"]), 0)

        self.assertEqual(callTest("tests/testivena_mt.txt", "tests/testivena_ma.txt", ["createMa", "IvenaToIvaEna"]), 0)

if __name__ == '__main__':
    unittest.main()
