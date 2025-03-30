"""
This module contains the "UmlChart"-class (user interface) to handle class-chart
extraction and puml-chart-code generation.
"""

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
    >>> uml = UmlChart()
    >>> a = uml.add_class(MyClassA)
    >>> b = uml.add_class(MyClassB)
    >>> uml.add_relation(a, b, "--o")
    >>> print(uml)
    """

    def __init__(self):
        self.classes: list = []
        self.relations: dict[tuple, str] = {}

    def __repr__(self):
        """representation-method to print puml-syntax"""

        output = "\n"
        for node in self.classes:
            output += str(node) + "\n"

        for pair, rel in self.relations.items():
            output += f"\n{pair[0].name} {rel} {pair[1].name}"
        return output

    def add_class(self, cls: type) -> ClassChart:
        """
        Adds a class to the uml-chart.

        Parameters
        ----------
        cls : type
            type of target class

        Returns
        -------
        ClassChart
            target class as ClassChart instance
        """
        value = ClassChart(cls)
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

    def add_package(name: str, *args) -> dict:
        """
        Adds a package with specified classes.

        Parameters
        ----------
        name : str
        *args: ClassChart or dict[str, dict]
            members of the package

        Returns
        -------
        dict
            package as dictionary with values of type ClassChart or packages
        """
        pass

    def draw(self, file: str) -> None:
        """
        Generates a svg image of the uml-chart.

        Parameters
        ----------
        file: str
            target location and name of the image
        """
        pass


if __name__ == "__main__":
    from puml.example import Source, Warning, SymLink, Core

    uml = UmlChart()

    source = uml.add_class(Source)
    warning = uml.add_class(Warning)
    symlink = uml.add_class(SymLink)
    core = uml.add_class(Core)

    uml.add_relation(symlink, warning, kind="--|>")
    uml.add_relation(symlink, core, kind="o--")
    uml.add_relation(source, core, kind="o--")

    logger.debug(uml)
