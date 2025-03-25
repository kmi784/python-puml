from puml.src.extract_class import ClassChart


class UmlChart:
    def __init__(self):
        self.classes: list = []
        self.relations: dict[tuple, str] = {}

    def add_class(self, cls):
        value = ClassChart(cls)
        self.classes.append(value)
        return value

    def add_relation(self, arg1, arg2, kind: str = "---"):
        self.relations[(arg1, arg2)] = kind

    def __repr__(self):
        def _handel_members(members, indent=1):
            value = ""
            if len(members) != 0:
                for member in members.values():
                    if member[0] != "_":
                        value += f"\n{"\t"*indent}+{member}"
            return value

        output = ""
        for node in self.classes:
            output += (
                f"\n{node.kind} {node.name} {{"
                f"{_handel_members(node.attributes)}"
                f"{_handel_members(node.methods)}"
                f"\n}}"
            )

        for pair, rel in self.relations.items():
            output += f"\n{pair[0].name} {rel} {pair[1].name}"
        return output


if __name__ == "__main__":
    from puml.test import Source, Warning, SymLink, Core

    uml = UmlChart()

    source = uml.add_class(Source)
    warning = uml.add_class(Warning)
    symlink = uml.add_class(SymLink)
    core = uml.add_class(Core)

    uml.add_relation(symlink, warning, kind="--|>")
    uml.add_relation(symlink, core, kind="o--")
    uml.add_relation(source, core, kind="o--")

    print(uml)
