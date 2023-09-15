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
            msg = "webhook_destination: {} is invalid. 'Discord' or 'Slack' allowed".format(
                webhook_destination
            )
            logger.error(msg)
            raise ValueError(msg)
    except:
        logger.error("Couldn't assemble message (id {})".format(event["id"]))
        raise

    # execute webhook
    try:
        response = requests.post(
            webhook_url, data, headers={"Content-Type": "application/json"}
        )
        logger.info(
            "executed webhook (id {}). Status: {}".format(
                event["id"], response.status_code
            )
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logger.error(
            "Couldn't execute webhook (id {}). Here's why: {}".format(
                event["id"], err.response.text
            )
        )
        raise
