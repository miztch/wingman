import os
import json
import requests
import message
import log

logger = log.get_logger()


def send(event) -> None:
    """
    assemble message body and send to webhook.
    """
    webhook_destination = os.environ["WEBHOOK_DESTINATION"]
    webhook_url = os.environ["WEBHOOK_URL"]

    try:
        if webhook_destination == "Discord":
            payload = message.format_discord(event)
        elif webhook_destination == "Slack":
            payload = message.format_slack(event)
        else:
            msg_invalid_dest = f"WEBHOOK_DESTINATION: {webhook_destination} is invalid. 'Discord' or 'Slack' allowed"
            logger.error(msg_invalid_dest)
            raise ValueError(msg_invalid_dest)
    except Exception as err:
        logger.error("Could not assemble message (id: %s). Error: %s", event["id"], err)
        raise

    # execute webhook
    try:
        response = requests.post(
            webhook_url,
            json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )
        logger.info(
            "executed webhook (id %s). Status: %s", event["id"], response.status_code
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logger.error(
            "Could not execute webhook (id: %s). Here's why: %s",
            event["id"],
            err.response.text,
        )
        raise
    except Exception as err:
        logger.error(
            "Could not execute webhook (id: %s). Here's why: %s",
            event["id"],
            err,
        )
        raise
