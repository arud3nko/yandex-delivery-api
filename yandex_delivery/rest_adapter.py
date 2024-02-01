import aiohttp
import logging

from json import JSONDecodeError

from .exceptions import YandexDeliveryApiError
from .rest_result import Result


class RestAdapter:
    def __init__(self,
                 hostname:     str,
                 api_key:      str,
                 ver:          str,
                 content_type: str,
                 logger:       logging.Logger = None):
        """

        RestAdapter Constructor

        :param hostname: b2b.taxi.yandex.net/b2b/cargo/integration
        :param api_key: OAuth-token
        :param ver: API version
        :param content_type: Content-Type header
        :param logger: (optional) logger instance
        """
        self._logger = logger or logging.getLogger(__package__)
        self.url = f"https://{hostname}/{ver}"
        self.content_type = content_type
        self._api_key = api_key

    async def _do(self,
                  http_method: str,
                  endpoint:    str,
                  params:      dict = None,
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
        headers = {'content-type': 'application/json', 'Accept-Language': 'ru',
                   'Authorization': f'Bearer {self._api_key}'}
        log_line_pre = f"method={http_method}, url={full_url}, params={params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))

        try:
            self._logger.debug(msg=log_line_pre)
            async with aiohttp.ClientSession(headers=headers) as session:
                response = await session.request(
                    method=http_method,
                    url=endpoint,
                    params=params,
                    json=payload
                )

        except aiohttp.ClientError as e:
            self._logger.error(msg=(str(e)))
            raise YandexDeliveryApiError("Request failed") from e

        try:
            data_out = await response.json()
        except (ValueError, TypeError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise YandexDeliveryApiError("Bad JSON in response") from e

        is_success = 299 >= response.status >= 200
        log_line = log_line_post.format(is_success, response.status, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status, headers=response.headers, message=response.reason, data=data_out)
        self._logger.error(msg=log_line)
        raise YandexDeliveryApiError(f"{response.status}: {response.reason}")

    async def get(self, endpoint: str, params: dict = None) -> Result:
        """
        Implements GET method
        """
        return await self._do(http_method='GET', endpoint=endpoint, params=params)

    async def post(self, endpoint: str, params: dict = None, payload: dict = None) -> Result:
        """
        Implements POST method
        """
        return await self._do(http_method='POST', endpoint=endpoint, params=params, payload=payload)

    async def delete(self, endpoint: str, params: dict = None, payload: dict = None) -> Result:
        """
        Implements DELETE method
        """
        return await self._do(http_method='DELETE', endpoint=endpoint, params=params, payload=payload)
