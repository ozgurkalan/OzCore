""" 
Processing and marking a csv file.

"""
import numpy as np
import logging

from .base import Base

class Process(Base):
    """ 
    Class for processing and marking csv files.
    Drived from Base class.
    ! And, cannot be initiated if validation fails.
    
    hint:
        This module can be used to modify fields in a csv file and tick mark completed rows...
    
    warning:
        Processing CSV assumes that the csv file has no index defined. Also, no kwargs are passed to read_csv method of Pandas.
        
    notes:
        You need to define a path to the csv file in order to initiate the Process class. 
        
    warning:
        If no process header found in CSV, this class raises an Exception
    
    usage::
    
        from ozcore.core.data.csv.process import Process as csv_process
        
        csv = csv_process(path="path_to_csv")
        
        csv.focus(0)
        # focus first record
        
        csv.processed()
        # mark first record as processed and save it to csv files
        
        csv.next()
        # focus on next unprocessed record (marked as 0) if exists
        
    create a processed column::

        # to use this class, a processed column with 0 values should be available
        # warning: there may be similar column, please check before proceeding
        
        from ozcore import core
        
        df = core.csv.read(file)
        
        df = df.assign(processed=0)
        df.processed = df.processed.astype(int)
        df.loc[:,"processed"] = 0
        
        core.save(df, index=False, overwrite=True)
        
        # now you can initiate the Process class
        
    deleting the processed column::
    
        # when you are finished with marking csv file you can remove it
        # warning: be sure to remove
        
        from ozcore import core
        
        df = core.csv.read(file)
        
        df.drop(columns="processed", inplace=True)
        
        core.save(df, index=False, overwrite=True)
        
        # column is removed
    
    """
    
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.focus_index = None # initate focus ID
        self.validate_csv # validate the csv if fits criteria
        
            
      
    @property  
    def validate_csv(self):
        """  
        Validates the CSV if fits the strict rules for processing a CSV file.
        
        
        """
        self.read(path=self.path)
        
        df = self.df
        
        if not "processed" in df.columns:
            raise Exception("your Dataframe has no `processed` column!")
        
        if not all(np.isin(df.processed.unique(), [1,0])):
            raise Exception("your processed column in the Dataframe may only have 1 or 0")
        
        return True
        
    
    def focus(self, index, verbose=True):
        """ 
        the record which is in progress
            all write actions is applied to this Serie
        
        paramaters:
            index: int, index number of the record being focused
            verbose: bool, default True
            
        returns:
            fills self.focus_index and displays the Series
            if verbose displays a warning msg
        """
        serie = self.df.loc[index]
        if serie.empty:
            raise Exception("no data in this Serie")
        
        if verbose:
            logging.warning(f"You have focused index: "+str(index)+"!")
            
        self.focus_index=index
        return serie
        
    def next(self):
        """  
        next unprocessed item where processed==0 is displayed and assigned as focused
        
        returns:
            Series
        """
        df = self.df[self.df.processed==0]
        if not df.empty:
            index = df.iloc[0].name
            return self.focus(index)
        else:
            logging.warning("All items are processed")
 
    def processed(self, revert=False):
        """ 
        marks a records as processed by assigning 1
        
        parameters:
            revert: boolean, default False

        usage:
            when a records focused by focus(index) or next() methods
            assigns 1 to processed column (0 if revert is True)
            saves the file
        """
        index = self.focus_index
        
        val = 0 if revert else 1
        
        if index is None:
            msg = "No records focused yet!"
            logging.error(msg)
            raise Exception(msg)
        elif index not in self.df.index:
            msg = "cannot find the focused record with this index:"+str(index)
            logging.error(msg)
            raise Exception(msg)
        else:
            self.df.loc[index, "processed"]=val
            if not revert:
                msg =  "The record is marked as processed at index: "+str(index)
            else:
                msg =  "The record is remarked as unprocessed at index: "+str(index)
            logging.warning(msg)
            self.save(self.df)
