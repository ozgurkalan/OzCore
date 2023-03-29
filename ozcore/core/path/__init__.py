
# path module::TMP_Folder
from .tmp_folders import TMP_Folder as __TMP_Folder
tmp_folder = __TMP_Folder()

# path module::Folder
from .folders import Folder as __Folder
folder = __Folder()

__all__ = ["folder","tmp_folder"]