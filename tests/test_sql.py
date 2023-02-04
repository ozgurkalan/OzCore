"""  
Tests for sqlite helper classes

warning:
    Some of the tests depend on ``apps/world/world.db``
"""
import os
import pytest
from pathlib import Path
import sqlalchemy as sa
import sqlite3

from ozcore import core
from ozcore.core.data.sqlite.sqlite import Sqlite as SQL # import it separately for fresh instance


class TestBase:
    """ basics
    """
    
    PATH = None  # will be set as the tmpdir posixpath
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, tmpdir, monkeypatch):
        # define pytest's tmpdir as PosixPath
        path = Path(tmpdir)
        self.PATH = path
        
        # pytest to run cwd in tests folder
        def mock_cwd():
            return Path(__file__).parent.resolve()
        monkeypatch.setattr(os,"getcwd", mock_cwd)
        

        # create sqlite file
        for db in ["db","sqlite","sqlite3"]:
            with sqlite3.connect(path.joinpath(f"sample.{db}")):
                pass
        
        yield
        # clean
        for file in path.glob("*.*"):
            if file.is_file():
                file.unlink()
        self.PATH = None
        
        

    @pytest.mark.parametrize("db", [("db"),("sqlite"),("sqlite3"),])
    def test_creating_an_engine_with_a_file_path_as_posixpath(self, db):
        # GIVEN tmpdir has 3 sqlite files with 3 different extentions
        db_path = self.PATH.joinpath(f"sample.{db}")
        sql = core.sql(db_path)
        # WHEN engine created from db_path
        db_engine = sql.create_engine(db_path)
        # THEN self.engine should be of sa engine type
        assert isinstance(db_engine, sa.engine.Engine)
        # THEN should match the engines' url 
        assert str(db_engine.url) == db_path.as_uri().replace("file:/", "sqlite://")
        
    def test_creating_an_engine_with_a_file_path_as_str(self):
        # GIVEN tmpdir has sample.db file
        db_path = self.PATH.joinpath(f"sample.db")
        sql = core.sql(db_path)
        # WHEN engine created from db_path as str
        db_engine = sql.create_engine(str(db_path))
        # THEN self.engine should be of sa engine type
        assert isinstance(db_engine, sa.engine.Engine)
        # THEN should match the engines' url 
        assert str(db_engine.url )== db_path.as_uri().replace("file:/", "sqlite://")
        
        
    def test_creating_an_engine_with_only_a_folder_path_error(self):
        # GIVEN tmpdir has 3 sqlite files with 3 different extentions
        path = self.PATH
        # WHEN the tmp folder is given to create an engine
        # THEN just a folder raise an error
        with pytest.raises(Exception):
            core.sql(path)


        
    def test_creating_an_engine_raises_errors(self):
        # GIVEN there should be no valid database files in tests folder (not subfolders)
        # WHEN path given
        # THEN should raise an error
        with pytest.raises(Exception):
            core.sql(path=Path(__file__))
        
        # GIVEN tmpdir has 3 sqlite files with 3 different extentions
        # WHEN sample.db wrong given and non-existing file path passed
        # THEN should raise an error
        with pytest.raises(Exception):
            core.sql(path=self.PATH.joinpath("wrong_name.db"))
            
    
    def test_setting_an_engine_with_a_relative_path_string(self, tmp_folder):
        # GIVEN sample.db in ./test_folder/tmp
        with sqlite3.connect(tmp_folder.joinpath("sample.db")):
            pass
        # WHEN engine param is set as a relative path string with wrong extension
        # THEN should raise error
        with pytest.raises(Exception) as exec_info:
            core.sql("test_folder/tmp/sample.dbX", return_engine=True)
        
        # clean db
        tmp_folder.joinpath("sample.db").unlink()
        
        
class TestSqlite:
    """Sqlite class """
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, tmpdir):
        # tmp dir
        path = Path(tmpdir).joinpath("sample.db")
        # create sqlite file
        with sqlite3.connect(path) as conn:
            core.df.dummy.df1.to_sql(name="df1", con=conn, index=False, if_exists='replace')
            # skip the dict column in col5
            core.df.dummy.df2.iloc[:,0:-1].to_sql(name="df2", con=conn, index=False, if_exists='replace') 
            core.df.dummy.df3.to_sql(name="df3", con=conn, index=False, if_exists='replace')
            
        yield
        
        # clean and teardown
        for file in path.glob("*.db"):
            if file.is_file():
                file.unlink()

    @pytest.fixture()
    def sql(self, tmpdir):
        return core.sql(Path(tmpdir).joinpath("sample.db"))
    
    def test_metadata_of_set_engine(self, sql):
        # WHEN sql metadata is available
        # THEN should be a member of SQlAlchemy MetaData type
        assert isinstance(sql.metadata, sa.MetaData)
        
        
    def test_tables_in_sample_db(self, sql):
        # GIVEN tables df1, df2, df3
        tables = sql.tables
        # WHEN request tables count
        # THEN should get 3
        assert len(tables) == 3
        # THEN df1 should be in tables enum
        assert tables.df1.name == "df1"
        # THEN also table_list must match tables
        assert sql.tables_list == [e.name for e in sql.tables]
        
    def test_columns_object_in_a_table(self, sql):
        # GIVEN tables df1, df2, df3
        # WHEN request df1
        # THEN columns should match dummy.df1
        assert [e.name for e in sql.columns(sql.tables.df1)] == list(core.df.dummy.df1.columns)
        
    def test_if_column_exits_works_well(self, sql):
        # GIVEN table df1 derived from core.df.dummy.df1
        # WHEN request col1 if exists in columns
        # THEN should assert True
        assert sql.column_exists("df1", "col1") == True
        # THEN also assert False for a non-existing column
        assert sql.column_exists("df1", "a_non_existing_column") == False
        
    def test_if_table_exits_works_well(self, sql):
        # GIVEN table df1 derived from core.df.dummy.df1
        # WHEN request df1 as table_name
        # THEN should assert True
        assert sql.table_exists("df1") == True
        # THEN also assert False for a non-existing table
        assert sql.table_exists("a_non_existing_table_name") == False
        
    def test_path_to_database_reveals_the_correct_database_path(self, tmpdir, sql):
        # GIVEN the sample.db database in tmp folder
        # WHEN database path requested
        # THEN should give the path as engine created
        db_path = Path(tmpdir).joinpath("sample.db")
        
        assert db_path == Path(sql.engine.url.database)
    
    @pytest.mark.parametrize(
        "limit",
        [(1),(3),(5)]
    )    
    def test_reading_a_table_from_database(self, limit, sql):
        # GIVEN table df1 derived from core.df.dummy.df1
        df = core.df.dummy.df1
        # WHEN read from df1 table in db
        db = sql.read(table_name="df1", limit=limit, index_column=None)
        # THEN they should match
        
        assert all(df.iloc[0:limit] == db)
        
    
class TestORM:
    """ Test ORM Class """
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, tmpdir):
        # tmp dir
        path = Path(tmpdir).joinpath("sample.db")
        # create sqlite file
        with sqlite3.connect(path) as conn:
            core.df.dummy.df1.to_sql(name="df1", con=conn, index=False, if_exists='replace')
            # skip the dict column in col5
            core.df.dummy.df2.iloc[:,0:-1].to_sql(name="df2", con=conn, index=False, if_exists='replace') 
            core.df.dummy.df3.to_sql(name="df3", con=conn, index=False, if_exists='replace')

        yield
        
        # clean and teardown
        for file in path.glob("*.db"):
            if file.is_file():
                file.unlink()
        
    @pytest.fixture()
    def sql(self, tmpdir):
        return core.sql(Path(tmpdir).joinpath("sample.db"))
      
    def test_adding_a_new_column_in_a_table(self, sql):
        # GIVEN table df1 derived from core.df.dummy.df1
        df = core.df.dummy.df1
        # WHEN a new column added
        col = "a_new_column"
        # THEN it should be in db' table' columns
        sql.sa_add_a_column("df1", col)
        db = sql.read("df1")
        assert list(db.columns.difference(df.columns)) == [col]
        
        # WHEN an exiting column tried to be added
        # THEN should rise an exception
        with pytest.raises(Exception):
            sql.sa_add_a_column("df1", col)
            
    def test_droping_a_column_in_a_table(self, sql):
        # GIVEN table df1 derived from core.df.dummy.df1
        df = core.df.dummy.df1
        # WHEN droping col1
        # THEN we have no col1
        sql.sa_drop_a_column("df1", "col1")
        db = sql.read("df1")

        assert list(df.columns.difference(db.columns)) == ["col1"]      
        
    def test_changing_a_column_type(self, sql):
        # GIVEN table df1 derived from core.df.dummy.df1
        # GIVEN col2 is int
        # WHEN we change col2 dtype int to str in db
        # THEN we should get a str from col2
        sql.sa_change_column_type("df1","col2",type_=sa.TEXT)
        db = sql.read("df1")
        
        assert sql.read("df1").col2.dtype == sa.TEXT
        
        
    def test_sa_table_is_a_table_object(self, sql):
        # GIVEN table df1 derived from core.df.dummy.df1
        # WHEN sa_table requested
        # THEN returns a sa.Table object
        assert type(sql.sa_table("df1")) == sa.Table

    def test_sa_column_is_a_column_object_of_a_given_table(self, sql):
        # GIVEN table df1 derived from core.df.dummy.df1
        # WHEN sa_column requested
        # THEN returns a sa.column object
        assert type(sql.sa_column("df1","col1")) == sa.Column
        
    def test_updating_a_record_in_a_table(self, sql):
        # GIVEN table df1 derived from core.df.dummy.df1
        # WHEN col1 first record=a and we update it as x
        # THEN should be the read csv returns that field
        sql.sa_update_a_record(table_name="df1", column_name="col1", compare_column="col2", compare_val=0, val="x")
        
        db = sql.read("df1")
        
        assert db.loc[0,"col1"] == "x"
        
    def test_updating_entire_column_with_a_given_df(self, sql):
        # GIVEN table df1 derived from core.df.dummy.df1 as table to be updated
        # GIVEN table df2 derived from core.df.dummy.df2 having a diffrent col3 (person names than df1)
        # WHEN we update col3 - the people 
        # THEN our first record in col3 should be ``Christina Cobb`` according to Faker name in seed 99
        source_df = core.df.dummy.df2
        sql.sa_update_a_column(table_name="df1", column_name="col3", compare_column="col1", source_df=source_df)
        assert sql.read("df1").loc[0,"col3"] == source_df.loc[0, "col3"]
        