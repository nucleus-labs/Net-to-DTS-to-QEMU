
from typing import Tuple, Union, Any
import re

import structs


def split_designator(designator: str) -> Tuple[Union[str, Any], ...]:
    match = re.match(r'([A-Za-z]+)(\d+)', designator)
    if match:
        return match.groups()
    else:
        raise Exception(f"Invalid designator provided: {match}")


def link(circuit: structs.Circuit):

    def build_dt_map(module: structs.Module) -> structs.Map_DeviceTree:
        mapping = structs.Map_DeviceTree()

        # ...

        return mapping


    for module in circuit.modules:
        if split_designator(module.ref)[0] == 'U':
            if 'dtsi' in module.fields:
                print(f'[{module}][dtsi]: {module.fields["dtsi"]}')
                build_dt_map(module)

            else:
                print(f'[{module}]')
                pass
