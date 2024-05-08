import logging
import httpx
import json
import dateutil.parser
from datetime import datetime, timedelta

from .onemeter_influx import OnemeterInflux

_LOGGER = logging.getLogger(__name__)

class OnemeterReaderDetail:  # pylint: disable=too-many-instance-attributes
    """Instance of EnvoyReader"""

    # P0 for older Envoy model C, s/w < R3.9 no json pages
    # P for production data only (ie. Envoy model C, s/w >= R3.9)
    # PC for production and consumption data (ie. Envoy model S)

    def __init__(  # pylint: disable=too-many-arguments
        self,
        hass,
        url,
        deviceid="",
        apikey="",
        influxdbhost="",
        influxdbport="",
        influxdbdatabase="",
        influxdbusername="",
        influxdbpassword="",
        shortreading="0",
        async_client=None,
        ) -> None:
        """Init the OnemeterReaderDetail."""
        self.hass = hass
        self.url = url
        self.deviceid = deviceid
        self.apikey = apikey
        self.influxdbhost = influxdbhost
        self.influxdbport = influxdbport
        self.influxdbdatabase = influxdbdatabase
        self.influxdbusername = influxdbusername
        self.influxdbpassword = influxdbpassword
        self._async_client = async_client
        self._auth = '{ header = ' + apikey  + '}'
        self._last_data = None
        self._shortreading = shortreading

    @property
    def async_client(self):
        """Return the httpx client."""
        return self._async_client or httpx.AsyncClient(verify=False)

    async def getData(self):  # pylint: disable=invalid-name
        """Fetch data from the endpoint and if inverters selected default"""
        """to fetching inverter data."""

        # Check if the Secure flag is set
        _LOGGER.debug("Onemeter getdatadetail: %s %s %s", self.url, self.deviceid, self.apikey)

#        mojedatetime = dateutil.parser.isoparse(output["lastReading"]["date"])
        timeshift = ""
        _LOGGER.debug("=================================================="+self._shortreading);
        if (self._shortreading == "1"):
          dt = datetime.now() - timedelta(days=1);
          timeshift = "?from="+dt.strftime("%Y-%m-%d %H:%M:%S")
          _LOGGER.debug(dt.strftime("%Y-%m-%d %H:%M:%S"));
        #2023-08-03T16:30:00.000Z

        try:
            response = await self.async_client.get(
                self.url+"/"+self.deviceid+"/Readings"+timeshift, headers={
                                       "Authorization": self.apikey
                                  }, timeout=120
            )
            response.raise_for_status()
            self._last_data = response.text
            #_LOGGER.info("Data Get from onemeter: %s", self._last_data)
            output=json.loads(self._last_data)
            _onemeterdata = output["readings"]

#            _LOGGER.info("DebugReaderDetail %s", len(_onemeterdata))
            if len(_onemeterdata) != 0:
              _LOGGER.debug("DebugReaderDetailPointFirst %s", _onemeterdata[0])

            for one in _onemeterdata:
              one1 = one

            if len(_onemeterdata) != 0:
              _LOGGER.debug("DebugReaderDetailPointLast %s", one1)

#            jsondata = json.load(_onemeterdata[0])
#            _LOGGER.info("DebugReaderDetailPoint180 %s", _onemeterdata[0]['C_1_0'])
#            _LOGGER.info("DebugReaderDetailPoint180 %s", _onemeterdata[0]['date'])
#            _LOGGER.info("DebugReaderDetailPoint180 %s", _onemeterdata[0]['1_8_0'])
#            _LOGGER.info("DebugReaderDetailPoint180 %s", _onemeterdata[0]['1_8_1'])
#            _LOGGER.info("DebugReaderDetailPoint180 %s", _onemeterdata[0]['1_8_2'])

            onemeter_influx = OnemeterInflux(
              _onemeterdata,
              self.influxdbhost,
              self.influxdbport,
              self.influxdbdatabase,
              self.influxdbusername,
              self.influxdbpassword,
            )

            await onemeter_influx.recode_to_influxpoints(
              self.hass
            )

        except httpx.TimeoutException:
            _LOGGER.error("Timeout getting data")
            return self._last_data
        except (httpx.RequestError, httpx.HTTPStatusError) as err:
            _LOGGER.error("Error getting data from %s %s:", err, self.url+"/"+self.deviceid)
            return self._last_data

    async def get_full_serial_number(self):
        return "123456789"
