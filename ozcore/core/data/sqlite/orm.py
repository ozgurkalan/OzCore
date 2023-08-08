""" sqlite alter operations  """

import logging

import alembic
import pandas as pd
import sqlalchemy as sa


class ORM:
    """
    Sqlite alter operations with ORM and Alembic

    warning:
        The ``sa_`` prefixed methods are for advanced usage

    """

    def __init__(self):
        pass

    def sa_add_a_column(self, table_name, column_name, type_=sa.TEXT):
        """
        alter table: add a new column in the given table

        parameters:
            table_name: str
            column_name: str, name for the new column

        returns:
            * creates the column in the table as Text type
            * returns Error if exception

        warning:
            new column is created as ``sqlalchemy.sql.sqltypes.Text``
        """
        col = column_name
        if self.engine is None:
            msg = "No engine found! Please set_engine()"
            raise Exception(msg)
        elif not self.table_exists(table_name):
            msg = f"{table_name} does not exists in this database!"
            logging.error(msg)
            raise Exception(msg)
        elif self.column_exists(table_name, col):
            msg = f"{col} already exists in {table_name}!"
            logging.error(msg)
            raise Exception(msg)
        # elif not isinstance(type_, sa.sql.visitors.Visitable):
        #     # sa.sql.visitors.VisitableType checks if the type_ argument is an Sqlalchemy type
        #     msg = f"{type(type_)} is not an Sqlalchemy type!"
        #     logging.error(msg)
        #     raise Exception(msg)

        with self.engine.connect() as conn:
            ctx = alembic.runtime.migration.MigrationContext.configure(conn)
            op = alembic.operations.Operations(ctx)
            if not isinstance(col, sa.sql.schema.Column):
                col = sa.Column(col, type_=type_)
            else:
                if isinstance(col.type, sa.sql.sqltypes.NullType):
                    # assign a type_ if col is NullType (otherwise error raised by albemic for NullType)
                    col.type = type_
            op.add_column(table_name, col)  # add column

        return True

    def sa_drop_a_column(self, table_name, column_name):
        """
        alter table: drop a column from a table

        parameters:
            table_name: str
            column_name: str, as column name or a sqlalchemy Column object

        returns:
            drops the column in the given table
        """
        col = column_name
        if isinstance(col, sa.sql.schema.Column):
            col = col.name

        if self.engine is None:
            logging.error("No engine found! Please set_engine()")
            raise Exception("No engine found!")
        elif not self.table_exists(table_name):
            logging.error(f"{table_name} does not exists in this database!")
            return False
        elif not self.column_exists(table_name, col):
            logging.error(f"{col} does not exists in {table_name}!")
            return False

        with self.engine.connect() as conn:
            ctx = alembic.runtime.migration.MigrationContext.configure(conn)
            op = alembic.operations.Operations(ctx)
            with op.batch_alter_table(table_name) as batch_op:
                # sqlite has different column operation
                # alembic solves this issue with batch_alter_table
                batch_op.drop_column(col)  # drop column

        return True

    def sa_change_column_type(self, table_name, column_name, type_):
        """
        alter table: change a column's type

        parameters:
            table_name: str
            column_name: str, as column name or a sqlalchemy Column object
            type_: Sqlalchemy Type

        returns:
            * True if type is changed successfully

        usage::

            import core

            core.sql.("table_name", "column_name", type_=sa.TEXT)
            # type changed to SQLalchemy Text type

        """
        col = column_name
        if self.engine is None:
            logging.error("No engine found! Please set_engine()")
            raise Exception("No engine found!")
        elif not self.table_exists(table_name):
            logging.error(f"{table_name} does not exists in this database!")
            return False
        elif not self.column_exists(table_name, col):
            logging.error(f"{col} does not exists in {table_name}!")
            return False
        # elif not isinstance(type_, sa.sql.visitors.Visitable):
        #     # sa.sql.visitors.VisitableType checks if the type_ argument is an Sqlalchemy type
        #     logging.error(f"{type(type_)} is not an Sqlalchemy type!")
        #     return False

        with self.engine.connect() as conn:
            ctx = alembic.runtime.migration.MigrationContext.configure(conn)
            op = alembic.operations.Operations(ctx)
            with op.batch_alter_table(table_name) as batch_op:
                # sqlite has no drop column operation
                # alembic solves this issue with batch_alter_table
                batch_op.alter_column(col, type_=type_)  # change column type

    def sa_table(self, table_name: str):
        """
        Sqalchemy Table object of a given table

        parameters:
            table_name: str or Sqlalchemy Table object

        returns:
            Sqlalchemy Table object of the set engine
        """
        if isinstance(table_name, sa.sql.schema.Table):
            table_name = table_name.name

        if not self.table_exists(table_name):
            logging.error(f"{table_name} does not exists in this database!")
            return False
        metadata = sa.MetaData()
        metadata.reflect(self.engine)
        return sa.Table(table_name, metadata)

    def sa_column(self, table_name: str, column_name: str):
        """
        Sqalchemy Column object of a given table

        parameters:
            table_name: str
            column_name: str
        """

        tbl = self.sa_table(table_name)
        table_name = tbl.name

        if isinstance(column_name, sa.sql.schema.Column):
            column_name = column_name.name

        if not self.column_exists(table_name, column_name):
            logging.error(f"{column_name} does not exists in {table_name}!")
            return False

        return tbl.columns[column_name]

    def sa_update_a_record(
        self, table_name, column_name, compare_column, compare_val, val
    ):
        """
        update a single record in a given column of a table

        parameters:
            table_name: str or Sqlalchemy Table object
            column_name: str or Sqlalchemy Column object
            compare_column: str, the common unique columnn to compare record
            compare_val: mixed, a value to compare in compare_column
            val: mixed, the new value of the record
        """

        tbl = self.sa_table(table_name)
        col = self.sa_column(tbl, column_name)

        with self.engine.connect() as conn:
            expr = tbl.update().where(tbl.c[compare_column] == compare_val).values(
                {column_name: val}
            )
            conn.execute(expr)
            conn.commit()

    def sa_update_a_column(self, table_name, column_name, compare_column, source_df):
        """
        update a column's records based on a given df_slice

        parameters:
            table_name: str or Sqlalchemy Table object
            column_name: str or Sqlalchemy Column object
            compare_column: str, the common unique columnn to compare record
            compare_val: mixed, a value to compare in compare_column
            source_df: source records as a DataFrame or Series, to update the Table

        warning:
            index of source_df is ignored

        """
        df = source_df.copy()

        # if df_slice is Series type
        if isinstance(df, pd.core.series.Series):
            df = df.to_frame().T

        # check df validatiy
        if not isinstance(df, pd.core.frame.DataFrame) or df.empty:
            raise TypeError("Source df should be valid DataFrame and not be empty!")

        tbl = self.sa_table(table_name)
        col = self.sa_column(table_name, column_name)

        if not compare_column in df:
            raise Exception(f"{compare_column} is not in {tbl.name}")

        if not isinstance(compare_column, str):
            logging.error("Unique column name should be str")
            raise TypeError("Unique column name should a String")

        for row in df.iterrows():
            row = row[1]
            self.sa_update_a_record(
                table_name=tbl.name,
                column_name=col.name,
                compare_column=compare_column,
                compare_val=row[compare_column],
                val=row[column_name],
            )

        return True
