""" version of the package OzCore. """

from dunamai import Version, Style
__version__ = Version.from_any_vcs().serialize(style=Style.SemVer)
del Version, Style
