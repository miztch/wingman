import json
import os

import requests
import log
from constants import countries

logger = log.getLogger()


def send(event) -> None:
    """
    assemble message body and send to webhook.
    """
    webhook_url = os.environ["WEBHOOK_URL"]

    # region emoji
    if event["eventCountryFlag"] == "un":
        region_emoji = ":united_nations:"
    else:
        region_emoji = ":flag_{}:".format(event["eventCountryFlag"])

    # assemble webhook data
    data = json.dumps(
        {
            "embeds": [
                {
                    "title": event["eventName"],
                    "url": event["eventUrl"],
                    "color": 394046,
                    "footer": {"text": "new event on vlr.gg"},
                    "thumbnail": {"url": event["eventLogoUrl"]},
                    "fields": [
                        {
                            "name": ":earth_americas: REGION",
                            "value": "{} {}".format(
                                region_emoji, countries[event["eventCountryFlag"]]
                            ),
                            "inline": True,
                        },
                        {
                            "name": ":calendar: DATES",
                            "value": event["dates"],
                            "inline": True,
                        },
                    ],
                }
            ],
        }
    )

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
