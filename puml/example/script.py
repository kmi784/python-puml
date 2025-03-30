from puml import UmlChart
from puml.example.classes import Core, Source, SymLink, Warning

uml = UmlChart()

core = uml.add_class(Core)
source = uml.add_class(Source)
symlink = uml.add_class(SymLink)
warning = uml.add_class(Warning)

uml.add_relation(core, source, "--o")
uml.add_relation(core, symlink, "--o")
uml.add_relation(symlink, warning, "--|>")

print(uml)