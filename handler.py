import json
import logging
import os
import boto3
import time

logger = logging.getLogger("handler_logger")
logger.setLevel(logging.DEBUG)

table_name = os.getenv('MESSAGES_TABLE')
dynamodb = boto3.resource("dynamodb")


def ping(event, context):
    logger.info("Table name: " + table_name)
 
    table = dynamodb.Table(table_name)
    timestamp = int(time.time())
    table.put_item(Item={"Room": "general", "Index":0, 
        "Timestamp": timestamp, "Username": "ping-user",
        "Content": "PING!"})

    logger.debug("Item added to the database.")

    response = {
        "statusCode": 200,
        "body": "PONG!"
    }

    return response


