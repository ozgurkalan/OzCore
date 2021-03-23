""" 
Dummy records, ready to use

hint:
    can be directly called from core as ``core.dummy``

usage::

    from ozcore import core
    
    core.dummy.emp
    #...returns a dataframe with 10 records
    
    core.dummy.dataframe(n=3, template="emp", verbose=True)
    #...returns a dataframe with 3 records using **emp** template
    
    core.dummy.df1
    #...returns a dataframe with faked with seed 99 having shape(5,5)
    
    core.dummy.df2
    #...returns another dataframe with faked with seed 99 having shape(5,5)
    
    core.dummy.df1
    #...returns another dataframe with faked with seed 99 having shape(5,4)

"""
import pandas as pd
from faker import Faker

class Dummy:
    """  
    ready-to-use dummy records, created using Faker
    
    """
    def __init__(self):
        """ no seed defined. 
        Faker langs:
            "tr_TR","en_US","it_IT","de_DE","fr_FR"
        
        """
        self.df = pd.DataFrame() # initiate dataframe
        # multi-national faker data
        self.fake = Faker(["tr_TR","en_US","it_IT","de_DE","fr_FR"])
        
    @property
    def emp(self):
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
            
        TODO: dummy
            * new templates other than emp, e.g. np arrays
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
        if n<2:
            n = 2
        
        emp = self.fake.json(data_columns={
            "user_name":"user_name",
            "prefix":"prefix",
            'first_name': 'first_name', 'last_name': 'last_name', 
            "job":"job",
            "city":"city",
            "country":"country",
            "email":"email",
            "password":"password",
            "phone_number":"phone_number", 
            }, num_rows=n)
        
        return emp
    
    @property
    def df1(self):
        """  
        Dataframe with Faker's seed 99
        
        returns:
            Dataframe shape(5,5), 5th col as datetime object
        """
        return self._make_df_w_seed_99(1)
    
    @property
    def df2(self):
        """  
        Dataframe with Faker's seed 99
        
        returns:
            Dataframe shape(5,5), 5th col as dict object
        """
        return self._make_df_w_seed_99(2)
    
    @property
    def df3(self):
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
        df = df.assign(col4=[fake.pyfloat(left_digits=2, right_digits=2) for _ in range(5)])
        # 3rd df with 4 columns
        df3 = df.copy()
        
        df = df.assign(col3=[fake.name() for _ in range(5)])
        df = df.assign(col4=[fake.pyfloat(left_digits=2, right_digits=2) for _ in range(5)])
        df = df.assign(col5=[fake.date_time() for _ in range(5)])
        # first df with 5th column dtype as datetime 
        df1 = df.copy()
        
        df = df.assign(col3=[fake.name() for _ in range(5)])
        df = df.assign(col4=[fake.pyfloat(left_digits=2, right_digits=2) for _ in range(5)])
        df.col5=[fake.pyset(value_types=[str], variable_nb_elements=False, nb_elements=3) for _ in range(5)]
        # second df with 5th column dtype as dict object
        df2 = df.copy()
        
        if df_no == 1:
            return df1
        elif df_no == 2:
            return df2
        else:
            return df3
        
    
