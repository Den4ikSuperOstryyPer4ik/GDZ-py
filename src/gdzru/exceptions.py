#                © Copyright 2023
#         Licensed under the MIT License
#       https://opensource.org/licenses/MIT
#    https://github.com/Den4ikSuperOstryyPer4ik

from typing import Any, Optional


class APIError(Exception):
    """Request API Error"""

    def __init__(self, url: str, status_code: int, details: Optional[Any] = None) -> None:
        error_text = f"RequestError [{status_code}]:\nURL: {url}"

        super().__init__(error_text)

        self.url = url
        self.status_code = status_code
        self.details = details
