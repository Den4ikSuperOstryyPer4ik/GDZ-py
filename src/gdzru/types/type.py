#                © Copyright 2023
#         Licensed under the MIT License
#       https://opensource.org/licenses/MIT
#    https://github.com/Den4ikSuperOstryyPer4ik

import json
import typing
from datetime import date, datetime, timedelta
from enum import Enum

from pydantic import BaseModel


class Type(BaseModel):
    @staticmethod
    def __default__(obj: typing.Any):
        if isinstance(obj, (bytes, typing.Match)):
            return repr(obj)
        elif isinstance(obj, (Enum, datetime, date, timedelta)):
            return str(obj)

        return {
            "_": obj.__class__.__name__,
            **{
                attr: getattr(obj, attr)
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            },
        }

    def __str__(self) -> str:
        return json.dumps(self, indent=4, default=Type.__default__, ensure_ascii=False)
