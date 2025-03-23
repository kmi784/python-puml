from inspect import getfile
from ast import parse, walk, dump, AST, ClassDef, FunctionDef, Assign, AnnAssign, Attribute, Name, Subscript, Tuple, Constant

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

        # helper to handle (not) annotated attribute assignments 
        def _get_assignment(node : AST) -> None:
            if isinstance(node, Assign):
                for target in node.targets:
                    self._add_attribute(target)
            elif isinstance(node, AnnAssign): 
                self._add_attribute(node.target, node.annotation) 

        for node in class_node.body:
            _get_assignment(node) # get attributes at class level
            if isinstance(node, FunctionDef): 
                self._add_method(node) # get methods
                for subnode in walk(node):
                    _get_assignment(subnode) # get attributes at instance level 
                        
                
    def __repr__(self) -> str:
        output = f"{self.kind} {self.name}{{\n"
        for attribute in self.attributes.values():
            output += f"\t+{attribute}\n"
        output += "\n"
        for method in self.methods.values():
            output += f"\t+{method}\n"
        output += "}\n"
        return output
    

    def _add_attribute(self, node : AST, annotation : AST = None) -> None:
        if isinstance(node, Attribute) and node.value.id == "self":
            name = node.attr
        elif isinstance(node, Name):
            name = node.id
        value = f"{name}: {self._format_type(annotation)}"
        if name in self.attributes:
            if (self.attributes[name].count("EMPTY") 
                >= value.count("EMPTY")):
                self.attributes[name] = value
        else:
            self.attributes[name] = value


    def _add_method(self, node : FunctionDef) -> None:
        arguments = [f"{arg.arg}: {self._format_type(arg.annotation)}" 
                     for arg in node.args.args 
                     if arg.arg != "self"]
        returns = node.returns.value if isinstance(node.returns, Constant) else self._format_type(node.returns)

        self.methods[node.name] = f"{node.name}({", ".join(arguments)})"\
                                  f"-> {returns}"


    def _format_type(self, node : AST) -> str:
        # handles typing annotation like Union, Tuple, etc.
        if isinstance(node, Subscript):
            base_type = node.value.id
            if isinstance(node.slice, Tuple):
                slice_type = ", ".join([t.id for t in node.slice.elts])
            elif isinstance(node.slice, Subscript):
                slice_type = self._format_type(node.slice)  
            else:
                slice_type = node.slice.id
            return f"{base_type}[{slice_type}]"
        # handles basic annotation
        elif isinstance(node, Name):
            return f"{node.id}"
        else:
            return "EMPTY"

        
if __name__ == "__main__":
    from puml.test import MockClass, MockParent

    obj = ExtractClassChart(MockClass, "class")
    print(obj)
    obj = ExtractClassChart(MockParent, "abstract")
    print(obj)