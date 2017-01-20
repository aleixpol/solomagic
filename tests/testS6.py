import unittest
import subprocess

def callTest(fileNameInput, fileNameOutput = None, extraarg = []):
    if fileNameOutput == None:
        fileNameOutput = fileNameInput
    with open('testfile', 'wb') as f:
        ret = subprocess.check_call(["python3", "solomagic.py", "tests/" + fileNameInput] + extraarg, stdout=f)
        if ret != 0:
            return 1

    # I think whitespace changes don't matter
    return subprocess.check_call(["diff", "-ub", "tests/" + fileNameOutput, "testfile"])

class TestIO(unittest.TestCase):

    def test_invariant(self):
        self.assertEqual(callTest("a.text.in"), 0)
        self.assertEqual(callTest("b.text.in"), 0)
        self.assertEqual(callTest("ivaena.text.in"), 0)
        self.assertEqual(callTest("realivaena.text.in"), 0)     
        
        self.assertEqual(callTest("ata.text.in"), 0)
        self.assertEqual(callTest("eta.text.in"), 0)
        self.assertEqual(callTest("ita.text.in"), 0)
        self.assertEqual(callTest("ota.text.in"), 0)
        self.assertEqual(callTest("uta.text.in"), 0)
        self.assertEqual(callTest("ngta.text.in"), 0)
        
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
     	self.assertEqual(callTest("realivaena.text.in", "realivaena.text.out", ["IvenaToIvaEna"]), 0)
        self.assertEqual(callTest("testivena_mt.txt", "testivena_ma.txt", ["IvenaToIvaEna"]), 0)
        
    def test_xta(self):
    	self.assertEqual(callTest("ata.text.in", "ata.text.out", ["ataToXta"]), 0)    	
    	self.assertEqual(callTest("eta.text.in", "eta.text.out", ["etaToXta"]), 0)
    	self.assertEqual(callTest("ita.text.in", "ita.text.out", ["itaToXta"]), 0)
    	self.assertEqual(callTest("ota.text.in", "ota.text.out", ["otaToXta"]), 0)
    	self.assertEqual(callTest("ota.text.in", "ota.text.out", ["otaToXta"]), 0)
    	self.assertEqual(callTest("uta.text.in", "uta.text.out", ["utaToXta"]), 0)
    	self.assertEqual(callTest("ngta.text.in", "ngta.text.out", ["ngtaToXta"]), 0)
    	
        
   
if __name__ == '__main__':
    unittest.main()
