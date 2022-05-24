from azure.iot.device.aio import IoTHubDeviceClient

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

class HubManager(object):

    async def __init__(self, connection_string):
        self.client = IoTHubDeviceClient.create_from_connection_string(connection_string)
        await self.client.connect()

    async def send_message(self, message):
        self.client.send_message(message)

    async def receive_message(self):
        message = self.client.receive_message()
        return message

    async def disconnect(self):
        await self.client.disconnect()
