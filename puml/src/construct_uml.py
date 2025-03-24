from puml.src import ExtractClassChart, logger


class ConstructorUmlChart:
    pass


if __name__ == "__main__":
    from puml.test import Source, Warning, SymLink, Core

    source = ExtractClassChart(Source)
    symlink = ExtractClassChart(SymLink)
    core = ExtractClassChart(Core)
    warning = ExtractClassChart(Warning)

    logger.debug(source)
    logger.debug(symlink)
    logger.debug(core)
    logger.debug(warning)
