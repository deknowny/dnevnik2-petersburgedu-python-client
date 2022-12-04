# Dnevnik2 peterburgsedu python client
> Python async/await client for getting studying related info (i.e. marks) from https://dnevnik2.petersburgedu.ru/

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dnev2spb)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/dnev2spb)
![PyPI](https://img.shields.io/pypi/v/dnev2spb)
[![Coverage Status](https://coveralls.io/repos/github/deknowny/dnevnik2-petersburgedu-python-client/badge.svg?branch=main)](https://coveralls.io/github/deknowny/dnevnik2-petersburgedu-python-client?branch=main)
***
__**Check out documentation**__: [https://deknowny.github.io/dnevnik2-petersburgedu-python-client/latest/](https://deknowny.github.io/dnevnik2-petersburgedu-python-client/latest/)

# Features
[x] Email auth
[x] Fetch children and schools
[x] Fetch subjects and marks
[ ] TODO: Cover other API endpoints, PRs are welcome!

## Overview
An example of fetching the latest mark:
```python
import asyncio
import datetime

from dnev2spb.client import APIAuthedClient


async def main():
    login = "YOUR_EMAIL"
    password = "YOUR_PASSWORD"

    client = await APIAuthedClient.new(
        login, password
    )
    children = await client.get_child_related()
    marks = await client.get_marks(
        education_id=children[0].educations[0].education_id,
        date_from=datetime.date(year=2022, month=9, day=1),
        date_to=datetime.date(year=2022, month=12, day=27),
        limit=1000,
        page=1
    )
    print(marks[0].json())
    await client.close_connection()

asyncio.run(main())
```
The output:
```json
{
  "date": "03.12.2022",
  "education_id": 362992,
  "estimate_comment": null,
  "estimate_type_code": 1058,
  "estimate_type_name": "Работа на уроке",
  "estimate_value_code": "5/5",
  "estimate_value_name": "5",
  "id": 2022424944,
  "lesson_id": 121707594,
  "subject_id": 92154,
  "subject_name": "Биология"
}
 ```

# Installation
Via PyPI:
```shell
python -m pip install dnev2spb
```
Or via GitHub
```shell
python -m pip install https://github.com/deknowny/dnevnik2-petersburgedu-python-client/archive/main.zip
```
# Contributing
Check out [site Contributing section](https://deknowny.github.io/dnevnik2-petersburgedu-python-client/latest/contributing/)
