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
        
        self.assertEqual(callTest("asterix.text.in"), 0)
        self.assertEqual(callTest("veampeu.text.in"), 0)
        self.assertEqual(callTest("vatoiva.text.in"), 0)
        self.assertEqual(callTest("soona.text.in"), 0)
        self.assertEqual(callTest("soena.text.in"), 0)
        
        self.assertEqual(callTest("deleteqm.text.in"), 0)
        self.assertEqual(callTest("colon.text.in"), 0)
        self.assertEqual(callTest("phonbrack.text.in"), 0)
        
        self.assertEqual(callTest("testapostrophe_mt.txt"), 0)
        self.assertEqual(callTest("testivena_apostrophe_mt.txt"), 0)
        self.assertEqual(callTest("testivena_mt.txt"), 0)
        self.assertEqual(callTest("testivena_ma.txt"), 0)
        self.assertEqual(callTest("bv_cs_nihenatuna_pt.txt"), 0)        
       

    def test_process(self):
        self.assertEqual(callTest("a.text.in", "a.text.out", ["ApostropheToQ"]), 0)
        self.assertEqual(callTest("b.text.in", "b.text.out", ["createMa", "ApostropheToQ"]), 0)
        self.assertEqual(callTest("asterix.text.in", "asterix.text.out", ["XtoAsterisk"]), 0)
        self.assertEqual(callTest("veampeu.text.in", "veampeu.text.out", ["Veampeu"]), 0)
        self.assertEqual(callTest("vatoiva.text.in", "vatoiva.text.out", ["VaToIva"]), 0) 
        self.assertEqual(callTest("soona.text.in", "soona.text.out", ["SonaToSoOna"]), 0)
        self.assertEqual(callTest("soena.text.in", "soena.text.out", ["SenaToSoEna"]), 0)

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
    	
    def test_delete(self):
    	self.assertEqual(callTest("deleteqm.text.in", "deleteqm.text.out", ["DeleteQM"]), 0)
    	self.assertEqual(callTest("colon.text.in", "colon.text.out", ["DeleteColon"]), 0)
    	self.assertEqual(callTest("phonbrack.text.in", "phonbrack.text.out", ["PhonBrackets"]), 0)
        
   
if __name__ == '__main__':
    unittest.main()
