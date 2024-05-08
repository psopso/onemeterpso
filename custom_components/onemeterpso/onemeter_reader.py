import logging
import httpx
import json
import dateutil.parser

_LOGGER = logging.getLogger(__name__)

class OnemeterReader:  # pylint: disable=too-many-instance-attributes
    """Instance of EnvoyReader"""

    # P0 for older Envoy model C, s/w < R3.9 no json pages
    # P for production data only (ie. Envoy model C, s/w >= R3.9)
    # PC for production and consumption data (ie. Envoy model S)

    def __init__(  # pylint: disable=too-many-arguments
        self,
        url,
        deviceid="",
        apikey="",
        async_client=None,
        ) -> None:
        """Init the OnemeterReader."""
        self.url = url
        self.deviceid = deviceid
        self.apikey = apikey
        self._async_client = async_client
        self._auth = '{ header = ' + apikey  + '}'
        self._last_data = None
        self.date = None
        self._onemeterdate = ""
        self._onemeterthismonth = None
        self._onemeterpreviousmonth = None

        self._value1_8_0 = None
        self._value1_8_1 = None
        self._value1_8_2 = None

    async def onemeterdate(self):
      return self._onemeterdate
    async def onemeterthismonth(self):
      return self._onemeterthismonth
    async def onemeterpreviousmonth(self):
      return self._onemeterpreviousmonth

    async def obis180(self):
      return self._value1_8_0
    async def obis181(self):
      return self._value1_8_1
    async def obis182(self):
      return self._value1_8_2

    @property
    def async_client(self):
        """Return the httpx client."""
        return self._async_client or httpx.AsyncClient(verify=False)

    async def getData(self):  # pylint: disable=invalid-name
        """Fetch data from the endpoint and if inverters selected default"""
        """to fetching inverter data."""

        # Check if the Secure flag is set
        _LOGGER.debug("Onemeter getdata: %s %s %s", self.url, self.deviceid, self.apikey)

        try:
#            async_client = get_async_client(self.hass, verify_ssl=self.verify_ssl)
            response = await self.async_client.get(
                self.url+"/"+self.deviceid, headers={
                                       "Authorization": self.apikey
                                  }, timeout=120
            )
            response.raise_for_status()
            self._last_data = response.text
            #_LOGGER.info("Data Get from onemeter: %s", self._last_data)
            output=json.loads(self._last_data)
            _LOGGER.debug("Test: %s", output["lastReading"]["date"])

            mojedatetime = dateutil.parser.isoparse(output["lastReading"]["date"])

            value1_8_0 = output["lastReading"]["OBIS"]["1_8_0"]  # Celkem
            value1_8_1 = output["lastReading"]["OBIS"]["1_8_1"]  # VT
            value1_8_2 = output["lastReading"]["OBIS"]["1_8_2"]  # NT

            self._onemeterdate = mojedatetime.strftime("%d.%m.%Y, %H:%M:%S")
            self._onemeterthismonth = output["usage"]["thisMonth"]
            self._onemeterpreviousmonth = output["usage"]["previousMonth"]

            self._value1_8_0 = value1_8_0
            self._value1_8_1 = value1_8_1
            self._value1_8_2 = value1_8_2

            _LOGGER.debug("Datum: %s", mojedatetime.ctime())

            _LOGGER.debug("Test: %s", output["usage"]["thisMonth"])
            _LOGGER.debug("Test: %s", output["usage"]["previousMonth"])

            _LOGGER.debug("DebugReader")

        except httpx.TimeoutException:
            _LOGGER.error("Timeout getting data")
            return self._last_data
        except (httpx.RequestError, httpx.HTTPStatusError) as err:
            _LOGGER.error("Error getting data from %s %s:", err, self.url+"/"+self.deviceid)
            return self._last_data

    async def get_full_serial_number(self):
        return "123456789"
