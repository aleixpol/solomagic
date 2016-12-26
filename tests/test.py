import unittest
import subprocess

def callTest(fileNameInput, fileNameOutput = None, extraarg = []):
    if fileNameOutput == None:
        fileNameOutput = fileNameInput
    with open('testfile', 'wb') as f:
        subprocess.check_call(["python3", "solomagic.py", fileNameInput] + extraarg, stdout=f)

    # I think whitespace changes don't matter
    return subprocess.check_call(["diff", "-ub", "testfile", fileNameOutput])

class TestIO(unittest.TestCase):

    def test_invariant(self):
        self.assertEqual(callTest("tests/a.text.in"), 0)
        self.assertEqual(callTest("tests/b.text.in"), 0)

    def test_process(self):
        self.assertEqual(callTest("tests/a.text.in", "tests/a.text.out", ["QtoApostrophe"]), 0)
        self.assertEqual(callTest("tests/b.text.in", "tests/b.text.out", ["createMa", "QtoApostrophe"]), 0)

    def test_ivaena(self):
        self.assertEqual(callTest("tests/ivaena.text.in", "tests/ivaena.text.out", ["IvenaToIvaEna"]), 0)

if __name__ == '__main__':
    unittest.main()
