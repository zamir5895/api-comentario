import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    bucket_name = os.environ["INGEST_BUCKET_NAME"]  
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
            'texto': texto
        }
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)
    s3_client = boto3.client('s3')
    s3_key = f"{tenant_id}/{uuidv1}.json"
    s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=json.dumps(comentario))
    
    print(comentario)
    return {
        'statusCode': 200,
        'message' : 'Se creo con exito el comentario',
        'comentario': comentario,
        'response': response
    }
