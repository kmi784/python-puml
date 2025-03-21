from dataclasses import dataclass, field, Field

import pytest

from puml.src import ExtractClassChart
from puml.test import MockParent, MockClass

class MockVoid:
    pass

class MockSingleAttribute:
    attr: int
    def __init__(self):
        self.attr = None

class MockSingleMethod:
    def method(self, arg):
        pass

class MockInherited(MockParent):
    def __init__(self):
        super().__init__()

@dataclass
class MockDataClass:
    attr : int 


def test_init_void_class():
    obj = ExtractClassChart(MockVoid)
    assert obj.name == "MockVoid"
    assert len(obj.attributes) == 0 and len(obj.methods) == 0
    assert obj.kind == "class"

def test_init_single_attribute_class():
    obj = ExtractClassChart(MockSingleAttribute, "class")
    assert obj.name == "MockSingleAttribute"
    assert len(obj.attributes) == 1 and len(obj.methods) == 0
    assert obj.attributes[0] == "+attr: int"
    assert obj.kind == "class"

def test_init_single_method_class():
    obj = ExtractClassChart(MockSingleMethod, "interface")
    assert obj.name == "MockSingleMethod"
    assert len(obj.attributes) == 0 and len(obj.methods) == 1
    assert obj.methods[0] == "+method(arg: EMPTY) -> EMPTY"
    assert obj.kind == "interface"

def test_init_inherited_class():
    obj = ExtractClassChart(MockInherited, "abstract")
    assert obj.name == "MockInherited"
    assert len(obj.attributes) == 1 and len(obj.methods) == 1
    assert obj.methods[0] == "+{abstract}abstract_method(arg: bool) -> bool"
    assert obj.attributes[0] == "+{abstract}attr_abstract: bool"
    assert obj.kind == "abstract"

def test_init_data_class():
    obj = ExtractClassChart(MockDataClass)
    assert obj.name == "MockDataClass"
    assert len(obj.attributes) == 1 and len(obj.methods) == 0
    assert obj.attributes[0] == "+attr: int"
    assert obj.kind == "class"

def test_init_wrong_puml_class_type():
    with pytest.raises(ValueError):
        ExtractClassChart(MockVoid, "afqvegf")

def test_init_functionality():
    obj = ExtractClassChart(MockClass)
    assert "+{abstract}attr_abstract: bool" in obj.attributes
    assert "+attr_basic: int" in obj.attributes
    assert "+attr_union: Union[int, float]" in obj.attributes
    assert "+attr_list: list[MockCore]" in obj.attributes
    assert "+attr_tuple: tuple[int, MockCore]" in obj.attributes
    assert "+core: bool" in obj.attributes
    assert "+_core: bool" not in obj.attributes
    assert "+{abstract}abstract_method(arg: bool) -> bool" in obj.methods
    assert "+_help_method() -> NoneType" not in obj.methods
    assert "+basic_method(arg1: MockCore, arg2: MockCore) -> list[Union[int, float]]" in obj.methods
    assert "+{static}class_method() -> NoneType" in obj.methods
    assert "+{static}static_method(arg: str) -> NoneType" in obj.methods

def test_hint_functionality():
    pass

def test_format_functionality():
    pass

if __name__ == "__main__":
    pass