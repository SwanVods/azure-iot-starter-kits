import uuid
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
        
def create_item(container, temperature, humidity, pressure):
    print('\nCreating Items\n')

    temperature_data = {
        'id': str(uuid.uuid1()),
        'sensor_id': 'BME280',
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure
    }
    
    container.create_item(body=temperature_data)
        
def read_item(container, doc_id, partition_key):
    print('\nReading Item\n')
    
    try:
        item = container.read_item(doc_id, partition_key)
        print('Read item \'{0}\' with id \'{1}\' from container \'{2}\''.format(item, doc_id, container.id))
    
    except exceptions.CosmosHttpResponseError as e:
        if e.status_code == 404:
            print('Item with id \'{0}\' does not exist'.format(doc_id))
        else:
            raise
        
def read_items(container):
    #reading all items on container
    data_list = list(container.read_all_items(max_item_count=100))
    print('Found {0} items'.format(data_list.__len__()))
    for doc in data_list:
        print('Item Id: {0}'.format(doc.get('id')))
    
def query_items(container, id):
    print('\nQuerying for an Item by Id\n')
    
    items = list(container.query_items(
        query="SELECT * FROM c WHERE c.id = '{0}'".format(id),
    ))
    
    print('Item queried by Id \'{0}\' is \'{1}\''.format(id, items[0]))
    
