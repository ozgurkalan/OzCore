"""Zipper functions 


"""

from pathlib import Path, PosixPath, WindowsPath
from typing import Union
from zipfile import ZIP_DEFLATED, ZipFile

import requests
import typer
from tqdm.auto import tqdm
from typeguard import typechecked

from ozcore import core


@typechecked
def unzip_url(url:str, dest:PosixPath, chunk_size:int=1024*1024, remove_zip: bool=False):
    """ 
    Downloads and unzips a zip file
    
    parameters:
        url: str, uri to zip file
        dest: PosixPath, destination folder
        chunk_size: int, default 1 MB
        remove_zip: bool, default False, unlinks zip file after unzip operation
        
    returns:
        tqdm progress bar and typer echo messages
    """
    stream = requests.get(url, stream=True, verify=False, allow_redirects=True)
    filename = stream.url.split(sep="/")[-1]
    length = int(stream.headers.get("content-length", -1))
    
    if length < 1:
        raise Exception(f"content length is less than 1 bytes")
    
    if not dest.exists():
        raise Exception(f"destination folder does not exist: {dest}")
    
    if dest.is_file():
        dest = dest.parent
        
    dest = dest.resolve()

    typer.echo("Downloading zip file...")

    with tqdm.wrapattr(
    open(dest.joinpath(filename), "wb"), "write",
    unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
    desc=filename, total=length) as f:
        for chunk in stream.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                f.flush()
                
    typer.echo("Extracting zip file...")
    
    with ZipFile(dest.joinpath(filename)) as zippo:
        for member in tqdm(zippo.infolist(), desc="Extracting zip file..."):
            zippo.extract(member, dest)
            
    if remove_zip:
        dest.joinpath(filename).unlink()
        typer.secho(f"{filename} is removed.", bold=True, fg="red")
    else:
        typer.secho(f"{filename} is unzipped in {dest}.", bold=True, fg="green")
        
        

@typechecked
def backup(src: Union[PosixPath,WindowsPath, list[Union[PosixPath, WindowsPath]]],
                      dest: Union[PosixPath, WindowsPath]=None,
                      suffix: Union[str, None] = None,
                      verbose: bool = True
                      ):
    """Create a backup zip from given files
    
    parameters:
        src: a PosixPath or list of PosixPaths of files, which will be zipped
        dest: a PosixPath, default is None, destination path, which the zip will saved. When omitted, current path will be used
        suffix: str, default is None, suffix of zip file's stem, when omitted, if a single file than its extension will be used; otherwise, '_files' will be used
        verbose: bool, default is True, echo output when verbose
    
    returns:
        path to a zip file in the destination folder
        
    warning:
        * if no destination given then current directory will be used
        * if a file path is given as destination, then its parent folder will be used
    """
    if isinstance(src, PosixPath) or isinstance(src, WindowsPath):
        src = [src]
        
    # check if src files exist
    [core.folder.check_path(path=e, is_file=True, get_parent=False) for e in src]

    if dest is None:
        # if no dest is specified then current directory
        dest = core.folder.check_path(Path('.'), is_file=False, get_parent=False)
    
    # check destination
    dest = core.folder.check_path(dest, is_file=False, get_parent=False)
    dest = dest.resolve()
    
    if suffix is None:
        if len(src) > 1:
            suffix = "files"
        else:
            suffix = src[0].stem
            
    filename = dest.joinpath("Backup_" + core.utils.now_prefix("_") + "_" + suffix + ".zip")
    
    with ZipFile(
        filename,
        "w",
        ZIP_DEFLATED,
        compresslevel=9,
    ) as thezip:
        for file in src:
            thezip.write(file, arcname=file.name)
            
    if verbose:
        typer.secho(f"{filename.name} is zipped in \n {dest}.", bold=True, fg="green")
        
    return filename