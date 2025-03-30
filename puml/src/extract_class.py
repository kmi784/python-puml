"""
This module contains the "ClassChart"-class for extracting puml syntax form the source
code by the usage of the ast-package.
"""

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
from inspect import getfile

from puml.src import logger


class ClassChart:
    """
    Collection of all members in a target-class with there corresponding uml-expression.

    Parameters
    ----------
    cls : type
    kind : "abstract", "class" or "interface"}


    Attributes
    ----------
    name : str
        Name of the passed type-object
    kind : str
        Name of uml-class-diagramm-type
    attributes : {"name": "puml syntax"}
        Names of attributes and properties mapped to there uml-expressions
    methods : {"name": "puml syntax"}
        Names of attributes and properties mapped to there uml-expressions
    """

    def __init__(self, cls: type, kind: str = "class"):
        self.name: str = cls.__name__
        self.attributes: dict = {}
        self.methods: dict = {}
        if kind in ("class", "interface", "abstract"):
            self.kind: str = kind

        # get considered class
        with open(getfile(cls), "r") as file:
            tree = parse(file.read())
            for node in tree.body:
                if isinstance(node, ClassDef) and node.name == self.name:
                    class_node = node

        # get attributes and methods
        for node in class_node.body:
            self._add_attribute(node, is_class_level=True)
            if isinstance(node, FunctionDef):
                self._add_method(node)
                for subnode in walk(node):
                    self._add_attribute(subnode)

    def __hash__(self):
        """hash-method to use instances in other classes as attributes"""
        return_tuple = (
            self.name,
            frozenset(self.attributes.items()),
            frozenset(self.methods.items()),
            self.kind,
        )
        return hash(return_tuple)

    def _add_attribute(self, node: AST, is_class_level: bool = False) -> None:
        """helper method to update attribute-dictionary of instance"""

        def _get_name(arg: AST):
            """helper function to extract attribute name from syntax tree"""
            if isinstance(arg, Subscript):
                return _get_name(arg.value)
            elif isinstance(arg, Tuple):
                return [name for n in arg.elts for name in _get_name(n)]
            elif (
                isinstance(arg, Attribute)
                and isinstance(arg.value, Name)
                and arg.value.id == "self"
            ):
                return [arg.attr]
            elif isinstance(arg, Name) and is_class_level:
                return [arg.id]
            else:
                return []

        # sets names and annotations or _add_attribute() call ends (returns)
        if isinstance(node, Assign):
            for target in node.targets:
                names = _get_name(target)
                annotations = ["EMPTY"] * len(names)
        elif isinstance(node, AnnAssign):
            names, annotations = _get_name(node.target), [node.annotation]
        else:
            return

        # adds names and annotations to attribute-dictionary
        for name, annotation in zip(names, annotations):
            value = f"{name}: {self._format_type(annotation)}"
            if name in self.attributes:
                if self.attributes[name].count("EMPTY") >= value.count("EMPTY"):
                    self.attributes[name] = value
            else:
                self.attributes[name] = value

    def _add_method(self, node: FunctionDef) -> None:
        """helper method to update method-dictionary of instance"""

        # sets kind according decorator
        kind, decorators = "", ("staticmethod", "classmethod")
        for subnode in node.decorator_list:
            if isinstance(subnode, Name):
                kind = "{static}" if subnode.id in decorators else f"{{{subnode.id}}}"
            elif isinstance(subnode, Attribute):
                kind = "{property}"

        # sets argument names and annotations
        arguments = ", ".join(
            [
                f"{arg.arg}: {self._format_type(arg.annotation)}"
                for arg in node.args.args
                if arg.arg != "self"
            ]
        )

        # sets return annotations
        if isinstance(node.returns, Constant):
            returns = node.returns.value
        else:
            returns = self._format_type(node.returns)

        # adds attribute(property) or method to dictionaries depending on kind
        if kind == "{property}":
            value = f"{node.name}: {returns}"
            if not (
                node.name in self.attributes
                and any(t in value for t in ("None", "EMPTY"))
            ):
                self.attributes[node.name] = value
        else:
            self.methods[node.name] = f"{kind}{node.name}({arguments})" f" -> {returns}"

    def _format_type(self, node: AST) -> str:
        """helper method to extract annotations from syntax tree"""

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
    from test import MockClass

    obj = ClassChart(MockClass, "class")
    logger.debug(obj)
