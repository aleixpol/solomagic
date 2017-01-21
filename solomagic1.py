import solomagic
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input text file")
    args = parser.parse_args()

    solomagic.process(args.input, ["XtoAsterisk", "SenaToSoEna", "SonaToSoOna", "VaToIva", "Veampeu", "qataToXta", "NgtaToXta", "ApostropheToQ", "IvenaToIvaEna"])
