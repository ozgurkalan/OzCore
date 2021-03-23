import re
from pathlib import Path
import ozcore

def test_version():
    # GIVEN tests folder is in root folder of the package!
    
    # GIVEN no .git initiated
    # WHEN requested version
    # THEN version should be 0.0.0
    git_folder_exists = Path(__file__).parent.parent.joinpath(".git")
    # WHEN .git is in pck folder
    # GIVEN .git version tag is captured by Versioneer module
    # THEN version should have prefix "v", preceeding min one number

    if not git_folder_exists:
        assert ozcore.__version__ == "0.0.0"
    else:
        assert len(re.compile(r"^\d+\.").findall(ozcore.__version__))>0

