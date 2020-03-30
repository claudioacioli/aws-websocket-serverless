import json
import logging
import os
import boto3
import time

logger = logging.getLogger("handler_logger")
logger.setLevel(logging.DEBUG)

messages_table = os.getenv("MESSAGES_TABLE")
connections_table = os.getenv("CONNECTIONS_TABLE")
dynamodb = boto3.resource("dynamodb")
endpoint = os.getenv('WEBSOCKET_API_ENDPOINT')

def ping(event, context):
    logger.info("Table name: " + table_name)
 
    table = dynamodb.Table(messages_table)
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


def connection_manager(event, context):

    """
    Handles connecting and disconnecting for the websocket.
    """

    connectionID = event["requestContext"].get("connectionId")

    if event["requestContext"]["eventType"] == "CONNECT":
        
        logger.info("Connect requested")
        
        table = dynamodb.Table(connections_table)
        table.put_item(Item={"ConnectionId": connectionID})

        return {"statusCode": 200, "body": "Connect successful"}

    elif event["requestContext"]["eventType"] == "DISCONNECT":
        
        logger.info("Disconnect requested")

        table = dynamodb.Table(connections_table)
        table.delete_item(key={"ConnectionId": connectionID})

        return {"statusCode": 200, "body": "Disconnect successful"}

    else:
        logger.error("Connection manager received unrecognized eventType.")
        return {"statusCode": 200, "body": "Unrecognized eventType."}


def _get_body(event):
    try:
        return json.loads(event.get("body", ""))
    except:
        logger.debug("event body could not be JSON decoded.")


def send_message(event, context):
    table = dynamodb.Table(connections_table)
    response = table.scan(ProjectionExpression="ConnectionId")
    connections = response.get("Items", [])
    for c in connections:
        logger.debug(c.get("ConnectionId", ""))
        gatewayapi = boto3.client("apigatewaymanagementapi", \
                endpoint_url = endpoint)
        gatewayapi.post_to_connection(ConnectionId=c.get("ConnectionId", ""),
                Data=json.dumps({"cotacao": "10"}).encode("utf-8"))
    return {"statusCode": 200, "body": "Message sent to all connections."}
