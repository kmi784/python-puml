"""
This module contains the "UmlChart"-class (user interface) to handle class-chart
extraction and puml-chart-code generation.
"""

from plantweb.render import render

from puml.src import logger, ClassChart


class UmlChart:
    """
    User interface to specify the objects to be drawn.

    Parameters
    ----------
    None

    Attributes
    ----------
    classes: list
        collection of ClassChart instances
    relations: dict
        the key is tuple of two ClassChart instances and the value is puml-expression
        for the relation as string

    Examples
    --------
    >>> from puml import UmlChart
    >>> uml = UmlChart(root_module="MyPackage")
    >>> a = uml.add_class(MyClassA)
    >>> b = uml.add_class(MyClassB, "interface")
    >>> uml.add_relation(a, b, "--o")
    >>> uml.draw("chart.svg") # for rendered svg-image
    >>> print(uml) # for puml syntax as string
    """

    def __init__(self, root_module: str = None):
        self.classes: list = []
        self.relations: dict[tuple, str] = {}
        self.root = root_module

    def __repr__(self):
        """representation-method to print puml-syntax"""
        # packaging
        self._set_root()

        output = "\n"
        # classes
        for cls in self.classes:
            output += f"{cls}\n"

        # relations
        for pair, rel in self.relations.items():
            output += f"\n{pair[0].name} {rel} {pair[1].name}"

        return output

    def add_class(self, cls: type, kind: str = "class") -> ClassChart:
        """
        Adds a class to the uml-chart.

        Parameters
        ----------
        cls : type
            target class type
        kind : "abstract", "class" or "interface"

        Returns
        -------
        ClassChart
            target class as ClassChart instance
        """
        value = ClassChart(cls, kind)
        self.classes.append(value)
        return value

    def add_relation(
        self, arg1: ClassChart, arg2: ClassChart, kind: str = "--|>"
    ) -> None:
        """
        Adds a relation of two classes to the uml-chart.

        Parameters
        ----------
        arg1 : ClassChart
        arg2 : ClassChart
        kind : str
            relation from arg1 to arg2 (default = "--|>")
        """
        self.relations[(arg1, arg2)] = kind

    def draw(self, file: str = "chart.svg") -> None:
        """
        Generates a svg image (with name of script) of the uml-chart.

        Parameters
        ----------
        file : str or path-object
            target directory with name and extension
        """
        svg_bytes, _, _, _ = render(str(self), engine="plantuml", format="svg")
        with open(file, "wb") as f:
            f.write(svg_bytes)

    def _set_root(self):
        """helper method to packing uml chart according to specified root package"""

        def _set_new_parents(old_name: str) -> str:
            """helper function to get new module parents"""
            if self.root:
                parents = old_name.split(".")
                if parents.count(self.root) == 1:
                    return ".".join(parents[parents.index(self.root) + 1 :])
                return ""
            return ""

        for cls in self.classes:
            cls.module = _set_new_parents(cls.module)


if __name__ == "__main__":
    from puml.example import Source, Warning, SymLink, Core

    uml = UmlChart(root_module="puml")

    source = uml.add_class(Source)
    warning = uml.add_class(Warning)
    symlink = uml.add_class(SymLink)
    core = uml.add_class(Core, kind="interface")

    uml.add_relation(symlink, warning, kind="..>")
    uml.add_relation(symlink, core, kind="o--")
    uml.add_relation(source, core, kind="o--")

    uml.draw()
    print(uml)
