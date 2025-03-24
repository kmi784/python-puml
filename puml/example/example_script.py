from puml.src.extract_class import ExtractClassChart
from puml.example.example_classes import Source, Warning, SymLink, Core 

source = ""#ExtractClassChart(Source)
symlink = ""#ExtractClassChart(SymLink)
core = ExtractClassChart(Core)
warning = ""#ExtractClassChart(Warning)

print(source,
      symlink,
      core,
      warning, 
      sep="\n")

