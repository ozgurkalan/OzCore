import pytest
from pathlib import Path, PosixPath 

@pytest.fixture(scope="session", autouse=True)
def TEST_FOLDER() -> PosixPath:
    # mark test_folder
    folder = Path(__file__).parent.joinpath("test_folder")
    if not folder.exists():
        raise Exception("test_folder does no exist!")
    else:
        return folder
    
@pytest.fixture(scope="session", autouse=True)
def TMP_FOLDER(TEST_FOLDER) -> PosixPath:
    tmp =  TEST_FOLDER / "tmp" 
    if not tmp.exists():
        tmp.mkdir(parents=False, exist_ok=True)
    return tmp

@pytest.fixture(autouse=False, scope="session")
def CLEAN_TMP(TMP_FOLDER):
    """  
    clean the tmp folder
    """    
    # unlink all files in any folder
    files = TMP_FOLDER.glob("**/*")
    for file in files:
        if file.is_file():
            file.unlink()

    

    