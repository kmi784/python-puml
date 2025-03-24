from inspect import getfile
from ast import (
    parse, 
    walk, 
    AST, 
    ClassDef, 
    FunctionDef, 
    Assign, 
    AnnAssign, 
    Attribute, 
    Name, 
    Subscript, 
    Tuple, 
    Constant, 
)

from puml.src import logger

class ExtractClassChart:
    def __init__(self, cls, kind : str = "class"):
        self.name: str = cls.__name__
        self.attributes: dict = {}
        self.methods: dict = {}
        if kind in ("class", "interface", "abstract"):
            self.kind: str = kind
        
        # get considered class
        with open(getfile(cls), "r") as file:
            tree = parse(file.read())
            for node in  tree.body:
                if isinstance(node, ClassDef) and node.name == self.name:
                    class_node = node

        # get attributes and methods
        for node in class_node.body:
            self._add_attribute(node, is_class_level=True) 
            if isinstance(node, FunctionDef): 
                self._add_method(node) 
                for subnode in walk(node):
                    self._add_attribute(subnode) 
                        
                
    def __repr__(self) -> str:
        output = f"\n{self.kind} {self.name}{{\n"
        for attribute in self.attributes.values():
            output += f"\t+{attribute}\n"
        output += "\n"
        for method in self.methods.values():
            output += f"\t+{method}\n"
        output += "}\n"
        return output
    

    def _add_attribute(self, node : AST, is_class_level: bool = False) -> None:

        def _get_name(arg: AST):
            if isinstance(arg, Subscript):
                return _get_name(arg.value)
            elif isinstance(arg, Tuple):
                return [name for n in arg.elts for name in _get_name(n)]
            elif isinstance(arg, Attribute) and isinstance(arg.value, Name) and arg.value.id == "self": 
                return [arg.attr]
            elif isinstance(arg, Name) and is_class_level:
                return [arg.id]
            else:
                return []
    
        if isinstance(node, Assign):
            for target in node.targets:
                names = _get_name(target)
                annotations = ["EMPTY"]*len(names)
        elif isinstance(node, AnnAssign): 
            names, annotations = _get_name(node.target), [node.annotation]
        else:
            return 

        for name, annotation in zip(names, annotations): 
            value = f"{name}: {self._format_type(annotation)}"
            if name in self.attributes:
                if (self.attributes[name].count("EMPTY") >= value.count("EMPTY")):
                    self.attributes[name] = value
            else:
                self.attributes[name] = value


    def _add_method(self, node : FunctionDef) -> None:
        # determines kind of method, 
        # i.e. "property", "staticmethod" or "classmethod"
        kind, decorators = "", ("staticmethod", "classmethod") 
        for subnode in node.decorator_list:
            if isinstance(subnode, Name):
                kind = "{static}" if subnode.id in decorators else f"{{{subnode.id}}}"
            elif isinstance(subnode, Attribute):
                kind = "{property}"
        # determines argument names and their types
        arguments = ", ".join([
            f"{arg.arg}: {self._format_type(arg.annotation)}" 
            for arg in node.args.args if arg.arg != "self"
        ])
        # determines return type
        if isinstance(node.returns, Constant):
            returns = node.returns.value 
        else: 
            returns = self._format_type(node.returns)
        # add attribute or method depending on kind
        if kind == "{property}":
            value = f"{node.name}: {returns}"
            if not (node.name in self.attributes
                    and any(t in value for t in ("None", "EMPTY"))):
                self.attributes[node.name] = value
        else:
            self.methods[node.name] = f"{kind}{node.name}({arguments})"\
                                  f" -> {returns}"


    def _format_type(self, node : AST) -> str:
        # handles typing annotation like Union, Tuple, etc.
        if isinstance(node, Subscript):
            base_type = node.value.id
            if isinstance(node.slice, Tuple):
                slice_type = ", ".join([self._format_type(t) for t in node.slice.elts])
            elif isinstance(node.slice, Subscript):
                slice_type = self._format_type(node.slice)  
            else:
                slice_type = node.slice.id
            return f"{base_type}[{slice_type}]"
        # handles basic annotation
        elif isinstance(node, Name):
            return f"{node.id}"
        # handles constant annotations like None
        elif isinstance(node, Constant):
            return f"{node.value}"
        return "EMPTY"

        
if __name__ == "__main__":
    from puml.test import MockClass


    obj = ExtractClassChart(MockClass, "class")
    logger.debug(obj)