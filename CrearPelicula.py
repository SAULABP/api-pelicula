import boto3
import uuid
import os
import json
import traceback

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

        # Log estándar INFO (json en CloudWatch)
        log = {
            "tipo": "INFO",
            "log_datos": {
                "request_id": context.aws_request_id,
                "mensaje": "Pelicula registrada correctamente",
                "tenant_id": tenant_id,
                "uuid": uuidv4,
                "pelicula_datos": pelicula_datos
            }
        }
        print(json.dumps(log, ensure_ascii=False, default=str))

        # Salida (json)
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # Lectura segura de la entrada: aquí no puede volver a fallar
        body = event.get('body') if isinstance(event, dict) else None
        tenant = body.get('tenant_id') if isinstance(body, dict) else None

        # Log estándar ERROR (json en CloudWatch)
        log = {
            "tipo": "ERROR",
            "log_datos": {
                "request_id": context.aws_request_id,
                "mensaje": "Error al registrar la pelicula",
                "tenant_id": tenant,
                "error_tipo": type(e).__name__,
                "error_detalle": str(e),
                "traceback": traceback.format_exc(),
                "entrada": body
            }
        }
        print(json.dumps(log, ensure_ascii=False, default=str))
        raise
