from ast import literal_eval as parse
from os import readlink, symlink, remove
from os.path import isfile, islink, abspath, basename, expanduser

from puml.src import logger

class Source:
    """
    Attribute:
        - dict of <absolut/path/to/target> mapping to <shellcommand>
    Method:
        - source/compile passed <absolut/path/to/target> via system_interface()
    """
    def __init__(self, kwargs : dict):
        pass



class Warning(Exception):
    
    def __init__(self, key:str, src_file:str="", sym_link:str=""):
        self.message = "" 
        self.ignore_file = True
    
        match key:
            case "FILE":
                if islink(src_file):
                    raise FileExistsError(
                        f"Link cannot be created, because <{src_file}> is not a regular file!"
                    )
                else:
                    self.message += f"File <{src_file}> does not exist."
                        
            case "LINK":
                if isfile(sym_link):
                    raise FileExistsError(
                        f"Link cannot be created, because <{sym_link}> already exsits "
                        f"and is a regular file"
                    )
                else:
                    self.message += f"Symlink <{sym_link}> does not exists, it will be created!"
                    symlink(src_file, sym_link)
                    self.ignore_file = False
                
            case "LINKING":
                logger.warning(f"{self.message}Symlink <{sym_link}> does not point to file <{src_file}>, symlink will be overwritten.")
                permission = input(f"->To continue hit (y/Y):").lower() == "y"

                if permission:
                    remove(sym_link)
                    symlink(src_file, sym_link)
                    self.message += "New symlink is set up."
                    self.ignore_file = False

                else:
                    self.message += "Old symlink remains!"

        super().__init__(self.message)
    

class SymLink:
    """
    Attribute:
        - dict of <path/to/target> mapping to <absolute/path/to/symlink>
    Method:
        - initially creates symlinks of all targets in attribute 
        - create symlink of passed <path/to/target> 
    """
    def __init__(self, kwargs : dict) -> None:
        self.targets = {}
        for src_path, value in kwargs.items():
            sym_path = f"{value}/{basename(src_path)}" if value[-1] == "/" else value
            file = abspath(src_path)
            link = expanduser(sym_path) if "~" in sym_path else abspath(sym_path)

            try:
                if not isfile(file) or islink(file):
                    logger.debug("raising FILE Warning")
                    raise Warning("FILE", src_file=file, sym_link=link)
                
                if not islink(link):
                    logger.debug("raising LINK Warning")
                    raise Warning("LINK", src_file=file, sym_link=link)
                
                if abspath(readlink(link)).lower() != file.lower():
                    logger.debug("raising LINKING Warning")
                    raise Warning("LINKING", src_file=file, sym_link=link)
                                
            except Warning as warn:
                logger.warning(warn.message)
                if warn.ignore_file:
                    continue
                                   
            self.targets[src_path] = link


    def __contains__(self, key):
        return key in self.targets
    

    def create(self, key):
        file, link = abspath(key), self.targets[key]
        if islink(link):
            remove(link)
        symlink(file, link)

class Core:
    """
    Attributes:
        - dict of aliases : <alias> convert to <absolut/path/to/target>
        - SymLink instance
        - Source instance

    Handles:
        - pickle file: store/load SymLink and Source instances
        - config file: passes the necessary arguments to the constructors
            - containg: "<absolut/path/to/target>" : {
                            "alias" : "<name, default = file name, optional while no dublicated alias exists>", 
                            "symlink" : "<path/to/symlink, optional>",
                            "requirement" : "<path/to/demanding/file, optional>",
                            "executable" : "<shellcommand, non-optional>"
                        }

    Methods:
        - save instance
        - load instance static method
        - delete instance
        - list targets 
        - excess Symlink method: creates symlink of passed target
        - excess Source method: source passed target
    """
    
    def __init__(self, config_path=".pyurc"):
        if basename(config_path) != ".pyurc":
            config_path += ".pyurc" if config_path[-1] == "/" else "/.pyurc"
        config_path = abspath(config_path)

        try:
            isfile(config_path)
            with open(f"{config_path}", "r") as file:
                targets = parse(file.read())

            self.aliases = {}
            sym_args, src_args = {}, {}
            for key, value in targets.items():

                alias = basename(key) if not "alias" in value  else value["alias"]
                if not alias in self.aliases:
                    self.aliases[alias] = key
                else:
                    logger.warning(f"Duplicated alias occurred.")
                    new_alias = ""
                    while new_alias in self.aliases or new_alias == "":
                        new_alias = input(f"->Enter alias for <{key}>:") # new alias in <.pyurc>
                    self.aliases[new_alias] = key


                if "sourcing" in value:
                    src_args[key] = value["sourcing"]
                    # logger.debug(value["sourcing"].format(target=key))

                if "linking" in value:
                    sym_args[key] = value["linking"]
                
            self._symlink = SymLink(sym_args)
            self._source = Source(src_args)

        except FileNotFoundError:
            logger.warning(f"<{config_path}> does not exists. It will be created!")
            permission = input(f"->To continue hit (y/Y):").lower() == "y"
            if permission:
                print("Template file will be created!")
            else:
                print("Nothing happened")


    def create_symlink(self, arg : str):
        try:
            if self.aliases[arg] in self._symlink:
                self._symlink.create(self.aliases[arg])
            else:
                logger.warning(f"<{arg}> is not a symbolic link target.")

        except KeyError:
            logger.warning(f"<{arg}> is not a target in <.pyurc>")
        
    def source_file(self, arg : str):
        pass