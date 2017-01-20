import unittest
import subprocess

def callTest(fileNameInput, fileNameOutput = None, extraarg = []):
    if fileNameOutput == None:
        fileNameOutput = fileNameInput

    command = ["python3", "solomagic.py", "tests/" + fileNameInput] + extraarg
    with open('testfile', 'wb') as f:
        ret = subprocess.check_call(command, stdout=f)
        if ret != 0:
            return 1

    # I think whitespace changes don't matter
    ret = 0
    try:
        subprocess.check_call(["diff", "-ub", "tests/" + fileNameOutput, "testfile"])
    except:
        print("Differences between: '%s' and tests/%s" % (" ".join(command), fileNameOutput))
        ret = 1
    return ret

class TestIO(unittest.TestCase):

    def test_invariant(self):
        self.assertEqual(callTest("a.text.in"), 0)
        self.assertEqual(callTest("b.text.in"), 0)
        self.assertEqual(callTest("ivaena.text.in"), 0)

        self.assertEqual(callTest("testapostrophe_mt.txt"), 0)
        self.assertEqual(callTest("testivena_apostrophe_mt.txt"), 0)
        self.assertEqual(callTest("testivena_mt.txt"), 0)
        self.assertEqual(callTest("testivena_ma.txt"), 0)
        self.assertEqual(callTest("bv_cs_nihenatuna_pt.txt"), 0)

    def test_process(self):
        self.assertEqual(callTest("a.text.in", "a.text.out", ["ApostropheToQ"]), 0)
        self.assertEqual(callTest("b.text.in", "b.text.out", ["createMa", "ApostropheToQ"]), 0)

    def test_ivaena(self):
        self.assertEqual(callTest("ivaena.text.in", "ivaena.text.out", ["IvenaToIvaEna"]), 0)

        self.assertEqual(callTest("testivena_mt.txt", "testivena_ma.txt", ["IvenaToIvaEna"]), 0)

if __name__ == '__main__':
    unittest.main()
