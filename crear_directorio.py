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
                'error': 'Body requerido con bucket_name y directory_name'
            }
        
        nombre_bucket = body.get('bucket_name')
        nombre_directorio = body.get('directory_name')
        
        if not nombre_bucket or not nombre_directorio:
            return {
                'statusCode': 400,
                'error': 'Campos bucket_name y directory_name son requeridos'
            }
        
        # Asegurar que el directorio termine con /
        if not nombre_directorio.endswith('/'):
            nombre_directorio += '/'
        
        # Proceso
        s3 = boto3.client('s3')
        
        # Crear el directorio (objeto vacío con / al final)
        s3.put_object(
            Bucket=nombre_bucket,
            Key=nombre_directorio,
            Body=''
        )
        
        # Salida
        return {
            'statusCode': 200,
            'message': f'Directorio {nombre_directorio} creado exitosamente en bucket {nombre_bucket}',
            'bucket_name': nombre_bucket,
            'directory_name': nombre_directorio
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'error': f'Error al crear directorio: {str(e)}'
        }