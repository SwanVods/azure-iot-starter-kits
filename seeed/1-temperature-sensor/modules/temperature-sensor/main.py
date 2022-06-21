#!/usr/bin/env python
import asyncio
import json
import time
import os
import pandas as pd

import azure.cosmos.cosmos_client as cosmos_client

import cosmos_config as config

from gpiozero.pins.native import NativeFactory
from gpiozero import Buzzer
from azure.iot.device.aio import IoTHubDeviceClient
from bme280sensor import BME280Sensor
from azure.iot.device import Message
import aioschedule as schedule

BME280_SEND_ENABLED = True
BME280_SEND_INTERVAL_SECONDS = 15

CONNECTION_STRING = os.getenv("DEVICE_CS")

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

df = pd.DataFrame(columns=['temperature', 'humidity', 'pressure'])

def main():
    hub_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    
    loop = asyncio.get_event_loop()
    
    schedule.every(30).minutes.do(insert_to_database, message='things')

    try:
        
        # Run the sample in the event loop
        loop.run_until_complete(stream_sensor_data(hub_client, BME280Sensor(), Buzzer(12, pin_factory=NativeFactory())))
        loop.run_until_complete(schedule.run_pending())
        
    except KeyboardInterrupt:
        print("IoTHubClients stopped by user")
    finally:
        # Upon application exit, shut down the client
        print("Shutting down IoTHubClient")
        loop.run_until_complete(hub_client.shutdown())
        loop.close()
    
    
async def insert_to_database():
    global df
    
    # Create the Cosmos client object
    db_client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY})
    db_client.get_database_client(DATABASE_ID)
    print('Database with id \'{0}\' was found'.format(DATABASE_ID))
    
    container = db_client.get_container_client(CONTAINER_ID)
    
    temperature = df['temperature'].mean()
    humidity = df['humidity'].mean()
    pressure = df['pressure'].mean()
    
    data = {
        'id' : str(int(time.time())),
        'temperature_avg' : temperature,
        'humidity_avg' : humidity,
        'pressure_avg' : pressure
    }
    
    container.create_item(body=data)
    print('Inserted to database')
    
    # reset df
    df = pd.DataFrame(columns=['temperature', 'humidity', 'pressure'])

async def record_sensor_data(bme280_sensor):
    temperature_sum = 0
    humidity_sum = 0
    pressure_sum = 0
    for n in range(15):
        temperature_sum += bme280_sensor.get_temperature()
        humidity_sum += bme280_sensor.get_humidity()
        pressure_sum += bme280_sensor.get_pressure()
        await asyncio.sleep(1)
        
    global df
    
    df = pd.concat([df, pd.DataFrame({'temperature': [temperature_sum/15], 'humidity': [humidity_sum/15], 'pressure':[pressure_sum/15]})], ignore_index=True, axis=0)
    
    return temperature_sum / 15, humidity_sum / 15, pressure_sum / 15
    
    
async def stream_sensor_data(hub_client, bme280_sensor, buzzer):
    global BME280_SEND_ENABLED
    global BME280_SEND_INTERVAL_SECONDS

    await hub_client.connect()
    
    print("The connection status is : ")
    print(hub_client.connected)

    while True:
        if BME280_SEND_ENABLED:
            print("Sending sensor data to Azure IoT Hub")
            
            # Send BME280 sensor data to Azure IoT Hub.
            temperature, humidity, pressure = await record_sensor_data(bme280_sensor)
            print("Avg. Temperature: {0:0.2f} C, \nAvg. Humidity: {1:0.2f} %, \nAvg. Pressure: {2:0.3f} hPa\n".format(temperature, humidity, pressure))
            
            if(temperature > 32) :
                buzzer.beep(off_time=0.5, n=5)

            message = Message(json.dumps({
                "deviceId": "BME280",   
                "temperature_avg": temperature, 
                "humidity_avg": humidity, 
                "pressure_avg": pressure,
                "timestamp": int(time.time())
            }))
            
            message.message_id = "message_" + str(int(time.time()))
            message.correlation_id = "correlation_" + str(int(time.time()))
            message.content_encoding = "utf-8"
            message.content_type = "application/json"
            message.custom_properties["temperatureAlert"] = "true" if temperature > 32 else "false"
            await hub_client.send_message(message)
        

# run the script
if __name__ == '__main__':
    main()
