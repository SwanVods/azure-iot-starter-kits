import sys
from azure.iot.device.aio import IoTHubDeviceClient

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

class HubManager(object):

    def __init__(self):

        print("\nPython %s\n" % sys.version)
        print("IoT Hub Client for Python")

        self.client = IoTHubDeviceClient.create_from_connection_string('HostName=ProyekAkhir.azure-devices.net;DeviceId=raspberrypi;SharedAccessKey=unMeV1DPFInhQN6IuxXvt98LqoHSr//0Dhi+q4YdukU=')
        self.client.connect()
        

        # set the time until a message times out
        # self.client.receive_message(block=True, timeout=MESSAGE_TIMEOUT)
        # some embedded platforms need certificate information
