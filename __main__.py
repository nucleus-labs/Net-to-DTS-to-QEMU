#
#   ExportDTS KiCAD Plugin ; __main__.py   
#
#   Copyright Maxine Alexander, All Rights Reserved
#
#

import argparse

from net_reader import generate_circuit
from dts import link


def main(args: argparse.Namespace):
    circuit = generate_circuit(args.input_file)
    link(args, circuit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KiCAD_TO_DTS - converts a KiCAD schematic to a dts file for QEMU emulation')

    parser.add_argument("input_file", help="the schematic file to parse ; should be a `.net` file.")
    parser.add_argument("-a", "--action", choices=["dts", "dtsi", "img_graph"], help="What to generate.")
    parser.add_argument("-o", "--output_dir", help="The directory for where to write the generated DTS files")
    parser.add_argument("-I", "--include_src", action="append", help="The main directory for DTSI files referenced by the netlist fields")
    parser.add_argument("-i", "--include", action='append', help="add an include directory for DTS/DTSI files")

    args = parser.parse_args()

    if args.include is None:
        args.include = []
    if args.include_src is None:
        args.include_src = []

    main(args)
