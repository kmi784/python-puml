from puml.src import ExtractClassChart

class ConstructorUmlChart:
    pass

if __name__ == "__main__":
    from puml.test import Source, Warning, SymLink, Core 

    source = ExtractClassChart(Source)
    symlink = ExtractClassChart(SymLink)
    core = ExtractClassChart(Core)
    warning = ExtractClassChart(Warning)

    print(source,
        symlink,
        core,
        warning, 
        sep="\n")
