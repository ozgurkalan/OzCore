""" Helper class for Temporary Folders and Files """

from pathlib import Path

class TMP_Folder:
    """  
    Helper class for Temporary Folders and Files
    
    methods:
    
    - tmp folder root
    - tmp folder path
    - cleans tmp folder files with given conditions
        
    hint:
        Useful for cleaning ``tmp`` folders espaecially when fetching csv files into ``tmp`` folders
        
    usage::
    
        from ozcore.core.path import TMP_Folder
        tmp = TMP_folder(tmp_root="root/folder/path/", tmp_folder_name="tmp")
        
        tmp.root
        # ../../root_folder
        
        tmp.path
        # ../../root folder/tmp_folder_path
        
        tmp.clean(glob="**/*.json", n=3)
        # ... cleans all json files up to latest 3 in the tmp
        
        tmp.clean(glob="*", n=-1)
        # ... cleans all files in the tmp
        
    """

    def __init__(self, tmp_root=".", tmp_folder_name="tmp"):
        self.tmp_root = tmp_root  # the root folder of the tmp folder as posixpath or str, defaults to ".", current folder
        self.tmp_folder_name = tmp_folder_name # defaults to 'tmp'

    @property
    def root(self):
        """  
        root folder path of the temporary folder as posixpath
        
        returns:
            posixpath path to root of the tmp folder
        """
        path = self.tmp_root
        if isinstance(path, str):
            path = Path(self.tmp_root).resolve()
            
        if not path.exists():
            raise FileNotFoundError("tmp folder root does not exist!")
        elif path.is_file():
            path = path.parent
         
        return path

    @property
    def path(self):
        """ 
        path of the tmp folder as posixpath
        
        returns: 
            posixpath to tmp folder
        """
        tmp = self.root.joinpath(self.tmp_folder_name)
        if not tmp.exists():
            raise FileNotFoundError("tmp folder root does not exist!")
        return tmp
    

    def clean(self, glob, n=5, reverse=False):
        """
        deletes old files in the tmp folder
        keeps last n files (sorted asc or desc)
        
        parameters:
            n: number of files to `keep`!, default:5; -1 for all files
            glob: search tmp folder to match files,
            reverse: default False if sort files asc; for desc order set to True
            
        usage::
        
            # e.g. **/*.json for all json files in recursive subfolders
            tmp_folder.clean(glob="**/*.json", n=3)
                
            # e.g. * for all files in the folder
            tmp_folder.clean(glob="*", n=-1)
            
        """

        # list file posixpath in tmp folder with glob parameter having files
        files = [e for e in self.path.glob(glob)]

        if len(files) > n:  # exit fn if file count is less than n
            
            # sort files in asc or desc order
            files = sorted(files, reverse=reverse)

            if n == -1:
                # n = -1 :: all files
                thefiles = files 
            else:
                thefiles = files[:-n]
            
            # delete files until file count is n, e.g. 5
            for file in thefiles:  
                if file.is_file():
                    file.unlink()