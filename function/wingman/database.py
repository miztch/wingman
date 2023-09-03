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
        logger.info("Found {} items.".format(len(saved_events)))
    except botocore.exceptions.ClientError as err:
        logger.error(
            "Couldn't scan events. Here's why: {}: {}".format(
                err.response["Error"]["Code"], err.response["Error"]["Message"]
            )
        )
        raise

    return saved_events


def put_events(events) -> None:
    """
    put items into specified DynamoDB table.
    """
    table = _get_table()

    with table.batch_writer() as batch:
        for event in events:
            try:
                logger.info("put event info into the table: {}".format(event))
                batch.put_item({k: v for k, v in event.items()})
            except botocore.exceptions.ClientError as err:
                logger.error(
                    "Couldn't add event {}. Here's why: {}: {}".format(
                        event["id"],
                        err.response["Error"]["Code"],
                        err.response["Error"]["Message"],
                    )
                )
                raise


def delete_events(events) -> None:
    table = _get_table()

    for event in events:
        try:
            table.delete_item(Key={"id": event["id"]})
        except botocore.exceptions.ClientError as err:
            logger.error(
                "Couldn't delete event {}. Here's why: {}: {}".format(
                    event["id"],
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
            )
            raise
