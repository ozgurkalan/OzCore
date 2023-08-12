"""test utils/temporal.py"""
from unittest.mock import patch
import pytest
from ozcore import core
from datetime import datetime
import pytz


class TestTempo:
    """test Tempo class"""
    def setup_method(self, method):
        self.data = { 
        "utc" : datetime(2018, 1, 2, 3, 4, 5, 654000, pytz.utc),
        "utc_ts" :  int(datetime(2018, 1, 2, 3, 4, 5, 654000, pytz.utc).timestamp() * 1000),
        "utc_zs" : datetime(2018, 1, 2, 3, 4, 0, 0, pytz.utc), # zero second
        "utc_zs_ts" : int(datetime(2018, 1, 2, 3, 4, 0, 0, pytz.utc).timestamp() * 1000),
        "nz" : datetime(2018, 1, 2, 3, 4, 5, 654000), # no zone
        "nz_ts" : int(datetime(2018, 1, 2, 3, 4, 5, 654000).replace(tzinfo=pytz.utc).timestamp() * 1000),
        "zs_nz" : datetime(2018, 1, 2, 3, 4, 0, 0), # zero second, no zone
        "zs_nz_ts" : int(datetime(2018, 1, 2, 3, 4, 0, 0).replace(tzinfo=pytz.utc).timestamp() * 1000),
        "nz_m1" : datetime(2018, 1, 2, 3, 3, 5, 654000), # no zone, -1 minute
        "nz_m1_ts" : int(datetime(2018, 1, 2, 3, 3, 5, 654000).replace(tzinfo=pytz.utc).timestamp() * 1000),
        "nz_p1" : datetime(2018, 1, 2, 3, 5, 5, 654000), # no zone, +1 minute
        "nz_p1_ts" : int(datetime(2018, 1, 2, 3, 5, 5, 654000).replace(tzinfo=pytz.utc).timestamp() * 1000),
        "zs": datetime(2018, 1, 2, 3, 4, 0, 0, pytz.utc), # zero second, utc
        "zs_ts": int(datetime(2018, 1, 2, 3, 4, 0, 0, pytz.utc).timestamp() * 1000),
        "zs_p1": datetime(2018, 1, 2, 3, 5, 0, 0, pytz.utc), # zero second, utc, +1 minute
        "zs_p1_ts": int(datetime(2018, 1, 2, 3, 5, 0, 0, pytz.utc).timestamp() * 1000),
                    }
    
    @pytest.fixture
    def expected(self, request):
        return self.data[request.param]
    
    @pytest.fixture
    def given(self, request):
        return self.data[request.param]
    
    @pytest.mark.parametrize("ts, zerosecond, nozone, expected", [
        (False, False, False, "utc"),
        (True, False, False, "utc_ts"),
        (False, True, False, "utc_zs"),
        (True, True, False, "utc_zs_ts"),
        (False, False, True, "nz"),
        (True, False, True, "nz_ts"),
        (False, True, True, "zs_nz"),
        (True, True, True, "zs_nz_ts"),
    ], indirect=["expected"])
    def test_now(self, ts, zerosecond, nozone, expected):
        # GIVEN Tempo class with now method
        # WHEN now method is called
        # THEN returns current datetime in UTC timezone
        with patch("ozcore.core.tempo") as mock_datetime:
            mock_datetime.now.return_value = expected
            assert core.tempo.now(to_timestamp=ts, zerosecond=zerosecond, nozone=nozone) == expected
            
    
    def test_str_to_datetime(self):
        # GIVEN Tempo class with str_to_datetime method
        # WHEN str_to_datetime method is called
        # THEN returns datetime object from a given string with miliseconds in UTC time zone
        s = "January 01, 2018"
        assert core.tempo.str_to_datetime(s) == datetime(2018, 1, 1, 0, 0, 0, 0, pytz.utc)
        assert core.tempo.str_to_datetime(s).tzinfo == pytz.utc
        
        
    def test_str_to_timestamp(self):
        # GIVEN Tempo class with str_to_timestamp method
        # WHEN str_to_timestamp method is called
        # THEN returns timestamp as int in ms from a given string in UTC time zone
        s = "January 01, 2018"
        assert core.tempo.str_to_timestamp(s) == int(datetime(2018, 1, 1, 0, 0, 0, 0, pytz.utc).astimezone(pytz.utc).timestamp() * 1000)
        
    @pytest.mark.parametrize("zerosecond, nozone, given, expected", [
        (False, False, "utc", "utc"),
        (False, False, "utc_ts", "utc"),
        (True, False, "utc_zs", "utc_zs"),
        (True, False, "utc_zs_ts", "utc_zs"),
        (False, True, "nz", "nz"),
        (False, True, "nz_ts", "nz"),
        (True, True, "zs_nz", "zs_nz"),
        (True, True, "zs_nz_ts", "zs_nz"),
    ], indirect=["given","expected"])
    def test_to_dt(self, zerosecond, nozone, given, expected):
        # GIVEN Tempo class with to_dt method
        # WHEN to_dt method is called
        # THEN returns datetime object from a given timestamp in UTC time zone
        assert core.tempo.to_dt(t=given, zerosecond=zerosecond, nozone=nozone) == expected
        
        # check one of the pytz info
        assert core.tempo.to_dt(self.data["utc_ts"]).tzinfo == pytz.utc
        
        
    def test_to_ts(self):
        # GIVEN Tempo class with to_ts method
        # WHEN to_ts method is called
        # THEN returns timestamp as int in ms from a given datetime in UTC time zone
        assert core.tempo.to_ts(self.data["utc"]) == self.data["utc_ts"]
        
    def test_time_past(self):
        # GIVEN Tempo class with time_past method
        # WHEN time_past method is called
        # THEN returns time difference in seconds between now and a given datetime
        assert core.tempo.time_past(start=self.data["nz"], end=self.data["nz_p1"], unit="m") == 1
        assert core.tempo.time_past(start=self.data["nz"], end=self.data["nz_m1"], unit="m") == -1
            
    
    def test_shifting(self):
        # GIVEN Tempo class with three shifting methods
        # WHEN shift_a_minute_fwd method is called
        # THEN returns timestamp int shifted by a minute forward
        assert core.tempo.shift_a_minute_fwd(self.data["nz"]) == self.data["nz_p1_ts"]
        # WHEN shift_a_minute_back method is called
        # THEN returns timestamp int shifted by a minute backward
        assert core.tempo.shift_a_minute_back(self.data["nz"]) == self.data["nz_m1_ts"]
        # WHEN shift method is called
        # THEN returns timestamp int shifted by a given number of minutes
        assert core.tempo.shift(self.data["nz"], minutes=1) == self.data["nz_p1_ts"]
        
        
    def test_ts_series(self):
        # GIVEN Tempo class with ts_series method
        # WHEN ts_series method is called
        # THEN returns a list of timestamps int shifted by a given number of minutes
        start = self.data["zs"]
        end = self.data["zs_p1"]
        start_ts = self.data["zs_ts"]
        end_ts = self.data["zs_p1_ts"]
        assert core.tempo.ts_series(start=start, end=end).isin([end_ts, start_ts]).all()
        
        
    def test_epochs(self):
        # GIVEN Tempo class with epochs method
        # WHEN epochs method is called
        # THEN length of ts_series is equal to number of epochs
        assert core.tempo.ts_series(start=self.data["nz"], 
                                    end=self.data["nz_p1_ts"]).shape[0] == 2
        
    
    