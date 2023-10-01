#                © Copyright 2023
#         Licensed under the MIT License
#       https://opensource.org/licenses/MIT
#    https://github.com/Den4ikSuperOstryyPer4ik

from typing import ClassVar, TypeVar

import requests
from aiohttp import ClientResponse, ClientSession
from pydantic import BaseModel

from gdzru.exceptions import APIError
from gdzru.types import BookInfo, FullBookList, TaskInfo
from gdzru.types.type import Type

T = TypeVar("T", Type, BaseModel)


class BaseAPIWrapper:
    """
    A base API requests wrapper.
    """

    BASE_URL = "https://gdz-ru.com"
    HEADERS: ClassVar[dict] = {
        "User-Agent": "okhttp/4.9.1",
    }


class AsyncAPI(BaseAPIWrapper):
    """
    An asynchronous wrapper for the gdz.ru API.
    """

    async def get(self, url: str, response_type: T = None, **kwargs) -> T | ClientResponse:
        """
        Asynchronously sends a GET request to the specified URL.

        Args:
            url (str): The URL or path of the method to send the request to.
            response_type (Optional[T]): The expected type of the response. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            T | Response: The response from the GET request.
                If a response_type is specified, the response will be validated and returned as an instance of that type
                Otherwise, the raw response object is returned.

        Raises:
            gdzru.exceptions.APIError: If the response status >= 400, an APIError is raised with the status code
        """
        url = self.BASE_URL + url if not url.startswith(self.BASE_URL) else url

        async with ClientSession(headers=self.HEADERS) as session:
            response = await session.get(url, **kwargs)

        if response.status >= 400:
            raise APIError(response.url, response.status, await response.text())

        return response_type.model_validate_json(await response.text()) if response_type else response

    async def get_books_list(self, country_id: int = 1) -> FullBookList:
        """
        Retrieve the full book list for a specific country.

        Args:
            country_id (int): The ID of the country. Defaults to 1.

        Returns:
            FullBookList: The full book list for the specified country.
        """
        return SyncAPI().get_books_list(country_id=country_id)

    async def get_book(self, url: str) -> BookInfo:
        """
        Retrieves book information from the specified URL.

        Args:
            url (str): The URL of the book.

        Returns:
            gdzru.types.BookInfo: The information of the book.
        """
        return await self.get(url, response_type=BookInfo)

    async def get_attachment(self, url: str) -> bytes:
        """
        Retrieve the contents of an attachment/cover/image from a given URL.

        Args:
            url (str): The URL of the attachment/cover/image.

        Returns:
            bytes: The contents of the attachment.
        """
        response = await self.get(url)
        return response.content

    get_cover = get_image = get_attachment

    async def get_task(self, method: str) -> TaskInfo:
        """
        Retrieves a task using the specified method.

        Args:
            method (str): The method to use for retrieving the task.

        Returns:
            TaskInfo: The retrieved task information.
        """
        return await self.get(method, response_type=TaskInfo)


class SyncAPI(BaseAPIWrapper):
    """
    A synchronous wrapper for the gdz.ru API.
    """

    def get(self, url: str, response_type: T = None, **kwargs) -> T | requests.Response:
        """
        Asynchronously sends a GET request to the specified URL.

        Args:
            url (str): The URL or path of the method to send the request to.
            response_type (Optional[T]): The expected type of the response. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            T | Response: The response from the GET request.
                If a response_type is specified, the response will be validated and returned as an instance of that type
                Otherwise, the raw response object is returned.

        Raises:
            gdzru.exceptions.APIError: If the response status >= 400, an APIError is raised with the status code
        """
        url = self.BASE_URL + url if not url.startswith(self.BASE_URL) else url

        response = requests.get(url, timeout=30, headers=self.HEADERS, **kwargs)

        if response.status_code >= 400:
            raise APIError(response.url, response.status_code, response.text)

        return response_type.model_validate_json(response.text) if response_type else response

    def get_books_list(self, country_id: int = 1) -> FullBookList:
        """
        Retrieve the full book list for a specific country.

        Args:
            country_id (int): The ID of the country. Defaults to 1.

        Returns:
            FullBookList: The full book list for the specified country.
        """
        return self.get(
            f"/full-book-list?country_id={country_id}",
            response_type=FullBookList
        )

    def get_book(self, url: str) -> BookInfo:
        """
        Retrieves book information from the specified URL.

        Args:
            url (str): The URL of the book.

        Returns:
            gdzru.types.BookInfo: The information of the book.
        """
        return self.get(url, response_type=BookInfo)

    def get_attachment(self, url: str) -> bytes:
        """
        Retrieve the contents of an attachment/cover/image from a given URL.

        Args:
            url (str): The URL of the attachment/cover/image.

        Returns:
            bytes: The contents of the attachment.
        """
        response = self.get(url)
        return response.content

    get_cover = get_image = get_attachment

    def get_task(self, method: str) -> TaskInfo:
        """
        Retrieves a task using the specified method.

        Args:
            method (str): The method to use for retrieving the task.

        Returns:
            TaskInfo: The retrieved task information.
        """
        return self.get(method, response_type=TaskInfo)
