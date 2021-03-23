""" office/docx tests """

import pytest
import os
from pathlib import Path
from shutil import copy

import ozcore
from ozcore import core
from ozcore.core import office


class TestDocx:
    
    TMP = Path(__file__).parent.joinpath("test_folder/tmp")
    S1 = TMP.joinpath("sample1.docx")
    S2 = TMP.joinpath("sample2.doc")
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, clean_tmp, monkeypatch):
        # clean tmp folder
        clean_tmp
        
        # cwd as tests folder
        def monkey():
            return Path(__file__).parent.resolve()
        monkeypatch.setattr(os, 'getcwd', monkey)
        
        # copy doc files from test folder to tmp folder
        copy(self.TMP.parent.joinpath(self.S1.name), self.S1)
        copy(self.TMP.parent.joinpath(self.S2.name), self.S2)
        
        yield None

        # clean tmp folder
        [e.unlink() for e in list(self.TMP.glob("*.doc*") )if e.is_file()]

    
    def test_core_is_calling_docx_class(self):
        # GIVEN core.docx is initiated in init
        # WHEN called
        # THEN should be an instance of Docx class
        assert isinstance(office.word, ozcore.core.office.docx.docx.Docx)
        
    @pytest.mark.parametrize(
        "folder, files, save_to_folder, expected",
        [
            (None, None, None, "error"), # at least a folder or files
            (TMP, S1, None, "error"), # either folder or files
            (None, [S1,S2], None, "error"), # no save_to_folder
            (None, [S1], TMP, "error"), # only one file
            ("test_folder/tmp", None, None, "error"), # relpath not allowed
            (TMP, None, None, 1),
            (None, [S1,S2], TMP, 1),
                        
        ]
        
    )
    def test_combine_docx_files(self, tmp_folder, folder, files, save_to_folder, expected):
        # GIVEN sample1.docx and sample2.doc in tmp folder
        # WHEN combine method called
        # THEN should be the output file created
        if expected == "error":
            with pytest.raises(Exception):
                core.office.word.combine_docx_files(folder=folder, files=files, save_to_folder=save_to_folder)
        else:
            core.office.word.combine_docx_files(folder=folder, files=files, save_to_folder=save_to_folder)
            
            assert len(list(tmp_folder.glob("ozcore_composed*.docx"))) == expected

    
    
