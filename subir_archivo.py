import boto3
import json
import base64

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
                'error': 'Body requerido con bucket_name, directory_name, file_name y file_content_base64'
            }
        
        nombre_bucket = body.get('bucket_name')
        nombre_directorio = body.get('directory_name')
        nombre_archivo = body.get('file_name')
        contenido_base64 = body.get('file_content_base64')
        
        if not all([nombre_bucket, nombre_directorio, nombre_archivo, contenido_base64]):
            return {
                'statusCode': 400,
                'error': 'Campos bucket_name, directory_name, file_name y file_content_base64 son requeridos'
            }
        
        # Construir la ruta completa del archivo
        if not nombre_directorio.endswith('/'):
            nombre_directorio += '/'
        
        ruta_archivo = f"{nombre_directorio}{nombre_archivo}"
        
        # Proceso
        s3 = boto3.resource('s3')
        
        # Decodificar el contenido base64 y subirlo a S3
        s3.Object(nombre_bucket, ruta_archivo).put(Body=base64.b64decode(contenido_base64))
        
        # Salida
        return {
            'statusCode': 200,
            'message': f'Archivo {nombre_archivo} subido exitosamente',
            'bucket_name': nombre_bucket,
            'directory_name': nombre_directorio,
            'file_name': nombre_archivo,
            'file_path': ruta_archivo,
            's3_url': f"s3://{nombre_bucket}/{ruta_archivo}"
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'error': f'Error al subir archivo: {str(e)}'
        }