"""
This module contains the "UmlChart"-class (user interface) to handle class-chart
extraction and puml-chart-code generation.
"""

from pathlib import Path

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
    >>> uml = UmlChart()
    >>> a = uml.add_class(MyClassA)
    >>> b = uml.add_class(MyClassB)
    >>> uml.add_relation(a, b, "--o")
    >>> print(uml)
    """

    def __init__(self):
        self.classes: dict = {}
        self.relations: dict[tuple, str] = {}

    def __repr__(self):
        """representation-method to print puml-syntax"""

        def _print_structure(arg: dict, indent: int = 0):
            rtrn = ""
            for key, value in arg.items():
                if isinstance(key, str) and isinstance(value, dict):
                    rtrn += (
                        "\t" * indent
                        + f'package "{key}"{{\n{_print_structure(value, indent + 1)}'
                        + "\t" * indent
                        + "}\n"
                    )
                elif isinstance(key, ClassChart):
                    rtrn += (
                        "\n".join(
                            ["\t" * indent + f"{line}" for line in str(key).split("\n")]
                        )
                        + f"\n"
                    )
            return rtrn

        output = _print_structure(self.classes)

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
        self.classes[value] = None
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

    def set_structure(self, tree: dict) -> None:
        """
        Adds a package with specified classes.

        Parameters
        ----------
        tree: dict[str or ClassChart, dict or None]
            members of the package
        """

        def _check_for_members(arg: dict):
            for key, value in arg.items():
                if isinstance(value, dict):
                    _check_for_members(value)
                elif isinstance(key, ClassChart):
                    self.classes.pop(key)

        _check_for_members(tree)
        self.classes = self.classes | tree

    def draw(self) -> None:
        """
        Generates a svg image (with name of script) of the uml-chart.
        """
        out_file = Path(__file__).with_suffix(".svg")
        svg_bytes, _, _, _ = render(str(self), engine="plantuml", format="svg")

        with open(out_file, "wb") as file:
            file.write(svg_bytes)


if __name__ == "__main__":
    from puml.example import Source, Warning, SymLink, Core

    uml = UmlChart()

    source = uml.add_class(Source)
    warning = uml.add_class(Warning)
    symlink = uml.add_class(SymLink)
    core = uml.add_class(Core)

    uml.set_structure(
        {
            core: None,
            "sub": {
                source: None,
                "sym": {
                    warning: None,
                    symlink: None,
                },
            },
        }
    )

    uml.add_relation(symlink, warning, kind="--|>")
    uml.add_relation(symlink, core, kind="o--")
    uml.add_relation(source, core, kind="o--")

    uml.draw()

    # logger.debug(uml)
