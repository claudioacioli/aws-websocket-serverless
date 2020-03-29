import json
import logging

logger = logging.getLogger("handler_logger")
logger.setLevel(logging.DEBUG)

def ping(event, context):
    logger.info("Ping requested.")
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": "PONG"
    }

    return response


