from typing import List, Tuple, Union

class MockCore:
    pass

class MockParent:
    attr_abstract : bool

    def __init__(self):
        self.attr_abstract = True

    def abstract_method(self, arg: bool) -> bool:
        return (self.attr_abstract and arg)

class MockClass(MockParent):
    _core: bool
    attr_basic: int
    attr_union: Union[int, float]
    attr_list: List[MockCore]
    attr_tuple: Tuple[int, MockCore]


    def __init__(self):
        super().__init__()
        self._core: bool = self.attr_abstract
        self.attr_basic: int = None
        self.attr_union: Union[int, float] = None
        self.attr_list: List[MockCore] = None
        self.attr_tuple: Tuple[int, MockCore] = None

    @property
    def core(self):
        pass

    @core.getter
    def core(self) -> bool:
        return self._core

    @core.setter
    def core(self, arg : bool) -> None:
        self._core = arg

    def _help_method(self) -> None:
        pass

    def basic_method(self, arg1 : MockCore, arg2 : MockCore) -> List[Union[int, float]]:
        self._help_method()

    @staticmethod
    def static_method(arg : str) -> None:
        pass

    @classmethod
    def class_method(cls) -> None:
        pass






if __name__ == "__main__":

    from inspect import getmembers, getattr_static, isfunction, ismethod
    from typing import get_type_hints

    class_info = {
        "attributes": [],
        "properties": [],
        "methods": [],
        "static methods": [],
        "class methods": [],
        "abstract methods": [],
    }

    def add(kind, name, type_info):
        class_info[kind].append(f"{name}: {type_info}")


    # attributes
    hints = get_type_hints(MockClass)
    for name, value in hints.items():
        add("attributes", name, value)

    # methods
    for name, member in getmembers(MockClass):
        if name[:2] != "__":
                
                member = getattr_static(MockClass, name)

                # abstract methods
                if any(hasattr(base, name) for base in MockClass.__bases__):
                    add("abstract methods", name, get_type_hints(member))

                # properties
                elif isinstance(member, property):
                    add("properties", name, get_type_hints(member.fget))
                    
                # static methods
                elif isinstance(member, staticmethod):
                    add("static methods", name, get_type_hints(member))
                    
                # class methods
                elif isinstance(member, classmethod):
                    add("class methods", name, get_type_hints(member))
                    
                # basic methods
                elif ismethod(member) or isfunction(member): 
                    add("methods", name, get_type_hints(member))

                else:
                    raise NotImplementedError(f"{member} is not excepted!")


    for key, values in class_info.items():
        print(key,"\b:")
        for value in values:
            print(" ->", value)