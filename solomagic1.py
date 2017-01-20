import solomagic

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input text file")
    args = parser.parse_args(args.input)

    process(parser.input, ["XtoAsterisk", "SenaToSoEna", "SonaToSoOna", "VaToIva", "Veampeu", "qataToXta", "NgtaToXta", "ApostropheToQ", "IvenaToIvaEna"])
