from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from aiohttp import ClientSession
from skekraft.const import (
    CMD_LOGIN,
    CMD_REFRESH,
    CLIENT_HEADERS,
)

class HttpClient:
    _session: ClientSession
    _baseurl: str
    inexistent_endpoints: List[str]

    def __init__(self, baseurl):
        self._baseurl = baseurl
        self._session = ClientSession()
        self.inexistent_endpoints = []
        self._dst = None

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()

    async def refresh(self, dst: str = None) -> None:
        refresh_url = f"{self._baseurl}/JsonRequest/{CMD_REFRESH}"
        if dst is not None:
            dstTest = dst
        else:
            dstTest = self._dst
        payload = {"DST": dstTest}
        # 100-level (Informational) – server acknowledges a request
        # 200-level (Success) – server completed the request as expected
        # 300-level (Redirection) – client needs to perform further actions to complete the request
        # 400-level (Client error) – client sent an invalid request
        # 400-Bad Request
        # 401-Unauthorized
        # 403-Forbidden
        # 404-Not Found
        # 412-Precondition Failed
        # 500-level (Server error) – server failed to fulfill a valid request due to an error with server
        # 500 Internal Server Error
        # 503 Service Unavailable
        try:
            async with self._session.post(
                    refresh_url, headers=CLIENT_HEADERS, json=payload, ssl=False
            ) as response:
                if response.status == 404:
                    self.inexistent_endpoints.append(command)
                    raise ValueError(f"The id or name for {command} was not found.")
                elif response.status == 500:
                    raise ValueError(f"Token invalid need reauth")
                self._dst = dstTest
                data: Dict[str, Any] = await response.json()
                return data
            return None
        except Exception as e:
            return False
    async def login(self, username: str, password: str):
        login_url = f"{self._baseurl}/JsonRequest/{CMD_LOGIN}"
        payload = {"username": username, "password": password}
        # 100-level (Informational) – server acknowledges a request
        # 200-level (Success) – server completed the request as expected
        # 300-level (Redirection) – client needs to perform further actions to complete the request
        # 400-level (Client error) – client sent an invalid request
        # 400-Bad Request
        # 401-Unauthorized
        # 403-Forbidden
        # 404-Not Found
        # 412-Precondition Failed
        # 500-level (Server error) – server failed to fulfill a valid request due to an error with server
        # 500 Internal Server Error
        # 503 Service Unavailable
        try:
            async with self._session.post(
                    login_url, headers=CLIENT_HEADERS, json=payload, ssl=False
            ) as response:
                if response.status == 404:
                    self.inexistent_endpoints.append(command)
                    raise ValueError(f"The id or name for {command} was not found.")

                data: Dict[str, Any] = await response.json()
                self._dst = data['Dst']
                return data
            return None
        except Exception as e:
            return False

    async def logout(self):
        await self._session.close()

    async def run_command(self, command: str, **kwargs):
        commandurl = f"{self._baseurl}/JsonRequest/{command}"
        payload = {"DST": self._dst}
        if 'payload' in kwargs.keys():
            payload = {**payload, **kwargs['payload']}
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'sv-SE,sv;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://minasidor.skekraft.se',
            'Connection': 'keep-alive',
            'Referer': 'https://minasidor.skekraft.se/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        }
        if 'headers' in kwargs.keys():
            headers = {**headers, **kwargs['headers']}

        if command in self.inexistent_endpoints:
            raise ValueError(f"The command {command} was not found.")

        async with self._session.post(
            commandurl, headers=headers, json=payload, ssl=False
        ) as response:
            if response.status == 404:
                self.inexistent_endpoints.append(command)
                raise ValueError(f"The id or name for {command} was not found.")

            data: Dict[str, Any] = await response.json()
            return data