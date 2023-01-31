"""  
tests for module csv_
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from ozcore import core
from ozcore.core.data.csv.process import Process

class Test_CSV_Base_Class:

    TMP = None

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, tmpdir):
        tmp = Path(tmpdir)
        self.TMP = tmp
        # create csv files
        core.df.dummy.df1.to_csv(tmp.joinpath("01_sample.csv"), index=False)
        core.df.dummy.df2.to_csv(tmp.joinpath("02_sample.csv"), index=False)
        core.df.dummy.df3.to_csv(tmp.joinpath("03_sample.csv"), index=False)
        
        yield None 
        # clean and teardown
        [e.unlink() for e in tmp.glob("*.csv")]
        self.TMP = None
        
    def test_reading_a_csv_file(self):
        # GIVEN 03_sample.csv file in tmp folder with core.df.dummy.df3
        file = self.TMP.joinpath("03_sample.csv")
        # WHEN read the csv
        csv = core.csv.read(file)
        # THEN col1 columns should be equal to with dummy df3
        pd.testing.assert_series_equal(core.df.dummy.df3.col1, csv.col1)
        
        
    def test_searching_in_a_csv_file(self):
        # GIVEN 03_sample.csv file in tmp folder with core.df.dummy.df3
        file = self.TMP.joinpath("03_sample.csv")
        core.csv.read(file)
        # WHEN search the csv for 
        result = core.csv.search(q="curtis")
        # THEN result is the first row of df3
        pd.testing.assert_frame_equal(
            result, core.df.dummy.df3.iloc[0:1]
        )
        
    def test_saving_a_csv_file(self):
         # GIVEN 03_sample.csv file in tmp folder with core.df.dummy.df3
        file = self.TMP.joinpath("03_sample.csv")
        core.csv.read(file)
        # GIVEN altered df is same dummy df3 with first row, col3 (name) as hello
        df_altered = core.df.dummy.df3.copy()
        df_altered.loc[0,"col3"] = "hello"
        # WHEN save
        core.csv.save(df_altered, index=False, overwrite=False)
        # THEN result same record is hello
        assert core.csv.df.loc[0,"col3"] == "hello"
        
        # WHEN overwrite if True and alter the csv's data structure by adding a new column
        df_altered = df_altered.assign(new_col=99)
        core.csv.save(df_altered, index=False, overwrite=True)
        # THEN result should be 99
        assert core.csv.df.loc[0, "new_col"] == 99

class Test_CSV_Process_Class:
    
    TMP = None

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, tmpdir):
        tmp = Path(tmpdir)
        self.TMP = tmp
        # create csv files
        core.df.dummy.df1.to_csv(tmp.joinpath("01_sample.csv"), index=False)
        core.df.dummy.df2.to_csv(tmp.joinpath("02_sample.csv"), index=False)
        core.df.dummy.df3.to_csv(tmp.joinpath("03_sample.csv"), index=False)
        
        yield None 
        # clean and teardown
        [e.unlink() for e in tmp.glob("*.csv")]
        self.TMP = None
        
    
    def test_validate_csv_for_processing(self):  
           
        # GIVEN 01_sample.csv file in tmp folder with core.df.dummy.df1
        file = self.TMP.joinpath("01_sample.csv")   
        
        # WHEN csv has no processed column
        # THEN raise Exception
        with pytest.raises(Exception):
            p = Process(path=file)
            
        # WHEN csv has processed column but not in [None, 1, 0]
        # THEN raise Exception
        df = core.df.dummy.df1.copy()
        df = df.assign(processed=0)
        df.processed = df.processed.astype(int)
        df.loc[0,"processed"] = 3 # error, should be between [1, 0]
        df.loc[1,"processed"] = 1
        df.loc[2,"processed"] = np.NAN
        core.csv.read(file)
        core.csv.save(df, index=False, overwrite=True)
        
        # not accepted cause 3 is not allowed in the first row!
        with pytest.raises(Exception):
            p = Process(path=file)
        
        df.loc[0,"processed"] = 1 # correct the errors
        df.loc[2,"processed"] = 1 # correct the errors
        core.csv.save(df, index=False, overwrite=True)
        
        # WHEN we have first three records as processed marked with 1
        p = Process(path=file)
        
        # THEN we validate that this csv file is good for processing
        assert p.validate_csv == True
        

    @staticmethod
    def setup_processed_csv(tmp, mark_all_processed=False):
        file = tmp.joinpath("01_sample.csv")   
        df = core.df.dummy.df1.copy()
        df = df.assign(processed=0)
        df.processed = df.processed.astype(int)
        df.loc[0,"processed"] = 1 # set the first record as processed
        
        if mark_all_processed:
            df.loc[:,"processed"] = 1 # mark all as processed
        
        core.csv.read(file)
        core.csv.save(df, index=False, overwrite=True)
        
    def test_focus_a_record_in_csv(self):
        # first setup the csv
        self.setup_processed_csv(self.TMP)
        
        # read the csv
        file = self.TMP.joinpath("01_sample.csv")   
        pro = Process(path=file)
        
        # set focus to first record
        serie = pro.focus(0, verbose=True)
        
        assert pro.focus_index == 0
        assert (serie == pro.df.iloc[0]).unique().all() # all fields True...
        
    def test_next_record_in_csv(self):
        # first setup the csv
        self.setup_processed_csv(self.TMP)
        
         # read the csv
        file = self.TMP.joinpath("01_sample.csv")   
        pro = Process(path=file)
        
        # next item not processed should be the second record
        nxt = pro.next()
        
        assert pro.focus_index == 1
        assert (nxt == pro.df.iloc[1]).unique().all() # all fields True...
        
        # WHEN all processed
        self.setup_processed_csv(self.TMP, mark_all_processed=True)
        pro = Process(path=file)
        
        
        # next item not processed should be the second record
        nxt = pro.next()
        
        assert nxt == None
        
    @pytest.mark.parametrize(
        "index, reverse, expected",
        # expect 1 or zero as processed
        [
            (1, False, 1),
            (2, False, 1),
            (0, True, 0)
        ]
    )
    def test_marking_records_processed_or_reverse(self, index, reverse, expected):
         # first setup the csv
        self.setup_processed_csv(self.TMP)
        
         # read the csv
        file = self.TMP.joinpath("01_sample.csv")   
        pro = Process(path=file)
        
        with pytest.raises(Exception):
            pro.processed()
            # because no focus record set yet
            
        pro.focus(index)
        pro.processed(revert=reverse)
        
        df = core.csv.read(file)
        assert df.loc[index, "processed"] == expected
        
    