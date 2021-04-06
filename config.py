""" configuration for the package """

import toml
from pathlib import Path
import typer

here = Path(__file__).parent.resolve() 
docs = here / "docs"
requirements = docs / "requirements.txt"
pyproject = here / "pyproject.toml"

conf = typer.Typer()

@conf.command("hello")
def hello():
    """ at least two commands required. This function is just dummy. """
    typer.echo("hello world")

@conf.command("create", help="create requirements.txt in docs folder")
def create_requirements():
    '''
    Sphinx is grouchy about requirements.txt
    So, before pushing to Github, we create a fresh requirements.txt from pyproject.toml
    '''
    t = toml.load(pyproject).get("tool", {}).get("poetry", {})
    
    with open(requirements, "w") as f:
        # get dependencies without versions
        dep = t.get("dependencies", {}).keys()
        # skip python
        dep = list(dep)[1:]
        
        print("# These dependencies are derived from pyproject.toml", 
              "# The file is prepared for Sphinx, which is grouchy about using it :(",
              "",
              "# Dependencies", sep="\n",
              file=f)
        
        for key in dep:
            print(key, file=f)
            
        devdep = list(t.get("dev-dependencies", {}).keys())
        print("# Dev-Dependencies", file=f)
        
        for key in devdep:
            print(key, file=f)
            
    typer.secho("created requirements.txt in docs folder", bold=True, fg="red")
        
        
        
if __name__ == "__main__":
    conf()