from inspect import (
    getmembers,
    getfullargspec, 
    getattr_static, 
    isfunction, 
    ismethod, 
)
from typing import (
    List, 
    Type, 
    Union, 
    get_args,
    get_origin,
    get_type_hints, 
)
     

class ExtractClassChart:
    name : str
    attributes: List[str]
    methods: List[str]
    kind : str

    def __init__(self, cls, kind : str = "class"):
        self.name = cls.__name__
        self.attributes = []
        self.methods = []
        if kind in ("class", "interface", "abstract"):
            self.kind = kind
        else:
            raise ValueError(f"\"{kind}\" is not a plantuml-class-type!")

        for name, return_type in get_type_hints(cls).items():
            if name[0] != "_":
                if any(name in base.__annotations__ for base in cls.__bases__):
                    self.attributes.append(f"+{{abstract}}{name}: {ExtractClassChart._format(return_type)}")
                else:
                    self.attributes.append(f"+{name}: {ExtractClassChart._format(return_type)}")


        def check(method_name, method_kind) -> bool:
            return isinstance(getattr_static(cls, method_name), method_kind)
        
        def hint(member) -> str:

            hints = get_type_hints(member)
            for arg in getfullargspec(member).args:
                if arg not in ("self", "cls"):
                    hints[arg] = self._format(self._format(hints[arg])) if arg in hints else "EMPTY"

            return_type = f"{self._format(hints.pop("return"))}" if "return" in hints else "EMPTY"
            arg_type = ", ".join([f"{key}: {value}" for key, value in hints.items()])
            return arg_type, return_type


        for name, object in getmembers(cls):
            if name[0] != "_":
                if check(name, property):
                    _, returns = hint(object.fget)
                    self.attributes.append(f"+{name}: {returns}")

                else:
                    args, returns = hint(object)
                    if check(name, staticmethod) or check(name, classmethod):
                        self.methods.append(f"+{{static}}{name}({args}) -> {returns}")

                    else:
                        if any(hasattr(base, name) for base in cls.__bases__):
                            self.methods.append(f"+{{abstract}}{name}({args}) -> {returns}")

                        elif isfunction(object) or ismethod(object):
                            self.methods.append(f"+{name}({args}) -> {returns}")
    
    @staticmethod
    def _format(data_type : Type):
        origin = get_origin(data_type)
        args = get_args(data_type)

        if origin:
            name = origin.__name__ if hasattr(origin, '__name__') else str(origin)
            args_str = ', '.join(ExtractClassChart._format(arg) for arg in args)
            return f"{name}[{args_str}]"

        if getattr(data_type, '__origin__', None) is Union and type(None) in args:
            non_none = [arg for arg in args if arg is not type(None)][0]
            return f"Optional[{ExtractClassChart._format(non_none)}]"

        if hasattr(data_type, '__name__'):
            return data_type.__name__

        return str(data_type).replace('typing.', '')


    def __repr__(self) -> str:
        output = f"{self.kind} {self.name}{{\n"

        for attribute in self.attributes:
            output += f"\t{attribute}\n"

        output += "\n"

        for method in self.methods:
            output += f"\t{method}\n"

        output += "}\n"

        return output


if __name__ == "__main__":
    from puml.test import MockClass

    obj = ExtractClassChart(MockClass, "class")
    print(obj)