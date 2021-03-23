import pytest
from pathlib import Path, PosixPath 

@pytest.fixture(scope="session", autouse=True)
def test_folder() -> PosixPath:
    # mark test_folder
    folder = Path(__file__).parent.joinpath("test_folder")
    if not folder.exists():
        raise Exception("test_folder does no exist!")
    else:
        return folder
    
@pytest.fixture(scope="session", autouse=True)
def tmp_folder(test_folder) -> PosixPath:
    tmp =  test_folder / "tmp" 
    if not tmp.exists():
        tmp.mkdir(parents=False, exist_ok=True)
    return tmp

@pytest.fixture(autouse=False)
def clean_tmp(tmp_folder):
    """  
    clean the tmp folder
    """
    # unlink all files in any folder
    files = tmp_folder.glob("**/*")
    for file in files:
        if file.is_file():
            file.unlink()

    

    