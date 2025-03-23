from dataclasses import dataclass
from typing import Union, Dict, List, Tuple, Optional

import pytest

from puml.src import ExtractClassChart
from puml.test import MockCore, MockClass


class MockVoid:
    pass

def test_init_void_class():
    obj = ExtractClassChart(MockVoid)
    assert obj.name == "MockVoid"
    assert len(obj.attributes) == 0 and len(obj.methods) == 0
    assert obj.kind == "class"


class MockSingleAttribute:
    def __init__(self):
        self.attr = None

def test_init_single_attribute_class():
    obj = ExtractClassChart(MockSingleAttribute, "class")
    assert obj.name == "MockSingleAttribute"
    assert len(obj.attributes) == 1 and len(obj.methods) == 1
    assert all(key == "attr" and "attr" in value
               for key, value in obj.attributes.items())
    assert obj.kind == "class"


class MockSingleMethod:
    def method(self, arg):
        pass

def test_init_single_method_class():
    obj = ExtractClassChart(MockSingleMethod, "interface")
    assert obj.name == "MockSingleMethod"
    assert len(obj.attributes) == 0 and len(obj.methods) == 1
    assert all(key == "method" and "method(arg" in value
               for key, value in obj.methods.items())
    assert obj.kind == "interface"


@dataclass
class MockDataClass:
    attr : int 

def test_init_data_class():
    obj = ExtractClassChart(MockDataClass)
    assert obj.name == "MockDataClass"
    assert len(obj.attributes) == 1 and len(obj.methods) == 0
    assert all(key == "attr" and "attr" in value
               for key, value in obj.methods.items())
    assert obj.kind == "class"


class MockComplexAnnotations:
    def __init__(self):
        self.attr1: Union[int, None, float]
        self.attr2: Optional[float]
        self.attr3: Tuple[int, MockCore, Union[int, float]]
        self.attr4: List[Union[bool, Optional[float]]]

    def method(self, arg: List[Union[None, MockCore]]) -> Dict[str, Optional[MockCore]]:
        pass

def test_init_complex_attribute_types():
    obj = ExtractClassChart(MockComplexAnnotations)
    assert "Union[int, None, float]" in obj.attributes["attr1"] 
    assert "Optional[float]" in obj.attributes["attr2"] 
    assert "Tuple[int, MockCore, Union[int, float]]" in obj.attributes["attr3"] 
    assert "List[Union[bool, Optional[float]]]" in obj.attributes["attr4"] 
    assert "List[Union[None, MockCore]]" in obj.methods["method"]
    assert "Dict[str, Optional[MockCore]]" in obj.methods["method"]


class MockClassLevelAnnotation:
    attr: dict 
    def __init__(self):
        self.attr = {}

class MockInstanceLevelAnnotation:
    def __init__(self):
        self.attr: dict = {}

class MockNoAnnotation:
    def __init__(self):
        self.attr = {}

class MockBothAnnotation:
    attr: dict
    def __init__(self):
        self.attr: dict = {}

def test_init_attribute_annotation():
    obj_class_level = ExtractClassChart(MockClassLevelAnnotation)
    assert "dict" in obj_class_level.attributes["attr"] 
    obj_instance_level = ExtractClassChart(MockInstanceLevelAnnotation)
    assert "dict" in obj_instance_level.attributes["attr"] 
    obj_no = ExtractClassChart(MockNoAnnotation)
    assert "EMPTY" in obj_no.attributes["attr"] 
    obj_both = ExtractClassChart(MockBothAnnotation)
    assert "dict" in obj_both.attributes["attr"]


def test_init_property():
    obj = ExtractClassChart(MockClass)
    assert "core" in obj.attributes
    assert "core: bool" == obj.attributes["core"]
    assert "core" not in obj.methods


def test_init_staticmethod_classmethod():
    obj = ExtractClassChart(MockClass)
    assert "{static}" in obj.methods["static_method"]
    assert "{static}" in obj.methods["class_method"]
 

if __name__ == "__main__":
    pass