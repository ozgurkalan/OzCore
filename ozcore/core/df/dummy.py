""" 
Dummy records, ready to use

hint:
    can be directly called from core as ``core.df.dummy``

usage::

    from ozcore import core
    
    core.df.dummy.emp
    #...returns a dataframe with 10 records
    
    core.df.dummy.dataframe(n=3, template="emp", verbose=True)
    #...returns a dataframe with 3 records using **emp** template
    
    core.df.dummy.df1
    #...returns a dataframe faked with seed 99 having shape(5,5)
    
    core.df.dummy.df2
    #...returns another dataframe faked with seed 99 having shape(5,5)
    
    core.df.dummy.df1
    #...returns another dataframe faked with seed 99 having shape(5,4)
    
    core.df.dummy.df_dup_parent_child
    #...returns a dataframe with seed 9 having shape(20,4)
    
    core.df.dummy.df_country_scores
    #...returns a dataframe with seed 0 having shape(50,2)
    
    core.df.dummy.fake.name_female()
    # ... you also have access to Faker class
    
    
TODO: col with years

"""
import pandas as pd
from pandas.core.frame import DataFrame
from faker import Faker
import numpy as np


class Dummy:
    """
    ready-to-use dummy records, created using Faker

    """

    def __init__(self):
        """no seed defined.
        Faker langs:
            "tr_TR","en_US","it_IT","de_DE","fr_FR"

        """
        self.df = pd.DataFrame()  # initiate dataframe
        # multi-national faker data
        self.fake = Faker(["tr_TR", "en_US", "it_IT", "de_DE", "fr_FR"])

    @property
    def emp(self) -> DataFrame:
        """
        ready to use dummy employee dataframe with 10 records

        returns:
            dataframe with 10 records
        """
        self.dataframe(template="emp", n=10, verbose=False)
        return self.df

    def dataframe(self, template="emp", n=10, verbose=True):
        """
        create a dummy dataframe

        parameters:
            n: int, number of records, default 10
            template: str, default "emp", choose from ready templates
            verbose: bool, default True

        returns:
            * if verbose, returns the dataframe
            * else, assigns class df values

        warning:
            Cannot assign 1 record only, if n<2 then n=2

        """
        df = self.df

        if template == "emp":
            df = pd.read_json(self._json_employee(n=n))

        df = df.assign(birthday=None)
        df.birthday = df.birthday.apply(lambda x: self.fake.date_of_birth())
        df = df.assign(log=None)
        df.log = df.log.apply(lambda x: self.fake.date_time_this_year())

        self.df = df

        if verbose:
            return df

    def _json_employee(self, n=10):
        """
        dummy json object with keys for employee template

        parameters:
            n: int, number of records, default 10

        returns:
            json object
        """
        # cannot assign less then 2 records
        if n < 2:
            n = 2

        emp = self.fake.json(
            data_columns={
                "user_name": "user_name",
                "prefix": "prefix",
                "first_name": "first_name",
                "last_name": "last_name",
                "job": "job",
                "city": "city",
                "country": "country",
                "email": "email",
                "password": "password",
                "phone_number": "phone_number",
            },
            num_rows=n,
        )

        return emp

    @property
    def df1(self) -> DataFrame:
        """
        Dataframe with Faker's seed 99

        returns:
            Dataframe shape(5,5), 5th col as datetime object
        """
        return self._make_df_w_seed_99(1)

    @property
    def df2(self) -> DataFrame:
        """
        Dataframe with Faker's seed 99

        returns:
            Dataframe shape(5,5), 5th col as dict object
        """
        return self._make_df_w_seed_99(2)

    @property
    def df3(self) -> DataFrame:
        """
        Dataframe with Faker's seed 99

        returns:
            Dataframe shape(5,4)
        """
        return self._make_df_w_seed_99(3)

    def _make_df_w_seed_99(self, df_no=1):
        """
        creates a dummy Dataframe with Faker seed 99

        parameters:
            df_no: int, default 1, can be 1 , 2 or 3

        returns:
            * a dataframe
            * all three dataframes have their first 2 columns identical
            * df_no=1: (5,5), 5th col as datetime object
            * df_no=2: (5,5), 5th col as dict object
            * df_no=3: (5,4)

        """
        # Faker with seed 99
        fake = Faker()
        Faker.seed(99)

        df = pd.DataFrame()
        df = df.assign(col1=list("abcde"))
        df = df.assign(col2=range(5))
        df = df.assign(col3=[fake.name() for _ in range(5)])
        df = df.assign(
            col4=[fake.pyfloat(left_digits=2, right_digits=2) for _ in range(5)]
        )
        # 3rd df with 4 columns
        df3 = df.copy()

        df = df.assign(col3=[fake.name() for _ in range(5)])
        df = df.assign(
            col4=[fake.pyfloat(left_digits=2, right_digits=2) for _ in range(5)]
        )
        df = df.assign(col5=[fake.date_time() for _ in range(5)])
        # first df with 5th column dtype as datetime
        df1 = df.copy()

        df = df.assign(col3=[fake.name() for _ in range(5)])
        df = df.assign(
            col4=[fake.pyfloat(left_digits=2, right_digits=2) for _ in range(5)]
        )
        df.col5 = [
            fake.pyset(value_types=[str], variable_nb_elements=False, nb_elements=3)
            for _ in range(5)
        ]
        # second df with 5th column dtype as dict object
        df2 = df.copy()

        if df_no == 1:
            return df1
        elif df_no == 2:
            return df2
        else:
            return df3
        
    @property
    def df_dup_parent_child(self) -> DataFrame:
        """Dataframe with Faker's seed 9  having two non-unique columns

        returns:
            Dataframe shape(20,4)
        """
        # Faker with seed 9
        fake = Faker()
        Faker.seed(9)

        count = 20
        df = pd.DataFrame(
            {
                "parent": fake.random_elements(
                    elements=(
                        "root",
                        "subfolder_A",
                        "subfolder_B",
                        "subfolder_C",
                        "subfolder_D",
                    ),
                    length=count,
                ),
                "child": fake.random_elements(
                    elements=(
                        "subfolder_E",
                        "subfolder_F",
                        "subfolder_G",
                        "subfolder_H",
                        "subfolder_J",
                    ),
                    length=count,
                ),
                "path": [fake.file_path() for _ in range(count)],
                "user": [fake.name() for _ in range(count)],
            }
        )
        return df

    @property
    def df_country_scores(self):
        """Dataframe with Faker's seed 0 of countries with scores
        
        returns:
            Dataframe shape(50,2)
            
        hint:
            * begins with Tanzania, score 1 and ends with Germany score 50
            * 50 countries 
        """
        # Faker with seed 0
        fake = Faker()
        Faker.seed(0)
        
        df=pd.DataFrame([(fake.country(), _+1 )for _ in range(50)], columns=['country','score'])
        return df
    
    @property
    def df_sales_per_year(self):
        """Dataframe with random sales and quantity results per three years
            Faker seed: 999, numpy random number seed: 99
        
        returns:
            Dataframe shape(60,7)
            
        hint:
            * columns: ['salesperson', 'industry', 'year', 'transaction', 'unit', 'result', 'rando']
            * years: [2022, 2021, 2023], all int
            * industry: ['Automotive','Healthcare','Manufacturing','Hightech','Retail']
            * rando: random number; np.arange(30)
            * result: float
        """
        fake = Faker()
        Faker.seed(999)
        np.random.seed(99)
        df = pd.DataFrame()
        
        r = 30
        f = {}
        
        industry = ['Automotive','Healthcare','Manufacturing','Hightech','Retail']
        year = [2023, 2021, 2022]
        for i in range(r):
            f[i] = {}
            f[i]["salesperson"] = fake.name()
            f[i]['industry'] = fake.random_element(industry)
            f[i]['year'] = fake.random_element(year)
            f[i]['transaction'] = 'sales'
            f[i]['unit'] = 'USD'
            f[i]['result'] = np.round(np.random.normal(1000,200)) *1_000
            f[i]['rando'] = fake.random_element(np.arange(r))
            
        df = pd.DataFrame(f).T

        f = {}
        for i in range(r):
            f[i] = {}
            f[i]["salesperson"] = fake.name()
            f[i]['industry'] = fake.random_element(industry)
            f[i]['year'] = fake.random_element(year)
            f[i]['transaction'] = 'quantity'
            f[i]['unit'] = 'PCS'
            f[i]['result'] = np.abs(np.round(np.random.normal(50,100)))
            f[i]['rando'] = fake.random_element(np.arange(r))

        df = pd.concat([df, pd.DataFrame(f).T], ignore_index=True)
        df = df.astype({'salesperson':object, 'industry':'category', 'year':int, 'transaction':'category', 'unit':'category', 'result':float, 'rando':int}, copy=True)
        
        return df