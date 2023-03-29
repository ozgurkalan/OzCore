"""  
Test path module:
    * folder
    * tmp_path
"""

import os
from ozcore import core
from pathlib import Path, PosixPath, WindowsPath
import sys
import pytest
from typeguard import TypeCheckError

from ozcore.core.path.tmp_folders import TMP_Folder
from ozcore.core.path.folders import Folder
folder = Folder()

class TestFolder():
    TEST_FOLDER = None
    TMP = None
    TOML = None
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, monkeypatch):
        # setup paths
        current_dir = Path(__file__).parent.resolve()
        self.TEST_FOLDER = current_dir.joinpath("test_folder")
        self.TMP = self.TEST_FOLDER.joinpath("tmp")
        self.TOML = self.TEST_FOLDER.joinpath("sample.toml")
        
        # pytest to run cwd in tests folder
        def mock_cwd():
            return current_dir
        monkeypatch.setattr(os,"getcwd", mock_cwd)
        

        yield None
        # teardown
    
    def test_is_a_subfolder(self):
        # GIVEN test_folder
        # WHEN asked it is a subfolder of tests folder
        # THEN should assert True
        assert folder.is_a_subfolder(path_to_check=self.TEST_FOLDER, parent_folder=Path(".")) == True
        with pytest.raises(TypeCheckError):
            folder.is_a_subfolder(path_to_check=self.TEST_FOLDER, parent_folder=[Path(".")])
            # WHEN path param is other than str, POSIXPath or WindowsPath
            # THEN should raise TypeCheckError
            # this also checks the method check_path()
    
    def test_search_a_folder(self):
        # GIVEN test_folder with only one .toml file
        # WHEN searched in test_folder
        # THEN sample.toml should be there
        result = folder.search(self.TEST_FOLDER, "**/*.toml")
        expected = self.TOML
        
        assert expected in result
        
    def test_listdir_a_folder(self):
        # GIVEN test_folder with many files
        # WHEN listdir in test_folder
        # THEN files are in a list and each of them is a POSIXPATH or a WindowsPath
        result = folder.listdir(self.TEST_FOLDER)
        expected = list
        
        assert type(result) == list
        assert len(result) > 1
        assert type(result[0]) == PosixPath or type(result[0]) == WindowsPath
        

    @pytest.mark.skipif(
        sys.platform != "darwin",
        reason="available only in MAC OSX"
    )
    def test_special_folders(self):
        """  
        warning:
            Only OSX!
        """
        assert folder.iCloud.exists()
        assert folder.Downloads.exists()
        assert folder.Documents.exists()
        assert folder.OneDrive.exists()
        assert folder.gDrive.exists()


    def test_checking_a_path(self):
        # GIVEN tests folder has a test_folder and sample.toml is in that folder
        # WHEN check the folder or file
        # THEN should retrieve their PosixPaths
        
        assert folder.check_path(self.TEST_FOLDER) == self.TEST_FOLDER
        assert folder.check_path(str(self.TEST_FOLDER)) == self.TEST_FOLDER
        assert folder.check_path(self.TOML, is_file=True) == self.TOML
        assert folder.check_path(self.TOML, is_file=False, get_parent=True) == self.TEST_FOLDER
        with pytest.raises(Exception):
            folder.check_path("test_folder_not_exists", is_file=False, get_parent=False)
        with pytest.raises(TypeError):
            folder.check_path(self.TEST_FOLDER, is_file=True, get_parent=False)
            folder.check_path(self.TOML, is_file=False, get_parent=False)
    
    

class Test_Path_TMP_Folder():
        
    def test_tmp_folder_path_and_root(self, test_folder, tmp_folder):
        # GIVEN test_folder/tmp in tests folder
        # WHEN TMP_Folder initiated with test_folder as tmp root
        tmp = TMP_Folder(tmp_root=test_folder, tmp_folder_name="tmp")
        # THEN should retrieve root and path to tmp folder
        
        assert tmp.root == test_folder
        assert tmp.path == tmp_folder

    @pytest.mark.parametrize("glob, n, reverse", [
        ("**/*.csv",1,False),
        ("**/*.csv",1,True),
        ("**/*.csv",-1,False),
    ])
    def test_tmp_clean(self, test_folder, tmp_folder, clean_tmp, glob, n, reverse):
        # GIVEN three csv files in each tmp and tmp/data folders
        # clean
        clean_tmp
        # create csv files
        core.df.dummy.df1.to_csv(tmp_folder.joinpath("01_sample.csv"), index=False)
        core.df.dummy.df2.to_csv(tmp_folder.joinpath("02_sample.csv"), index=False)
        core.df.dummy.df3.to_csv(tmp_folder.joinpath("03_sample.csv"), index=False)
        
        # GIVEN there is tmp folder in test_folder
        tmp = TMP_Folder(tmp_root=test_folder, tmp_folder_name="tmp")
        
        # WHEN clean method called
        tmp.clean(glob=glob, n=n, reverse=reverse)
        
        # THEN method cleans with glob params, keeps n items
        files = list(tmp_folder.glob(glob))
        if n == 1:
            assert len(files) == 1
        elif n == -1:
            assert len(files) == 0
        
        # FINALLY clean tmp folder
        clean_tmp
        
    

