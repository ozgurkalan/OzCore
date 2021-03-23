""" Microsoft docx files helper class 


"""
import os
from pathlib import PosixPath
from ozcore import core
from typing import Union, List
from typeguard import check_argument_types

from docx import Document
from docxcompose.composer import Composer


class Docx:
    """  
    Microsoft docx files helper class
    
    usage::
    
        from ozcore.core import office
        office.word.combine_docx_files(folder="some-folder")
    
    """
    
    def combine_docx_files(self, 
                                       folder:Union[str, PosixPath] = None,
                                       files:Union[List[str], List[PosixPath]] = None,
                                       save_to_folder:Union[str, PosixPath] = None
                                       ):
        """  
        Combine multiple documents (.docx, .doc, .docxm)
        
        parameters:
            folder: str|PosixPath, default None
            files: list(str)|list(PosixPath), default None
            save_to_folder: str|PosixPath, default None
        
        warning:
            You can either define  ``folder``or ``files``. If ``files`` given (more than one), ``save_to_folder`` must be defined.
            
        returns:
            * combines docx files and saves in ``save_to_folder``
            * if ``folder`` is given but no ``save_to_folder`` , output file saved in ``folder``
        """
        
        # allowed extentions
        exts = [".docx", ".doc", ".docxm"]
        
        # check argument types
        check_argument_types()
        
        if folder is None and files is None:
            raise Exception("Please provide with either a folder path or a list of files")
        
        elif folder is not None and files is not None:
            raise Exception("Choose a folder or a list of files. Both options are not allowed")
        
        # check folders and files
        folder = core.folder.check_path(folder) if folder else None
        save_to_folder = core.folder.check_path(save_to_folder) if save_to_folder else None
        files = [core.folder.check_path(file, is_file=True) for file in files] if files else None
        
        if folder:
            filo = list(folder.glob("*.doc*"))
        elif files:
            filo = files
            
        if len(filo)<2:
            raise Exception("More than 1 docx file needed!")
        
        result = Document(filo[0])
        result.add_page_break()
        composer = Composer(result)
    
        for i in range(1, len(filo)):
            doc = Document(filo[i])

            if i != len(filo) - 1:
                doc.add_page_break()

            composer.append(doc)
            
        if files is not None and save_to_folder is None:
            raise Exception("Please provide a folder to save the output file!")
        
        if save_to_folder:
            new_file = save_to_folder.joinpath(f"ozcore_composed_{core.now_prefix(separator='_')}.docx")
        else:
            new_file = folder.joinpath(f"ozcore_composed_{core.now_prefix(separator='_')}.docx")
            
        composer.save(new_file)

        