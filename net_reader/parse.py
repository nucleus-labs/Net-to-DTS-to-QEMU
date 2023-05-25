#
#   ExportDTS KiCAD Plugin ; net_reader/parse.py   
#
#   Copyright Maxine Alexander, All Rights Reserved
#
#

import sexpdata

from typing import cast, List, Tuple, Union, Dict, Optional, Callable, Any
import collections
import json
import re

import structs


SEXP_SCH_LABELS: Dict[str, Callable] = {
    'version':          lambda x: None,
    'thickness':        lambda x: None,
    'offset':           lambda x: None,
    'mid':              lambda x: None,
    'radius':           lambda x: None,
    'label':            lambda x: None,
    'in_bom':           lambda x: None,
    'color':            lambda x: None,
    'kicad_sch':        lambda x: None,
    'lib_id':           lambda x: None,
    'pts':              lambda x: None,
    'fill':             lambda x: None,
    'size':             lambda x: None,
    'junction':         lambda x: None,
    'circle':           lambda x: None,
    'text':             lambda x: None,
    'symbol_instances': lambda x: None,
    'property':         lambda x: None,
    'end':              lambda x: None,
    'diameter':         lambda x: None,
    'xy':               lambda x: None,
    'at':               lambda x: None,
    'unit':             lambda x: None,
    'symbol':           lambda x: None,
    'path':             lambda x: None,
    'no_connect':       lambda x: None,
    'wire':             lambda x: None,
    'number':           lambda x: None,
    'generator':        lambda x: None,
    'name':             lambda x: None,
    'sheet_instances':  lambda x: None,
    'justify':          lambda x: None,
    'id':               lambda x: None,
    'lib_symbols':      lambda x: None,
    'global_label':     lambda x: None,
    'width':            lambda x: None,
    'length':           lambda x: None,
    'font':             lambda x: None,
    'paper':            lambda x: None,
    'stroke':           lambda x: None,
    'shape':            lambda x: None,
    'page':             lambda x: None,
    'on_board':         lambda x: None,
    'rectangle':        lambda x: None,
    'footprint':        lambda x: None,
    'center':           lambda x: None,
    'value':            lambda x: None,
    'reference':        lambda x: None,
    'lib_name':         lambda x: None,
    'uuid':             lambda x: None,
    'type':             lambda x: None,
    'arc':              lambda x: None,
    'pin':              lambda x: None,
    'pin_names':        lambda x: None,
    'start':            lambda x: None,
    'polyline':         lambda x: None,
    'effects':          lambda x: None,
    'pin_numbers':      lambda x: None
}

SEXP_NET_LABELS: Dict[str, Optional[Callable]] = {
    'footprints':       lambda x, circuit: None,
    'rev':              lambda x, circuit: None,
    'fields':           lambda x, circuit: None,
    'field':            lambda x, circuit: None,
    'comment':          lambda x, circuit: None,
    'value':            lambda x, circuit: None,
    'property':         lambda x, circuit: None,
    'library':          lambda x, circuit: None,
    'footprint':        lambda x, circuit: None,
    'All':              lambda x, circuit: None,
    'ref':              lambda x, circuit: None,
    'names':            lambda x, circuit: None,
    'libparts':         lambda x, circuit: None,
    'pins':             lambda x, circuit: None,
    'node':             lambda x, circuit: None,
    'logical':          lambda x, circuit: None,
    'title':            lambda x, circuit: None,
    'pin':              lambda x, circuit: None,
    'design':           lambda x, circuit: None,
    'date':             lambda x, circuit: None,
    'nets':             lambda x, circuit: None,
    'lib':              lambda x, circuit: None,
    'fp':               lambda x, circuit: None,
    'number':           lambda x, circuit: None,
    'type':             lambda x, circuit: None,
    'version':          lambda x, circuit: None,
    'libsource':        lambda x, circuit: None,
    'datasheet':        lambda x, circuit: None,
    'uri':              lambda x, circuit: None,
    'sheet':            lambda x, circuit: None,
    'name':             lambda x, circuit: None,
    'part':             lambda x, circuit: None,
    'sheetpath':        lambda x, circuit: None,
    'components':       lambda x, circuit: None,
    'docs':             lambda x, circuit: None,
    'tool':             lambda x, circuit: None,
    'pinfunction':      lambda x, circuit: None,
    'comp':             lambda x, circuit: None,
    'num':              lambda x, circuit: None,
    'net':              lambda x, circuit: None,
    'title_block':      lambda x, circuit: None,
    'description':      lambda x, circuit: None,
    'tstamps':          lambda x, circuit: None,
    'export':           lambda x, circuit: None,
    'code':             lambda x, circuit: None,
    'source':           lambda x, circuit: None,
    'company':          lambda x, circuit: None,
    'libraries':        lambda x, circuit: None,
    'libpart':          lambda x, circuit: None,
    'pintype':          lambda x, circuit: None
}

SCHEM_TYPE = Union[sexpdata.Symbol, str, Tuple['SCHEM_TYPE', ...]]


class BuildState:
    circuit:            structs.Circuit
    current_module:     Optional[structs.Module]

    def __init__(self):
        self.circuit = structs.Circuit()
        self.current_module = None



def generate_circuit(schematic_file: str) -> structs.Circuit:
    if not schematic_file.endswith('.net'):
        schematic_file = schematic_file + '.net'
    with open(schematic_file, 'r') as file:
        schem: SCHEM_TYPE = sexpdata.loads(file.read())

    current_state = BuildState()

    def find_processors(expr: SCHEM_TYPE, parent: Any, state: BuildState) -> None:

        if not parent:
            parent = state.circuit

        for item in expr:
            if isinstance(item, collections.abc.Iterable) and not isinstance(item, str):
                sexp = cast(Tuple[SCHEM_TYPE], item)
                sexp_label = cast(str, sexp[0]).lower()

                if len(sexp) < 2: continue

                # print(sexp_label)
                if sexp_label == "value":
                    if type(parent) is not structs.Module: continue
                    _field = structs.Field("name", sexp[1])
                    cast(structs.Module, state.current_module).fields["name"] = _field

                    find_processors(sexp, _field, state)
                    
                elif sexp_label == "comp":
                    state.current_module = structs.Module()
                    state.circuit.modules.append(state.current_module)
                    find_processors(sexp, state.current_module, state)
                    state.current_module = None

                elif sexp_label == "ref":
                    if state.current_module is None: continue
                    state.current_module.ref = sexp[1]
                    find_processors(sexp, state.current_module.ref, state)

                elif sexp_label == "field":
                    if state.current_module is None: continue
                    try:
                        assert((str(sexp[1][0]) == "name") and "Field provided does not contain a name ; should never happen")
                    except Exception as e:
                        print(sexp)
                        raise e
                    _field = structs.Field(sexp[1][1].lower(), sexp[2])
                    state.current_module.fields[_field.name] = _field
                    find_processors(sexp, _field, state)

                elif sexp_label == 'property':
                    continue
                
                else:
                    find_processors(sexp, parent, state)


    find_processors(schem, None, current_state)

    # def iter_schem(schem: SCHEM_TYPE) -> None:
    #     for item in schem:
    #         if isinstance(item, collections.Iterable):
    #             if str(item[0]) in SEXP_NET_LABELS:
    #                 SEXP_NET_LABELS[str(item[0])](item, circuit)
    #                 iter_schem(item)
    #             else:
    #                 raise Exception(f"This error should never happen ; iter_schem(schem)'s schem contains an unrecognized symbol: [{item[0]}]")

    #         elif isinstance(item, str):
    #             # what else is needed?
    #             continue
    #         else:
    #             raise Exception(f"This error should never happen ; iter_schem(schem) was passed an item that is neither an iterable nor a symbol: [{type(item)}]")
            
    # iter_schem(schem)

    return current_state.circuit


if __name__ == '__main__':
    generate_circuit("C:/Users/ThePi/Documents/Circuits/k210/sound_field_imager/sound_field_imager.net")

