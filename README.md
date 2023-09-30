<p align="center"><a href="https://gdz.ru/"><img src="https://i.ibb.co/VCJF9dc/image-2.png" align="center"/></a> <a href="https://www.python.org/"><img src="https://i.ibb.co/DKCcTDj/image.png" align="center"/></p></a>

# gdz-ru-py
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/downloads/release/python-391/)
[![PyPI - Version](https://img.shields.io/pypi/v/gdzru.svg)](https://pypi.org/project/gdzru)

Python library for using gdz.ru API

-----

**Table of Contents**

- [Installation](#installation)
- [Using](#using)
- [License](#license)


## Installation
### Stable version
```bash
$ pip install gdzru --upgrade
```

### Latest version
```bash
$ pip install https://github.com/OctoDiary/OctoDiary-py/archive/main.zip --upgrade
```

## Using
```python
from gdzru import AsyncAPI, SyncAPI

async def amain():
    """
    Asynchronous using GDZ.ru API
    """
    api = AsyncAPI()

    # Get info for classes, subjects, books, etc.
    info = await api.get_books_list()

    # Get info for one book
    book_info = await api.get_book(info.books[0].url)

    # Print book authors, title, etc.
    print("Title:", book_info.book.title)
    print("Authors:", ", ".join(book_info.book.authors))
    print("Year:", book_info.book.year)
    print("Publisher:", book_info.book.publisher)

    # Get get first task of first book structure
    task_info = await api.get_task(book.structure[0].tasks[0].url)
    print("Task title:", task_info.task.title)


    # Get images of task
    images: list[bytes] = [
        await api.get_image(image.url)
        for image in task_info.task.editions[0].images
    ]

def main():
    """
    Synchronous using GDZ.ru API
    """
    api = SyncAPI()

    # Get info for classes, subjects, books, etc.
    info = api.get_books_list()

    # Get info for one book
    book_info = api.get_book(info.books[0].url)

    # Print book authors, title, etc.
    print("Title:", book_info.book.title)
    print("Authors:", ", ".join(book_info.book.authors))
    print("Year:", book_info.book.year)
    print("Publisher:", book_info.book.publisher)

    # Get get first task of first book structure
    task_info = api.get_task(book.structure[0].tasks[0].url)

    # Print task title
    print("Task title:", task_info.task.title)

    # Get images of task
    images: list[bytes] = [
        api.get_image(image.url)
        for image in task_info.task.editions[0].images
    ]
```


## License

`gdzru` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.