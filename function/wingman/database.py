import os

import boto3
import botocore
import log
from boto3.dynamodb.conditions import Key

logger = log.getLogger()


def _get_table():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["VLR_EVENTS_TABLE"])

    return table


def get_saved_events() -> list:
    """
    scan DynamoDB table
    """
    table = _get_table()

    try:
        logger.info("Scan table")
        response = table.scan()
        saved_events = response["Items"]
        logger.info(f"Found {len(saved_events)} items.")
    except botocore.exceptions.ClientError as err:
        logger.error(
            f"Couldn't scan events. Here's why: {err.response["Error"]["Code"]}: {err.response["Error"]["Message"]}"
        )
        raise

    return saved_events


def put_events(events) -> None:
    """
    put items into DynamoDB table.
    """
    table = _get_table()

    with table.batch_writer() as batch:
        for event in events:
            try:
                logger.info(f"put event info into the table: {event}")
                batch.put_item({k: v for k, v in event.items()})
            except botocore.exceptions.ClientError as err:
                logger.error(f"Couldn't add event {event["id"]}. Here's why: {err.response["Error"]["Code"]}: {err.response["Error"]["Message"]}")
                raise


def delete_events(events) -> None:
    """
    delete items from DynamoDB table.
    """
    table = _get_table()

    for event in events:
        try:
            logger.info(f"delete event info from the table: {event}")
            table.delete_item(Key={"id": event["id"]})
        except botocore.exceptions.ClientError as err:
            logger.error(f"Couldn't delete event {event["id"]}. Here's why: {err.response["Error"]["Code"]}: {err.response["Error"]["Message"]}")
            raise
