import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://cosmos-ariefg.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'deVdBJ7uqnAsbVrxgrMBRridkTeVDYUV4UOTdq7ZAh1mYMrngAPoDk1BeZsCyTzUQ3Wih18rOYAsAE7adpL8SA=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'proyek_akhir'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'sensor_data'),
}