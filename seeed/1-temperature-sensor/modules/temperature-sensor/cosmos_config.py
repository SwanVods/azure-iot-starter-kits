import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://ariefg.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'z6KcLKgpMCH8ICSdFb30fKvq5IM5KXDAQSqkKnfcNUvOczpgKaWkwxzCuyAnKW0HlBeGqjq8pZVEfbSznbgAFA=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'proyek_akhir'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'sensor_data'),
}