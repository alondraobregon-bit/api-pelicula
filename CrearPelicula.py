import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        # Entrada (json)
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        # Salida (json) - Log estandar INFO en CloudWatch
        log = {
            'tipo': 'INFO',
            'log_datos': pelicula
        }
        print(json.dumps(log, default=str))
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    except Exception as e:
        # Salida (json) - Log estandar ERROR en CloudWatch
        log = {
            'tipo': 'ERROR',
            'log_datos': {
                'error_tipo': type(e).__name__,
                'error_mensaje': str(e),
                'event': event
            }
        }
        print(json.dumps(log, default=str))
        return {
            'statusCode': 500,
            'error': str(e)
        }
