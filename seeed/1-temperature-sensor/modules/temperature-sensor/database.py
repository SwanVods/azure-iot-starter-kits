import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()
        
    def connect(self):
        self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
        
    def insert(self, data):
        cursor = self.connection.cursor()
        query = "INSERT INTO sensor_data (temperature, humidity, pressure, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())"
        cursor.execute(query, data)
        self.connection.commit()
        print(cursor.rowcount, "record inserted.\n")
        
    def find(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()