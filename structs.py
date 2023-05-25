#
#   ExportDTS KiCAD Plugin ; structs.py   
#
#   Copyright Maxine Alexander, All Rights Reserved
#
#   structs.py contains classes used by several of this plugin's modules for
#   representing a given schematic
#

import pydevicetree
import sexpdata

from typing import List, Dict, Any
import uuid


class Pin:
    parent:         'Module'
    name:           str
    number:         str
    no_connect:     bool

class Field:
    name:       str
    value:      Any

    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
    
    def __str__(self):
        return f"({self.name}, {self.value})"


class Module:
    ref:            str
    fields:         Dict[str, Field]
    pins:           List[Pin]
    device_tree:    'Map_DeviceTree'

    def __init__(self):
        self.ref    = ''
        self.fields = {}
        self.pins   = []
    
    def __str__(self):
        return f"{self.name}:{self.ref}"
    
    @property
    def name(self):
        return self.fields["name"].value


class Wire:
    connections:    List[Pin]
    state:          float


class Circuit:
    name:           str
    modules:        List[Module]
    wires:          List[Wire]

    def __init__(self):
        self.name       = ''
        self.modules    = []
        self.wires      = []


class Map_DeviceTree:
    pass
