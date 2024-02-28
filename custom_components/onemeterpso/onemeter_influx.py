import logging
import json
import dateutil.parser

from influxdb import InfluxDBClient


_LOGGER = logging.getLogger(__name__)

class OnemeterInflux:  # pylint: disable=too-many-instance-attributes
    """Instance of OnemeterInflux"""

    def __init__(  # pylint: disable=too-many-arguments
      self,
      onemeterdata,
      influxdbhost,
      influxdbport,
      influxdbdatabase,
      influxdbusername,
      influxdbpassword,
    ) -> None:
      self._onemeterdata = onemeterdata
      self.influxdbhost = influxdbhost
      self.influxdbport = influxdbport
      self.influxdbdatabase = influxdbdatabase
      if (influxdbusername == ""):
        influxdbusername = None

      self.influxdbtoken = None
      if (influxdbusername is None):
        self.influxdbtoken = influxdbpassword
        influxdbpassword = None
      self.influxdbusername = influxdbusername
      self.influxdbpassword = influxdbpassword

    async def recode_to_influxpoints(
      self,
      hass
    ) -> None:

      _influx_points = []
      index = 0
      for detail in self._onemeterdata:
        index = index + 1
        if index == 5:
          break;
        point = {}
        point["measurement"]="kWh"
        point["tags"] = {}
        point["tags"]["domain"] = "onemeter"
        point["tags"]["entity"] = "tarif"
        point["time"] = detail["date"]
        point["fields"] = {}
        point["fields"]["value"] = detail['1_8_0']
        point["fields"]["valuelow"] = detail['1_8_1']
        point["fields"]["valuehigh"] = detail['1_8_2']
        _influx_points.append(point)

#      _LOGGER.info(_influx_points)


      _influx_points = []
      index = 0
      for detail in self._onemeterdata:
        index = index + 1
        point = {}
        point["measurement"]="kWh"
        point["tags"] = {}
        point["tags"]["meter"] = detail['C_1_0']
        point["time"] = detail["date"]
        point["fields"] = {}

        if detail['1_8_0'] != "":
          point["fields"]["value"] = float(detail['1_8_0'])
        if detail['1_8_1'] != "":
          point["fields"]["valuehigh"] = float(detail['1_8_1'])
        if detail['1_8_2'] != "":
          point["fields"]["valuelow"] = float(detail['1_8_2'])

        _influx_points.append(point)

#      _LOGGER.info(_influx_points)
      if self.influxdbtoken is None:
        cli = InfluxDBClient(self.influxdbhost, self.influxdbport, self.influxdbusername, self.influxdbpassword,self.influxdbdatabase)
      else:
        headers = {}
        headers.setdefault("Authorization", "Token "+self.influxdbtoken)
        cli = InfluxDBClient(self.influxdbhost, self.influxdbport, self.influxdbusername, self.influxdbpassword, self.influxdbdatabase,
                headers = headers)

      def cliwrite():
        cli.write_points(
          _influx_points,
        )

      await hass.async_add_executor_job(cliwrite)
      _LOGGER.info(str(index)+" points written.")
