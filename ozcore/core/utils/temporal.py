"""datetime related temporal methods in Tempo class"""

from datetime import datetime
from typing import Union
import numpy as np
import pandas as pd

import pytz
import dateparser


class Tempo:
    """temporal methods
    
    usage:
        tempo = core.tempo
        
        tempo.now() # returns current datetime in UTC timezone
        tempo.now(to_timestamp=True) # returns current timestamp in UTC timezone
        tempo.now(zerosecond=True, nozone=True) # returns current datetime with seconds and microseconds set to 0 and timezone set to None
        
        tempo.str_to_datetime(s) # returns datetime object from a given string with miliseconds in UTC time zone
        tempo.str_to_timestamp(s) # returns timestamp as int in ms from a given string in UTC time zone
        
        tempo.to_dt(t, zerosecond=True, nozone=True) # returns datetime object from a given timestamp in UTC time zone with seconds and microseconds set to 0 and timezone set to None
        
        tempo.to_ts(dt, zerosecond=True, nozone=True) # returns timestamp as int in ms from a given datetime object in UTC time zone with seconds and microseconds set to 0 and timezone set to None

        tempo.time_past(start, end, unit="m") # returns time passed between start and end in given unit
        
        tempo.shift_a_minute_fwd(dt) # returns datetime object shifted a minute forward
        tempo.shift_a_minute_back(dt) # returns datetime object shifted a minute backward
        tempo.shift(dt, minutes=10) # returns datetime object shifted with a given minutes
        
        tempo.ts_series(start, end) # returns timestamp series between start and end in 1 minute interval
        tempo.epochs(start, end) # returns epochs between start and end 
    
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def now(
        cls, to_timestamp: bool = False, zerosecond: bool = False, nozone: bool = False
    ) -> Union[datetime, int]:
        """Returns current datetime or timestamp in UTC timezone
        
        parameters:
            to_timestamp: bool, if True, returns timestamp in ms
            zero_second: bool, if True, seconds and microseconds are set to 0
            nozone: bool, if True, timezone is set to None
            
        returns:
            datetime object with miliseconds in UTC time zone
            if to_timestamp is True, returns timestamp in ms
            if zeroseconds is True, seconds and microseconds are set to 0
            if nozone is True, timezone is set to None
        
        """
        dt =  datetime.now(pytz.utc)
        if to_timestamp:
            return cls.to_ts(dt, zerosecond=zerosecond, nozone=nozone)
        else:
            return cls.to_dt(dt, zerosecond=zerosecond, nozone=nozone)

    @classmethod
    def str_to_datetime(cls, s: str) -> datetime:
        """Returns datetime object from a given string with miliseconds in UTC time zone

        Parameters:
            s: string, e.g.: "January 01, 2018", "11 hours ago UTC", "now UTC"
            
        warning: 
            "January 01, 2018" has no seconds nor miliseconds, so they are set to 0
        """
        
        if not isinstance(s, str):
            s = str(s)
        
        dt = dateparser.parse(s, settings={"TIMEZONE": "UTC"} )
        
        dt = dt.replace(tzinfo=pytz.utc)
        
        if dt.second is None:
            dt = dt.replace(second=0)
        
        if dt.microsecond is None:
            dt = dt.replace(microsecond=0)

        return dt

    @classmethod
    def str_to_timestamp(cls, s: str) -> int:
        """Returns timestamp as int in ms from a given string in UTC time zone

        Parameters:
            s: string
        """
        t = cls.str_to_datetime(s)
        
        return cls.to_ts(t)

    @classmethod
    def to_dt(
        cls,
        t: Union[int, str, datetime],
        zerosecond: bool = False,
        nozone: bool = False,
    ) -> datetime:
        """Returns datetime object from any given temporal object

        Parameters:
            t: int|str|datetime, any temporal object to converted to datetime
            zerosecond: bool, if True, seconds and microseconds are set to 0
            nozone: bool, if True, timezone is set to None

        returns:
            datetime object with miliseconds in UTC time zone
            if zeroseconds is True, seconds and microseconds are set to 0
            if nozone is True, timezone is set to None
        """
        if isinstance(t, datetime):
            dt = cls.str_to_datetime(str(t))
        elif isinstance(t, int) or isinstance(t, np.int64):
            dt = datetime.fromtimestamp(t / 1000, pytz.utc)
        elif isinstance(t, str):
            dt = cls.str_to_datetime(t)
        else:
            return None

        if zerosecond:
            dt = dt.replace(second=0, microsecond=0)

        if nozone:
            dt = dt.replace(tzinfo=None)

        return dt

    @classmethod
    def to_ts(
        cls,
        t: Union[int, str, datetime],
        zerosecond: bool = False,
        nozone: bool = False,
    ) -> int:
        """Returns timestamp in ms from any given temporal object

        parameters:
            t: int|str|datetime, any temporal object to converted to timestamp
            zerosecond: bool, if True, seconds and microseconds are set to 0
            nozone: bool, if True, timezone is set to None

        returns:
            int, timestamp in ms in UTC time zone
            if zeroseconds is True, seconds and microseconds are set to 0
            if nozone is True, timezone is set to None

        """
        dt = cls.to_dt(t, zerosecond=zerosecond, nozone=nozone)
        return int(dt.timestamp() * 1000)

    @classmethod
    def time_past(cls, start: Union[int, str, datetime], end:Union[int, str, datetime]=None, unit:str="m") -> Union[float, int]:
        """Returns time past from a given temporal object

        parameters:
            start: int|str|datetime, any temporal object to measure
            end: int|str|datetime, any temporal object to measure from, default is now if given None
            unit: str, unit to measure, e.g.: "m" for minutes, "h" for hours, "s" for seconds, default is "m"

        returns:
            float or int, time past in given unit

        """
        start = cls.to_dt(start)
        
        if end is None:
            end = cls.now()
        else:
            end = cls.to_dt(end)
            
        delta = end - start
        
        s = delta.total_seconds()
        m = s / 60
        h = m / 60

        if unit == "s":
            return s
        elif unit == "m":
            return m
        elif unit == "h":
            return h
        else:
            raise ValueError("unit must be 's', 'm' or 'h'")
    
    @classmethod
    def shift_a_minute_fwd(cls, t: Union[str, int, datetime]) -> int:
        """shift given time one minute forward

        parameters:
            t: Union[str,int, datetime], the time to shift forward

        returns:
            int, the shifted time as timestamp
        """
        # get the time as datetime
        t = cls.to_dt(t)

        # shift the time one minute forward
        new_time = t + pd.Timedelta("1 minute")

        # return the shifted time as timestamp
        return cls.to_ts(new_time)

    @classmethod
    def shift_a_minute_back(cls, t: Union[str, int, datetime]) -> int:
        """shift given time one minute back

        parameters:
            t: Union[str,int, datetime], the time to shift forward

        returns:
            int, the shifted time as timestamp
        """
        # get the time as datetime
        t = cls.to_dt(t)

        # shift the time one minute forward
        new_time = t - pd.Timedelta("1 minute")

        # return the shifted time as timestamp
        return cls.to_ts(new_time)
    
    @classmethod
    def shift(cls, t: Union[int, str, datetime], minutes: int) -> int:
        """shift given time by minutes
        
        parameters:
            t: Union[int, str, datetime], the time to shift
            minutes: int, the minutes to shift (can be negative)
        
        returns:
            int, the shifted time as timestamp
        """
        dt = cls.to_dt(t)
        
        delta = pd.Timedelta(minutes=minutes)
        
        return cls.to_ts(dt + delta)
        
    @classmethod
    def ts_series(cls,
                start:Union[int,str,datetime], end:Union[int,str,datetime]
                ) -> pd.Series:
        """returns the timestamp series between start and end in 1min steps
        
        parameters:
            start: Union[int,str,datetime], the start time
            end: Union[int,str,datetime], the end time
            
        returns:
            pd.Series, the timestamp series between start and end
        """
        # convert start and end to clean datetime
        start = cls.to_dt(start, zerosecond=True)
        end = cls.to_dt(end, zerosecond=True)
        
        t=pd.DataFrame([start, end], columns=["timestamp"], index=[cls.to_dt(start), cls.to_dt(end)])

        t=t.resample("T").asfreq().index.astype(int).sort_values()//10**6
        t = pd.Series(t, name="timestamp")
        
        return t
    
    @classmethod
    def epochs(cls, start:Union[int,str,datetime], end:Union[int,str,datetime])->int:
        """length of epochs between start and end as minutes
            basicly the length of ts_series
        
        parameters:
            start: Union[int,str,datetime], the start time
            end: Union[int,str,datetime], the end time
            
        returns:
            int, the number of epochs between start and end   
        
        """
        return len(cls.ts_series(start, end))