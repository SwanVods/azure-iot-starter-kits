#!/usr/bin/env python
import asyncio
import json
import time
import cosmos_mongo as cosmos
import pymongo

# import local devicecheck module and azure.iot.device
import devicecheck
import hubmanager
from azure.iot.device.aio import IoTHubDeviceClient
from bme280sensor import BME280Sensor
from azure.iot.device import Message


BME280_SEND_ENABLED = True
BME280_SEND_INTERVAL_SECONDS = 5

CONNECTION_STRING = "HostName=ProyekAkhir.azure-devices.net;DeviceId=raspberrypi;SharedAccessKey=unMeV1DPFInhQN6IuxXvt98LqoHSr//0Dhi+q4YdukU="

DB_CONNECTION_STRING = "mongodb://cosmos-ta:H1NEBb3nPPBH2leGlplggZNcVFeIxGrwSm1Sl8wrbXGlsPnHslYZoR3WvjRFAVB8E5B6fuIKjgFzRSIORMyRMw==@cosmos-ta.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@cosmos-ta@" # Prompts user for connection string
DB_NAME = "proyek_akhir"
UNSHARDED_COLLECTION_NAME = "sensor_data"

# allows the user to quit the program from the terminal
def stdin_listener():
    """
    Listener for quitting the stream
    """
    while True:
        if KeyboardInterrupt:
            print("Quitting...")
            break

async def main():
    hub_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    await hub_client.connect()
    print("The connection status is : ")
    print(hub_client.connected)
    
     # initialize bme280 sensor
    bme280_sensor = BME280Sensor()
    
    # initialize mongodb
    db_client = pymongo.MongoClient(DB_CONNECTION_STRING)
    try:
        db_client.server_info() # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")
    
    async def stream_sensor_data(hub_client, bme280_sensor, client):
        global BME280_SEND_ENABLED
        global BME280_SEND_INTERVAL_SECONDS

        while True:
            if BME280_SEND_ENABLED:
                # Send BME280 sensor data to Azure IoT Hub.
                temperature = bme280_sensor.get_temperature()
                humidity = bme280_sensor.get_humidity()
                pressure = bme280_sensor.get_pressure()
                print("Temperature: {} C\nHumidity: {} %\nPressure: {} hPa".format(temperature, humidity, pressure))
                
                # insert to cosmos DB
                # db.insert((temperature, humidity, pressure))
                # db = client.get_database_client(DATABASE_ID)
                # container = db.get_container_client(CONTAINER_ID)
                # cosmos.create_item(container, temperature, humidity, pressure)
                
                # collection = cosmos.create_database_unsharded_collection(client, DB_NAME, UNSHARDED_COLLECTION_NAME)
                # cosmos.insert_document(collection, temperature, humidity, pressure)

                message = Message(json.dumps({
                    "machine": {
                        "temperature": temperature, 
                        "pressure": pressure,
                    },
                    "ambient": {
                        "temperature": temperature,
                        "humidity": humidity,
                    }, 
                    "timestamp": time.time()
                }))
                
                message.message_id = "message_" + str(int(time.time()))
                message.correlation_id = "correlation_" + str(int(time.time()))
                message.content_encoding = "utf-8"
                message.content_type = "application/json"
                message.custom_properties["temperatureAlert"] = "true" if temperature > 30 else "false"
                await hub_client.send_message(message)
            await asyncio.sleep(BME280_SEND_INTERVAL_SECONDS)

    
    send_telemetry_task = asyncio.create_task(stream_sensor_data(hub_client, bme280_sensor, db_client)) 
    
    # try:
        # start the sensor streaming
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)
    
    await user_finished
    
    send_telemetry_task.cancel()
    await hub_client.disconnect()
        # loop.run_until_complete(stream_sensor_data(hub_manager.client, bme280_sensor, db_client))

# run the script
if __name__ == '__main__':
    asyncio.run(main())
    # initialize hub manager
    # hub_manager = hubmanager.HubManager(CONNECTION_STRING)

   
