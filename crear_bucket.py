import boto3
import json

def lambda_handler(event, context):
    # Entrada (json)
    try:
        if 'body' in event and event['body']:
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
        else:
            return {
                'statusCode': 400,
                'error': 'Body requerido con el nombre del bucket'
            }
        
        nombre_bucket = body.get('bucket_name')
        if not nombre_bucket:
            return {
                'statusCode': 400,
                'error': 'Campo bucket_name es requerido'
            }
        
        # Proceso
        s3 = boto3.client('s3')
        
        # Crear el bucket
        response = s3.create_bucket(Bucket=nombre_bucket)
        
        # Salida
        return {
            'statusCode': 200,
            'message': f'Bucket {nombre_bucket} creado exitosamente',
            'bucket_name': nombre_bucket,
            'location': response['Location']
        }
        
    except s3.exceptions.BucketAlreadyExists:
        return {
            'statusCode': 409,
            'error': f'El bucket {nombre_bucket} ya existe'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': f'Error al crear bucket: {str(e)}'
        }