""" 
Data and dataframe  helper class for the module Core

hint:
    can be directly called from core as ``core.df``

basic usage::

    from ozcore import core
    core.df.search(df, q="something")

"""

from pathlib import PosixPath
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
import matplotlib.pyplot as plt
from ozcore import core


class Dataframe:
    """  
    helper methods for dataframe operations
    
    """
    def update_a_df_column(self, df_to_update:DataFrame, df_as_source:DataFrame, unique_col:str, col_to_update:str):
        '''
        Updates a Dataframe column with a source Dataframe based on their common unique columns
        
        parameters:
            df_to_update: dataframe, main df to be updated
            df_as_source: dataframe, source df to update the main df
            unique_col: str,
                common columns (should have same name) to match records, 
                this unique column must have unique values
            col_to_update: str, which column value to be updated
        
        returns:
            a copy of the updated DataFrame     

        warning:
            index is reset during the update
        '''
        # copy df
        df = df_to_update.copy()
        source = df_as_source.copy()
        
        # reset index: WARNING: drops index if exist
        df.reset_index(inplace=True, drop=True)
        source.reset_index(inplace=True, drop=True)
        
        # set unique_col as index
        df.set_index(unique_col, inplace=True)
        source.set_index(unique_col, inplace=True)
        
        # update on series
        df[col_to_update].update(source[col_to_update])
        
        # reset index: WARNING: puts back the index to first
        df.reset_index(inplace=True, drop=False)
        source.reset_index(inplace=True, drop=False)

        return df    

    def pngTable(self, df:DataFrame, colwidth_factor:float=0.20, fontsize:int = 12, formatFloats:bool = True, 
                 save:bool = False, in_folder:PosixPath = None):  
        '''
        Displays or saves a table as png.
        Uses matplotlib => pandas plotting table.
        
        parameters:
            df: dataframe or pivot table
            colwidth_factor: float, default 0.20, defines the width of columns
            fontsize: int, default 12
            formatFloats: bool, default True, formats as two digit prettiy floats
            save: saves the png file as table.png
            in_folder: posixpath, default None, folder to save the png file
        
        returns:
            png file in Downloads folder
        '''
        if not isinstance(in_folder, PosixPath) or not in_folder.exists():
            in_folder = core.folder.Downloads
        
        # file name and path
        path = in_folder.joinpath(f"table-{core.now_prefix()}.png")
        
        # format floats - two digits
        if formatFloats:
            df.applymap(lambda x: '{:,.2f}'.format(x) if isinstance(x, float) else x)

        # get pandas.plotting.table
        table = pd.plotting.table
        
        fig, ax = plt.subplots(figsize=(1.9*df.shape[1], 0.3*df.shape[0])) # set size frame
        ax.xaxis.set_visible(False)  # hide the x axis
        ax.yaxis.set_visible(False)  # hide the y axis
        ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
        tabla = table(ax, df, loc='upper left', colWidths=[colwidth_factor]*len(df.columns))  # where df is your data frame
        tabla.auto_set_font_size(False) # Activate set fontsize manually
        tabla.set_fontsize(fontsize) # if ++fontsize is necessary ++colWidths
        tabla.scale(1.2, 1.2) # change size table
        if save:
            plt.savefig(fname=path, bbox_inches="tight", pad_inches=1) # save
            # https://stackoverflow.com/questions/56328353/matplotlib-savefig-cuts-off-pyplot-table
            plt.close()
            print(f"saved in Downloads folder as {path.stem}.png")
        else:
            plt.show() # show the result
            plt.close()

    def compare_two_df(self, df_1, df_2, col_to_compare:str, side="both"):
        """ 
        Compares two dataframes based on a given column, aka given common Series

        warning:
            This comparison is only checking the identical values in a Series. Other columns may not match.
            
        parameters:
            df_1: dataframe 1
            df_2: dataframe 2
            col_to_compare (str): column to make the comparison, which is common 
            side: str, default `both`, options: `left`, `right`
            
        returns:
            * a dataframe with diffrences of df_1 from df_2
            * empty if all match
        """
        df1 = df_1.copy()
        df2 = df_2.copy()
        
        df1.sort_values(col_to_compare, inplace=True)
        df2.sort_values(col_to_compare, inplace=True)
        df1.reset_index(drop=False, inplace=True)
        df2.reset_index(drop=False, inplace=True)
        
        left = df1[~df1[col_to_compare].isin(df2[col_to_compare])]
        right = df2[~df2[col_to_compare].isin(df1[col_to_compare])]
        both = pd.concat([left,right])
        
        if side == "left":
            return left
        elif side == "right":
            return right
        else:
            return both
        
    def add_a_col_from_a_df(self, into_df:DataFrame, from_df:DataFrame, unique_col:str, col_to_add:str ):
        """  
        Add a column into a dataframe from another dataframe
        
        parameters:
            into_df: dataframe, main df, which will be updated with a new column
            from_df: dataframe, source df, which has the column to add into main df
            unique_col: str, column name which is common in both dataframes
            col_to_add: str, column to be added from source dataframe
            
        returns:
            * main dataframe filled with the new column and values, where unique column matches
        
        warning:
            this method assumes no index
        """
        
        main = into_df.copy()
        source = from_df.copy()
        
        return main.merge(source[[unique_col, col_to_add]], on=unique_col, how="left")
    
    def search(self, df_to_search, q, columns=None):
        """ 
        Search all or any column of a dataframe, where columns having str (type: object) 
        
        parameters:
            df_to_search: dataframe to be searched
            q: str, query term
            columns: str | list, default None, columns to search, if None all columns
            
        returns:
            a dataframe with found records
            
        note:
            index columns are not included.
        """
        df = df_to_search.copy()
        
        if columns is None:
            df_cols = df
        elif isinstance(columns, str):
            df_cols = df[[columns]]
        elif isinstance(columns, list):
            df_cols = df[columns]
        
        return df[df_cols.apply(lambda x: x.str.contains(q, case=False, na=False).any() \
                                            if x.dtype == "object" else x, axis=1)]
        