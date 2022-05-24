import smbus2
import bme280

class BME280Sensor():
    def __init__(self):
        self.address = 0x76
        self.bus = smbus2.SMBus(1)
        self.json_temperature_data = None
        self.raw_sensor_data = None

        try:
            self.calibration_params = bme280.load_calibration_params(self.bus, self.address)
        except Exception as e:
            print(e)

    def get_sample(self):
        return bme280.sample(self.bus, self.address, self.calibration_params)

    def get_temperature(self):
        sample = self.get_sample()

        return sample.temperature

    def get_humidity(self):
        sample = self.get_sample()

        return sample.humidity

    def get_pressure(self):
        sample = self.get_sample()

        return sample.pressure

    def get_json_data(self):
        sample = self.get_sample()

        self.json_temperature_data = {
            "temperature": sample.temperature,
            "humidity": sample.humidity,
            "pressure": sample.pressure
        }

        return self.json_temperature_data

    def get_raw_data(self):
        sample = self.get_sample()

        self.raw_sensor_data = {
            "temperature": sample.temperature,
            "humidity": sample.humidity,
            "pressure": sample.pressure
        }

        return self.raw_sensor_data