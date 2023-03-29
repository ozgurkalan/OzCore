""" 
Common paths and folders, search in folders helper methods.

warning:
    Folder paths are returned as POSIXPATH for **OSX** and WINDOWSPATH for win32 systems. 
    
note:
    Special folders like Google Drive and OneDrive may not be available in your directories. Or your directory structure may be different. 

"""
from pathlib import Path, PosixPath, WindowsPath
from typing import Union
from typeguard import typechecked


class Folder:
    """
    Essential folder paths as posixpath:
        - Downloads
        - Documents
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
        core.path.search(path=core.path.Downloads, file="the_file_searched.xl**")

    Example, List directory::

        from ozcore import core
        core.path.listdir(path=core.path.Downloads)

    Example, is_a_subfolder::

        from ozcore import core
        core.path.is_a_subfolder(path_to_check=Path("."), parent_folder=core.BASE_DIR)

    Example, check_path::

        from ozcore import core
        core.path.check_path(path=core.path.Downloads.joinpath('test.xlsx'), file=True)
    """

    @property
    def Downloads(self) -> Union[PosixPath, WindowsPath]:
        """Downloads folder path

        returns:
            POSIXPATH or WindowsPath to Downloads folder
        """
        path = Path().home().joinpath("Downloads")
        if path.exists():
            return path
        else:
            raise FileNotFoundError("Downloads folder not found!")

    @property
    def Documents(self) -> Union[PosixPath, WindowsPath]:
        """Documents folder path

        returns:
            POSIXPATH or WindowsPath to Documents folder
        """
        path = Path().home().joinpath("Documents")
        if path.exists():
            return path
        else:
            raise FileNotFoundError("Documents folder not found!")

    @property
    def gDrive(self) -> Union[PosixPath, WindowsPath]:
        """Google Drive folder path

        returns:
            POSIXPATH or WindowsPath to gDrive
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
    def iCloud(self) -> Union[PosixPath, WindowsPath]:
        """iCloud folder path

        returns:
            POSIXPATH or WindowsPath to iCloud
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
    def OneDrive(self) -> Union[PosixPath, WindowsPath]:
        """OneDrive folder path

        returns:
            POSIXPATH or WindowsPath to OneDrive
        """
        ls = [
            e
            for e in Path().home().iterdir()
            if e.is_dir() and e.stem[:8] == "OneDrive"
        ]

        if len(ls) == 1:
            ls = ls[0]
        elif len(ls)>1:
            ls = ls[1] 
            # if there is more than one OneDrive probably the second one is the Business version you're looking for

        path = Path(ls).resolve()
        if path.exists():
            return path
        else:
            raise FileNotFoundError("OneDrive folder not found!")

    def listdir(
        self, path: Union[str, PosixPath, WindowsPath]
    ) -> list[Union[None, PosixPath, WindowsPath]]:
        """ls files in a folder

        parameters:
            path: a str or posixpath path

        returns:
            list, files in POSIXPATH type
        """
        path = self.check_path(path, is_file=False, get_parent=True).resolve()

        return [e for e in path.iterdir()]

    @typechecked
    def search(
        self, path: Union[str, PosixPath, WindowsPath], file: str
    ) -> list[Union[None, PosixPath, WindowsPath]]:
        """Search files in a given folder path

        parameters:
            path: a str or posixpath or WindowsPath path
            file: str, file to search; searches as glob, e.g. **"**/.json"**

        returns:
            list, files in POSIXPATH or WindowsPath type

        usage::

            from ozcore import core
            core.path.search(core.path.gDrive.joinpath("folder name"), "*.xlsx")
        """

        path = self.check_path(path, is_file=False, get_parent=True).resolve()
        ls = path.rglob(file)
        result = sorted([e for e in ls], reverse=False)

        return result

    @typechecked
    def is_a_subfolder(
        self,
        path_to_check: Union[str, PosixPath, WindowsPath],
        parent_folder: Union[str, PosixPath, WindowsPath],
    ) -> bool:
        """Check if a given path is in parent folder

        parameters:
            path_to_check: posixpath, a path to match with base folder
            parent_folder: posixpath, the base aka parent folder

        return:
            boolean
        """

        path = self.check_path(path_to_check, is_file=False, get_parent=True).resolve()
        base = self.check_path(parent_folder, is_file=False, get_parent=True).resolve()

        if path == base:
            return True

        if base.stem in path.parts:
            return True
        else:
            return False
    
    @typechecked
    def check_path(
        self,
        path: Union[str, PosixPath, WindowsPath],
        is_file: bool = False,
        get_parent: bool = False,
    ) -> Union[PosixPath, WindowsPath]:
        """Checks the given ``path`` parameter, converts it to an absolute path.

        warning:
            All relative paths are ignored and Exception will be raised.

        note:
            This method checks the type of the arguments and raise Exception if not satisfied.

        parameters:
            path: str|PosixPath|WindowsPath, can be Pathlike path or a relative path
            is_file: bool, default False, False: a directory, True: a file
            get_parent: bool, default False, True: get file's parent (is_file should be False)

        returns:
            Absolute PosixPath or WindowsPath;
            Raise error if directory or file not exists.
        """

        if isinstance(path, str):
            path = Path(path).absolute()

        if not path.exists():
            raise Exception(f"{str(path)} does not exists")

        if is_file == False and not path.is_dir():
            if get_parent == True:
                path = path.parent
            else:
                raise TypeError(f"{str(path)} is not a directory")

        if is_file == True and not path.is_file():
            raise TypeError(f"{str(path)} is not a file")

        return path
