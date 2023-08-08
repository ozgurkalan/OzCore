""" 
sqlite helper methods 
"""


import enum
from pathlib import Path, PosixPath, WindowsPath
from typing import Union

import pandas as pd
import sqlalchemy as sa
from typeguard import typechecked

from ozcore import core

from .orm import ORM


class Sqlite(ORM):
    """
    Sqlite helper methods using ``ORM`` class

    Set the engine before using or if .db is in the current folder, creates the engine automatically

    warning:
        set_engine() before proceeding any other method!

    usage::

        from ozcore import core

        sql= core.sql(path_to_database)

        sql.tables.table_name
        sql.path_to_database

        sql.read(table_name, engine, limit=100)

    """

    DB_EXTENTIONS = ["db", "sqlite", "sqlite3"]

    def __init__(self, path: Union[str, PosixPath, WindowsPath]):
        self.engine = self.create_engine(path)
        self.tables_list = []
        self.columns_list = {}

    @typechecked
    def create_engine(self, path: Union[str, PosixPath, WindowsPath]):
        """
        Creates an engine.

        parameters:
            path: str | posixpath, path to the sqlite db

        returns:
            Engine object

        note:
            Allowed extensions: "db","sqlite","sqlite3"
        """

        path = core.folder.check_path(path, is_file=True)

        if path.suffix.replace(".", "") not in self.DB_EXTENTIONS:
            raise Exception(
                f"This is not a valid Sqlite file! Allowed extentions: \n{self.DB_EXTENTIONS}"
            )

        return sa.create_engine("sqlite:///" + str(path), echo=False)

    @typechecked
    def set_engine(
        self,
        engine: Union[sa.engine.Engine, str, PosixPath, WindowsPath],
        return_engine: bool = False,
    ):
        """
        Set the engine to work with.

        parameters:
            engine: sqlalchemy engine, Posixpath, or str
            return_engine: bool, default False, returns the engine set

        returns:
            * fills self engine
            * if returns=True, returns the engine set

        warning:
            To work with **core.sql** methods, you should first set the engine!

        usage::

            # with an engine name
            core.sql.set_engine(engine=core.sql.engines._ENGINE_NAME)

            # with an relative path
            core.sql.set_engine(engine="./sample.db")

        """

        if isinstance(engine, sa.engine.Engine):
            engine = engine

        else:
            engine = self.create_engine(engine)

        self.engine = engine
        if return_engine:
            return engine

    @property
    def tables(self):
        """
        enum tables in a database

        returns:
            a table name from Enum
            also, assigns table names as a list in self.tables_list

        usage::

            core.sql.tables.table_name
        """
        tables = sa.inspect(self.engine).get_table_names()
        en = enum.IntEnum("tables", tables)
        self.tables_list = [e.name for e in en]
        return en

    def columns(self, table_name):
        """
        enum columns in a table

        parameters:
            table_name: str|enum

        returns:
            enum columns (.name as str name, .value as sa col object)
            also assigns this query to self.columns_list as a dict
        """
        engine = self.engine

        if isinstance(table_name, enum.Enum):
            table_name = table_name.name

        if not self.table_exists(table_name):
            raise Exception("table name not found in the database!")
        metadata = sa.MetaData()
        metadata.reflect(engine)
        cols = [col for col in sa.Table(table_name, metadata).columns]
        names = [e.name for e in cols]
        dic = dict(e for e in zip(names, cols))

        en = enum.Enum("columns", dic)
        self.columns_list[table_name] = [e.name for e in en]
        return en

    def column_exists(self, table_name, col_name):
        """
        checks if a column name exists in a table

        parameters:
            table_name: str|enum
            col_name: str|enum

        returns:
            boolean
        """
        cols = self.columns(table_name)

        if col_name in cols.__dict__.keys():
            return True
        else:
            return False

    def table_exists(self, table_name):
        """
        checks if a table name exists in a database

        parameters:
            table_name: str|enum

        returns:
            boolean
        """
        tbls = self.tables

        if isinstance(table_name, enum.Enum):
            table_name = table_name.name

        if table_name in tbls.__dict__.keys():
            return True
        else:
            return False

    @property
    def path_to_database(self):
        """
        path to database from current engine

        parameters:
            engine
        """
        return Path(self.engine.url.database)

    def read(self, table_name, limit=None, index_column=None):
        """
        read a table

        parameters:
            table_name: str
            limit: int, default None

        returns:
            a dataframe with table results
        """
        engine = self.engine

        if not isinstance(engine, sa.engine.Engine):
            raise Exception("Engine must be set!")

        if isinstance(table_name, enum.Enum):
            table_name = table_name.name

        if not self.table_exists(table_name):
            raise Exception("table name not found in the database!")

        sql = "SELECT * from " + table_name

        if isinstance(limit, int):
            sql += " LIMIT " + str(limit)

        return pd.read_sql(sql, con=engine, index_col=index_column)
