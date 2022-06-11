from dataclasses import dataclass, field
from typing import Optional
import datetime as dt

@dataclass
class Document:
    """
    Domain model of a Document.
    """

    # Instance variables
    id:             Optional[int]           = field(init=True, default=None)
    title:          str                     = field(init=True, default="")
    content:        str                     = field(init=True, default="")
    create_date:    Optional[dt.datetime]   = field(init=True, default=None)
    modify_date:    Optional[dt.datetime]   = field(init=True, default=None)