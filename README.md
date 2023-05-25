# Net to DTS to QEMU

Net to DTS to QEMU is a command-line tool that converts KiCAD schematic files to Device Tree Source (DTS) files for QEMU emulation. It enables the translation of circuit designs into a format that can be understood by the QEMU emulator, allowing you to simulate and test hardware designs.


## Installation

You can install Net2DTS2QEMU using pip: ***NOT YET IMPLEMENTED***
```bash
pip install net2dts2qemu
```

## Usage

The Net2DTS2QEMU command-line tool can be used with the following syntax:
```
usage: net2dts2qemu [-h] [-a {dts,dtsi,img_graph}] [-o OUTPUT_DIR]
                    [-I INCLUDE_SRC] [-i INCLUDE]
                    input_file

net2dts2qemu - converts a circuit schematic netlist to a dts file for QEMU emulation

positional arguments:
  input_file            the schematic file to parse ; should be a `.net` file.

optional arguments:
  -h, --help            show this help message and exit
  -a {dts,dtsi,img_graph}, --action {dts,dtsi,img_graph}
                        What to generate.
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        The directory for where to write the generated DTS
                        files
  -I INCLUDE_SRC, --include_src INCLUDE_SRC
                        The main directory for DTSI files referenced by the
                        netlist fields
  -i INCLUDE, --include INCLUDE
                        add an include directory for DTS/DTSI files
```

## Timeline

- [X] Parse the net file to locate ICs with a "DTSI" field
- [ ] Parse the provided DTSI files to generate a component graph and IC graphs
  - It seems there's a hiccup. Both python libraries I found that provide device tree bindings only want to parse DTS files, not DTSI files. A custom library will be needed.
    - [ ] [PyDTSI](#)
- [ ] Parse the net file to update the component graph, disregarding non-IC components
- [ ] Export an updated DTS for each processor
- [ ] Export QEMU command line arguments for 
