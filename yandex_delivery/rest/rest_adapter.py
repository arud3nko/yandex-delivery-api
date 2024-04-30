"""

This module describes REST adapter class

"""

import logging
from json import JSONDecodeError

import aiohttp

from .exceptions import YandexDeliveryApiError
from .rest_result import Result


class RestAdapter:
    """

    This class describes common REST operations

    """
    def __init__(self,
                 hostname:        str,
                 api_key:         str,
                 ver:             str,
                 content_type:    str,
                 accept_language: str,
                 timeout:         int = None,
                 retries:         int = 0,
                 logger:          logging.Logger = None):
        """

        RestAdapter Constructor

        :param hostname: b2b.taxi.yandex.net/b2b/cargo/integration
        :param api_key: OAuth-token
        :param ver: API version
        :param content_type: Content-Type header
        :param accept_language: Accept-Language header
        :param timeout: Timeout in seconds / None to request without timeout
        :param retries: Additional attempts
        :param logger: (optional) logger instance
        """
        self._logger = logger or logging.getLogger(__package__)
        self.url = f"https://{hostname}/{ver}"
        self.content_type = content_type
        self.accept_language = accept_language
        self._api_key = api_key
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._retries = retries

    async def _do(self,
                  http_method: str,
                  endpoint:    str,
                  params:      dict[str, str] = None,
                  payload:     dict = None) -> Result:
        """

        REST operations common method

        :param http_method: GET, POST, DELETE, etc.
        :param endpoint: URL Endpoint
        :param params: Params
        :param payload: Dictionary with payload
        :return: Result instance
        """
        full_url = self.url + endpoint
        headers = {'content-type': self.content_type, 'Accept-Language': self.accept_language,
                   'Authorization': f'Bearer {self._api_key}'}
        log_line_pre = f"method={http_method}, url={full_url}, params={params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))

        for _ in range(1 + self._retries):
            try:
                self._logger.debug(msg=log_line_pre)
                async with aiohttp.ClientSession(headers=headers, timeout=self._timeout) as session:
                    response = await session.request(
                        method=http_method,
                        url=self.url + endpoint,
                        params=params,
                        json=payload
                    )

                    try:
                        data_out = await response.json()
                    except (ValueError, TypeError, JSONDecodeError) as e:
                        self._logger.error(msg=log_line_post.format(False, None, e))
                        raise YandexDeliveryApiError("Bad JSON in response") from e

                break
            except aiohttp.ClientError as e:
                self._logger.error(msg=str(e))
                raise YandexDeliveryApiError("Request failed") from e
            except (TimeoutError, aiohttp.ServerTimeoutError) as e:
                self._logger.error(msg=str(e))
                if _ >= self._retries:
                    raise YandexDeliveryApiError("Timeout error") from e
                continue

        is_success = 299 >= response.status >= 200
        if is_success:
            return Result(response.status,
                          headers=response.headers,
                          message=response.reason,
                          data=data_out)
        raise YandexDeliveryApiError(f"{response.status}: {response.reason} "
                                     f"({data_out['message']})")

    async def get(self,
                  endpoint: str,
                  params: dict[str, str] = None,
                  payload: dict = None) -> Result:
        """
        Implements GET method
        """
        return await self._do(http_method='GET',
                              endpoint=endpoint,
                              params=params,
                              payload=payload)

    async def post(self,
                   endpoint: str,
                   params: dict[str, str] = None,
                   payload: dict = None) -> Result:
        """
        Implements POST method
        """
        return await self._do(http_method='POST',
                              endpoint=endpoint,
                              params=params,
                              payload=payload)

    async def delete(self,
                     endpoint: str,
                     params: dict[str, str] = None,
                     payload: dict = None) -> Result:
        """
        Implements DELETE method
        """
        return await self._do(http_method='DELETE',
                              endpoint=endpoint,
                              params=params,
                              payload=payload)
