from setuptools import setup, find_packages
from dunamai import Version, Style

setup(
   
   version=Version.from_any_vcs().serialize(style=Style.SemVer),
   packages = find_packages(exclude=["docs", "tests"]),  
)
