"""  
Useful paths and folders, search in folders and temporary folder helper methods.

warning:
    Folder paths are for **OSX** only. 
    
note:
    Special folders like Google Drive and OneDrive may not be available in your directories. Or your directory structure may be different. 

"""
from pathlib import Path, PosixPath
from typing import Union
from typeguard import check_argument_types


class Folder:
    """
    Essential folder paths as posixpath:
        - Downloads
        - gDrive
        - iCloud
        - OneDrive

    hint:
        Search for a folder with glob option

    Apps folder in this package:
        * folders in apps as posixpath enum
        * list of folders in apps folder

    Example, Search Downloads folder::

        from ozcore import core
        core.folder.search(path=core.folder.Downloads, file="the_file_searched.xl**")

    Example, is_a_subfolder::

        from ozcore import core
        core.folder.is_a_subfolder(path_to_check=Path("."), parent_folder=core.BASE_DIR)
    """

    @property
    def Downloads(self):
        """
        MacOS Downloads folder path

        returns:
            POSIXPATH to Downloads folder
        """
        path = Path().home().joinpath("Downloads")
        if path.exists():
            return path
        else:
            raise FileNotFoundError("Downloads folder not found!")

    @property
    def gDrive(self):
        """
        Google Drive folder path

        returns:
            POSIXPATH to gDrive
        """
        ls = [
            e
            for e in Path().home().iterdir()
            if e.is_dir() and e.stem == "Google Drive"
        ]

        if len(ls) == 1:
            ls = ls[0]

        path = Path(ls).resolve()
        if path.exists():
            return path
        else:
            raise FileNotFoundError("Google Drive folder not found!")

    @property
    def iCloud(self):
        """
        iCloud folder path

        returns:
            POSIXPATH to iCloud
        """
        ls = sorted(
            [
                e
                for e in Path().home().joinpath("Library/Mobile Documents").iterdir()
                if e.is_dir and e.stem == "com~apple~CloudDocs"
            ]
        )

        if len(ls) == 1:
            ls = ls[0]

        path = Path(ls).resolve()
        if path.exists():
            return path
        else:
            raise FileNotFoundError("iCloud folder not found!")

    @property
    def OneDrive(self):
        """
        OneDrive folder path

        returns:
            POSIXPATH to OneDrive
        """
        ls = [
            e
            for e in Path().home().iterdir()
            if e.is_dir() and e.stem[:8] == "OneDrive"
        ]

        if len(ls) == 1:
            ls = ls[0]

        path = Path(ls).resolve()
        if path.exists():
            return path
        else:
            raise FileNotFoundError("OneDrive folder not found!")

    def search(self, path, file):
        """
        search files in a given folder path

        parameters:
            path: a str or posixpath path
            file: str, file to search; searches as glob, e.g. **"**/.json"**

        returns:
            list, files in POSIXPATH type

        usage::

            from ozcore import core
            core.folder.search(core.folder.gDrive.joinpath("folder name"), "*.xlsx")
        """

        path = Path(path).resolve()

        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"{path} is not available!")

        ls = path.rglob(file)
        result = sorted([e for e in ls], reverse=False)
        return result

    def is_a_subfolder(self, path_to_check: PosixPath, parent_folder: PosixPath):
        """
        check if a given path is in parent folder

        parameters:
            path_to_check: posixpath, a path to match with base folder
            parent_folder: posixpath, the base aka parent folder

        return:
            boolean
        """
        path = path_to_check.resolve()
        base = parent_folder.resolve()

        if path == base:
            return True

        if base.stem in path.parts:
            return True
        else:
            return False

    def check_path(
        self, path: Union[str, PosixPath], is_file: bool = False
    ) -> PosixPath:
        """
        Checks the given ``path`` param, converts it to an absolute path

        warning:
            All relative paths are ignored and Exception will be raised.

        note:
            This method checks the type of the arguments and raise Exception if not satisfied.

        parameters:
            path: str|PosixPath, can be Pathlike path or a relative path
            is_file: bool, default False, False: a directory, True: a file

        returns:
            Absolute PosixPath; checks if path exists.
        """
        # check type of the given path parameter
        check_argument_types()

        if isinstance(path, str):
            path = Path(path)

        if not path.is_absolute():
            raise Exception("Only absoulte paths are allowed.")

        elif not path.exists():
            raise Exception(f"{str(path)} does not exists")

        elif is_file == False and not path.is_dir():
            raise TypeError(f"{str(path)} is not a directory")

        elif is_file == True and not path.is_file():
            raise TypeError(f"{str(path)} is not a file")

        return path
