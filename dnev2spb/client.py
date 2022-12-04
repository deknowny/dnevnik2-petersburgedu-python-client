from __future__ import annotations

import dataclasses
import datetime
import ssl
import typing

import aiohttp
import orjson

from dnev2spb.exceptions import BadRequestError
from dnev2spb.models.child_related import ChildRelated
from dnev2spb.models.mark import Mark


async def _send_get_request(
    session: aiohttp.ClientSession,
    url: str,
    user_agent: str,
    headers: typing.Optional[dict] = None,
    params: typing.Optional[dict] = None,
    json: typing.Optional[dict] = None,
) -> dict:
    headers = headers or {}
    headers["User-Agent"] = user_agent
    async with session.get(
        url, headers=headers, params=params, json=json
    ) as response:
        if response.status >= 400:
            raise BadRequestError(status=response.status)
        parsed_response = await response.json(loads=orjson.loads)
        return parsed_response["data"]


@dataclasses.dataclass
class APIAuthedClient:
    session: aiohttp.ClientSession
    jwt_token: str
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    api_endpoint: str = "https://dnevnik2.petersburgedu.ru/api"

    @classmethod
    async def new(
        cls,
        login: str,
        password: str,
        type: typing.Literal["email"] = "email",
        user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        api_endpoint: str = "https://dnevnik2.petersburgedu.ru/api",
    ) -> APIAuthedClient:
        session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl.SSLContext()),
            skip_auto_headers={"User-Agent"},
            raise_for_status=True,
        )
        api_login_response = await _send_get_request(
            session,
            f"{api_endpoint}/user/auth/login",
            user_agent=user_agent,
            json={
                "login": login,
                "password": password,
                "type": type,
                "_isEmpty": False,
            },
        )
        token = api_login_response["token"]

        return APIAuthedClient(session, token, user_agent, api_endpoint)

    async def get_child_related(self) -> typing.List[ChildRelated]:
        api_response = await _send_get_request(
            self.session,
            f"{self.api_endpoint}/journal/person/related-child-list",
            user_agent=self.user_agent,
        )
        return [
            ChildRelated.parse_obj(child) for child in api_response["items"]
        ]

    async def get_marks(
        self,
        education_id: int,
        date_from: datetime.date,
        date_to: datetime.date,
        limit: int,
        page: int,
    ) -> typing.List[Mark]:
        api_response = await _send_get_request(
            self.session,
            f"{self.api_endpoint}/journal/estimate/table",
            user_agent=self.user_agent,
            params={
                "p_educations[]": education_id,
                "p_date_from": format(date_from, "%d.%m.%Y"),
                "p_date_to": format(date_to, "%d.%m.%Y"),
                "p_limit": limit,
                "p_page": page,
            },
        )
        return [Mark.parse_obj(mark) for mark in api_response["items"]]

    async def close_connection(self) -> None:
        await self.session.close()

    def _require_jwt_token(self) -> None:
        pass
