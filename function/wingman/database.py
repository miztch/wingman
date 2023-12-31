import os

import boto3
import botocore
import log
from boto3.dynamodb.conditions import Key

logger = log.get_logger()


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
        logger.info("Found %s items.", len(saved_events))
    except botocore.exceptions.ClientError as err:
        logger.error(
            "Could not scan events. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
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
                logger.info("put event info into the table: %s", event)
                batch.put_item({k: v for k, v in event.items()})
            except botocore.exceptions.ClientError as err:
                logger.error(
                    "Could not add event %s. Here's why: %s: %s",
                    event["id"],
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise


def delete_events(events) -> None:
    """
    delete items from DynamoDB table.
    """
    table = _get_table()

    for event in events:
        try:
            logger.info("delete event info from the table: %s", event)
            table.delete_item(Key={"id": event["id"]})
        except botocore.exceptions.ClientError as err:
            logger.error(
                "Could not delete event %s. Here's why: %s: %s",
                event["id"],
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
