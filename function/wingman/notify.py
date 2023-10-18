import os

import requests
import message
import log

logger = log.getLogger()


def send(event) -> None:
    """
    assemble message body and send to webhook.
    """
    webhook_destination = os.environ["WEBHOOK_DESTINATION"]
    webhook_url = os.environ["WEBHOOK_URL"]

    try:
        if webhook_destination == "Discord":
            data = message.format_discord(event)
        elif webhook_destination == "Slack":
            data = message.format_slack(event)
        else:
            msg = f"webhook_destination: {webhook_destination} is invalid. 'Discord' or 'Slack' allowed"
            logger.error(msg)
            raise ValueError(msg)
    except:
        logger.error(f"Could not assemble message (id {event['id']})")
        raise

    # execute webhook
    try:
        response = requests.post(
            webhook_url, data, headers={"Content-Type": "application/json"}
        )
        logger.info(
            f"executed webhook (id {event['id']}). Status: {response.status_code}"
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logger.error(
            f"Couldn't execute webhook (id {event['id']}). Here's why: {err.response.text}"
        )
        raise
