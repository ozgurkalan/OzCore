"""  
Test path module: folders
"""

import os
import sys
from pathlib import Path, PosixPath
import pytest
from ozcore import core


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
        
        # end
    
    def test_is_a_subfolder(self):
        # GIVEN test_folder
        # WHEN asked it is a subfolder of tests folder
        # THEN should assert True
        assert folder.is_a_subfolder(path_to_check=self.TEST_FOLDER, parent_folder=Path(".")) == True
    
    def test_search_a_folder(self):
        # GIVEN test_folder with only one .toml file
        # WHEN searched in test_folder
        # THEN sample.toml should be there
        result = folder.search(self.TEST_FOLDER, "**/*.toml")
        expected = self.TOML
        
        assert expected in result

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
        assert folder.OneDrive.exists()
        assert folder.gDrive.exists()


    def test_checking_a_path(self):
        # GIVEN tests folder has a test_folder and sample.toml is in that folder
        # WHEN check the folder or file
        # THEN should retrieve their PosixPaths
        
        assert core.folder.check_path(self.TEST_FOLDER) == self.TEST_FOLDER
        assert core.folder.check_path(str(self.TEST_FOLDER)) == self.TEST_FOLDER
        assert core.folder.check_path(self.TOML, is_file=True) == self.TOML
        with pytest.raises(Exception):
            core.folder.check_path("test_folder")
    
    