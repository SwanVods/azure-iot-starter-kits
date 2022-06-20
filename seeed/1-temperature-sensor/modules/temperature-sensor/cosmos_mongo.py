from time import time

def delete_document(collection, document_id):
    """Delete the document containing document_id from the collection"""
    collection.delete_one({"_id": document_id})
    print("Deleted document with _id {}".format(document_id))

def read_document(collection, document_id):
    """Return the contents of the document containing document_id"""
    print("Found a document with _id {}: {}".format(document_id, collection.find_one({"_id": document_id})))

def insert_document(collection, temperature, humidity, pressure):
    """Insert a sample document and return the contents of its _id field"""

    temperature_data = {
        'sensor_id': 'BME280',
        'ambient_temperature_avg': temperature,
        'ambient_humidity_avg': humidity,
        'machine_pressure_avg': pressure,
        'ts': int(time())
    }
    document_id = collection.insert_one(temperature_data).inserted_id
    print("Inserted document with _id {}".format(document_id))
    return document_id

def create_database_unsharded_collection(client, database_id, collection_id):
    """Create database with shared throughput if it doesn't exist and an unsharded collection"""
    db = client[database_id]

    # Create database if it doesn't exist
    if database_id not in client.list_database_names():
        # Database with 400 RU throughput that can be shared across the DB's collections
        db.command({'customAction': "CreateDatabase", 'offerThroughput': 400})
        print("Created db {} with shared throughput". format(database_id))
    
    # Create collection if it doesn't exist
    if collection_id not in db.list_collection_names():
        # Creates a unsharded collection that uses the DBs shared throughput
        db.command({'customAction': "CreateCollection", 'collection': collection_id})
        print("Created collection {}". format(collection_id))

    return db[collection_id]