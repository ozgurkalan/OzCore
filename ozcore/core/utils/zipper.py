"""Zipper functions 


"""

import requests
import zipfile
from pathlib import Path, PosixPath
from typeguard import typechecked
import typer
from tqdm.auto import tqdm

@typechecked
def unzip(url:str, dest:PosixPath, chunk_size:int=1024*1024, remove_zip: bool=False):
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
    
    with zipfile.ZipFile(dest.joinpath(filename)) as zippo:
        for member in tqdm(zippo.infolist(), desc="Extracting zip file..."):
            zippo.extract(member, dest)
            
    if remove_zip:
        dest.joinpath(filename).unlink()
        typer.secho(f"{filename} is removed.", bold=True, fg="red")
    else:
        typer.secho(f"{filename} is unzipped in {dest}.", bold=True, fg="green")
    