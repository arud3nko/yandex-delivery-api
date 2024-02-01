"""
This module describes REST adapter result class
"""

from dataclasses import dataclass
from aiohttp.typedefs import CIMultiDictProxy


@dataclass
class Result:
    """
    REST adapter result class
    """
    def __init__(self, status_code: int, headers: CIMultiDictProxy[str], message: str = '', data: list[dict] = None):
        """
        Result returned from low-level RestAdapter
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
        """
        self.status_code = int(status_code)
        self.headers = headers
        self.message = str(message)
        self.data = data if data else []
