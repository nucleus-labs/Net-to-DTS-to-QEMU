
import argparse

from net_reader import generate_circuit
from dts import link


def main(args: argparse.Namespace):
    circuit = generate_circuit(args.input_file)
    link(circuit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KiCAD_TO_DTS - converts a KiCAD schematic to a dts file for QEMU emulation')

    parser.add_argument("input_file", help="the schematic file to parse ; should be a `.kicad_sch` file.")
    parser.add_argument("-a", "--action", choices=["dts", "dtsi", "img_graph"], help="What to generate.")
    parser.add_argument("-o", "--output", help="The name of the generated file")

    args = parser.parse_args()

    main(args)
